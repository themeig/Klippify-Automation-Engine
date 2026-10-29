import paths
import os
import re
import sys
import json
import shutil
import time
from datetime import datetime, timedelta
from pathlib import Path
from klippify_scraper import fetch_klippify_submissions
import video_captioner
import video_inspector

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = paths.PROJECT_ROOT
AUDIT_STATE_FILE = BASE_DIR / "rejection_audit_state.json"
APPROVAL_REPORT_FILE = BASE_DIR / "approval_audit_report.json"
SCHEDULES_FILE = BASE_DIR / "campaign_schedules.json"
PUBLISHED_CONTENT_FILE = BASE_DIR / "published_content.json"
CLIP_METADATA_FILE = BASE_DIR / "clip_metadata.json"
SUBMISSIONS_CACHE_FILE = BASE_DIR / "klippify_submissions.json"


def load_audit_state():
    default_state = {
        "last_audit_time": None,
        "resolved_rejections": [],
        "active_experiment": None,
        "propagation_history": [],
        "campaigns_needing_attention": {}
    }
    if AUDIT_STATE_FILE.exists():
        try:
            with open(AUDIT_STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for k, v in default_state.items():
                    if k not in data:
                        data[k] = v
                return data
        except Exception:
            pass
    return default_state


def save_audit_state(state):
    try:
        with open(AUDIT_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[AUDIT ERROR] Impossibile salvare audit state: {e}")


def save_approval_report(report):
    try:
        with open(APPROVAL_REPORT_FILE, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[AUDIT ERROR] Impossibile salvare approval report: {e}")


def _load_json_safe(file_path: Path, default_val):
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return default_val


def _parse_iso_dt(created_str: str, fallback: datetime) -> datetime:
    if created_str:
        try:
            return datetime.fromisoformat(created_str.replace("Z", "+00:00")).replace(tzinfo=None)
        except Exception:
            pass
    return fallback


def get_campaign_cta_and_brief(campaign_id: str) -> dict:
    """
    Recupera il brief reale e la Call-To-Action specifica della campagna Klippify.
    Non usa MAI CTA hardcoded di altre campagne.
    """
    brief = {}
    if campaign_id:
        try:
            brief = video_inspector.load_campaign_brief(str(campaign_id)) or {}
        except Exception:
            brief = {}

    raw_cta = (brief.get("call_to_action") or "").strip()
    if "su klippify" in raw_cta.lower():
        raw_cta = ""

    mentions = brief.get("mandatory_mentions") or []
    primary_mention = mentions[0] if mentions else ""
    if primary_mention and not primary_mention.startswith("@"):
        primary_mention = f"@{primary_mention}"

    if raw_cta:
        effective_cta = raw_cta
    elif primary_mention:
        effective_cta = f"Visita il profilo ufficiale {primary_mention}"
    elif brief.get("name"):
        effective_cta = f"Scopri di più su {brief['name']}"
    else:
        effective_cta = "Visita il profilo ufficiale per saperne di più!"

    return {
        "campaign_id": str(campaign_id or ""),
        "campaign_name": brief.get("name") or str(campaign_id or ""),
        "brand": brief.get("brand") or "",
        "cta_text": effective_cta,
        "primary_mention": primary_mention,
        "mandatory_mentions": mentions,
        "mandatory_hashtags": brief.get("mandatory_hashtags") or [],
        "rules": brief.get("rules") or [],
        "video_prompt": brief.get("video_prompt") or ""
    }


def match_submission_to_local_clip(submission: dict, published_records: list, clip_metadata: dict) -> dict:
    """
    Collega una submission Klippify (post_url) al file MP4 locale e ai suoi metadati di regia AI
    (hook_text, cta_text, segments, raw_source_video).
    """
    post_url = (submission.get("post_url") or "").strip()
    video_id_match = re.search(r"/video/(\d+)", post_url)
    sub_video_id = video_id_match.group(1) if video_id_match else None

    matched_pub = None
    if post_url or sub_video_id:
        for rec in reversed(published_records):
            rec_url = (rec.get("post_url") or rec.get("tiktok_url") or "").strip()
            rec_vid = str(rec.get("video_id") or "").strip()
            if (post_url and rec_url and post_url == rec_url) or (sub_video_id and rec_vid and sub_video_id == rec_vid):
                matched_pub = rec
                break

    filename = matched_pub.get("filename") if matched_pub else None
    meta = clip_metadata.get(filename, {}) if filename else {}

    return {
        "clip_filename": filename,
        "published_title": matched_pub.get("title") if matched_pub else None,
        "published_at": matched_pub.get("published_at") or matched_pub.get("timestamp") if matched_pub else None,
        "hook_text": meta.get("hook_text"),
        "cta_text": meta.get("cta_text"),
        "brand_mention": meta.get("brand_mention"),
        "segments": meta.get("segments"),
        "raw_source_video": meta.get("raw_source_video"),
        "directed_by": meta.get("directed_by")
    }


def diagnose_rejection_reason(ai_reasoning: str, campaign_info: dict) -> dict:
    """
    Analizza la motivazione di rifiuto dell'AI di Klippify (ai_reasoning)
    e genera un'istruzione operativa precisa per l'Agente AI Director.
    """
    reason_text = (ai_reasoning or "").strip()
    lower = reason_text.lower()
    cta = campaign_info.get("cta_text", "")
    mention = campaign_info.get("primary_mention", "")
    camp_name = campaign_info.get("campaign_name", "questa campagna")

    categories = []
    instructions = []

    if any(k in lower for k in ["call to action", "cta", "action at the end", "link in bio", "profilo"]):
        categories.append("missing_or_weak_cta")
        instructions.append(
            f"Assicurati che gli ultimi 3.5s (e il parlato finale) contengano esplicitamente la CTA di '{camp_name}': \"{cta}\" {mention}".strip()
        )
    if any(k in lower for k in ["hook", "first 3 seconds", "initial", "attention", "primi 3 secondi"]):
        categories.append("weak_hook")
        instructions.append(
            "Scegli un primo segmento (teaser_hook) con impatto immediato nei primi 3 secondi e imposta un hook_text forte nel banner superiore."
        )
    if any(k in lower for k in ["subtitle", "caption", "sottotitol", "text on screen"]):
        categories.append("missing_subtitles")
        instructions.append(
            "Verifica che l'audio parlato sia chiaro e che i sottotitoli dinamici ASS vengano impressi lungo tutta la clip."
        )
    if any(k in lower for k in ["duration", "too short", "too long", "seconds", "durata"]):
        categories.append("duration_out_of_bounds")
        instructions.append(
            "Mantieni la durata complessiva della clip rigorosamente tra 28 e 50 secondi."
        )
    if any(k in lower for k in ["guideline", "rule", "brand", "off-topic", "prompt", "unrelated", "mention"]):
        categories.append("guideline_mismatch")
        instructions.append(
            f"Allinea rigorosamente i segmenti scelti al brief di '{camp_name}' ({campaign_info.get('video_prompt') or 'vedi regole campagna'})."
        )

    if not categories:
        categories.append("general_rejection")
        instructions.append(
            f"Rivedi i segmenti del video per '{camp_name}' correggendo quanto segnalato dall'AI di Klippify: \"{reason_text}\"."
        )

    return {
        "categories": categories,
        "ai_reasoning": reason_text or "Nessuna motivazione fornita da Klippify.",
        "ai_director_instruction": " ".join(instructions)
    }


def get_chronological_available_clips(campaign_id):
    """
    Restituisce tutte le clip vergini disponibili sul disco per la campagna, ordinate cronologicamente.
    """
    clips_dir = BASE_DIR / "generated_videos" / str(campaign_id) / "clips"
    if not clips_dir.exists():
        return []

    pub_clips = []
    if SCHEDULES_FILE.exists():
        try:
            with open(SCHEDULES_FILE, "r", encoding="utf-8") as f:
                sched = json.load(f)
                pub_clips = sched.get(str(campaign_id), {}).get("published_clips", [])
        except Exception:
            pass

    candidates = []
    for f in clips_dir.glob("*.mp4"):
        if f.name not in pub_clips and not f.name.startswith("temp_"):
            try:
                candidates.append((f, f.stat().st_mtime))
            except Exception:
                candidates.append((f, 0))

    candidates.sort(key=lambda x: (x[1], x[0].name))
    return [c[0] for c in candidates]


def apply_fix_to_clip(clip_path, campaign_id=None, brand_cta=None):
    """
    Applica il re-rendering con Outro CTA Card specifica della campagna sulla clip specificata.
    Se la clip è già stata montata dall'AI Director (ha già sottotitoli e banner impressi),
    NON sovrascrive con doppi sottotitoli ma segnala che serve un nuovo taglio dal sorgente grezzo.
    """
    clip_path = Path(clip_path)
    clip_metadata = _load_json_safe(CLIP_METADATA_FILE, {})
    meta = clip_metadata.get(clip_path.name, {})

    inferred_campaign_id = str(campaign_id or meta.get("campaign_id") or "")
    if not inferred_campaign_id and clip_path.parent.name == "clips":
        inferred_campaign_id = clip_path.parent.parent.name

    if meta.get("directed_by") == "antigravity_ai_director":
        print(
            f"[AUDIT ADAPTATION] ℹ️ La clip '{clip_path.name}' ha già sottotitoli e grafica AI Director impressi. "
            f"Segnalata per ri-taglio pulito da sorgente grezzo invece di sovrascrivere i sottotitoli."
        )
        return False

    camp_info = get_campaign_cta_and_brief(inferred_campaign_id)
    effective_cta = brand_cta or camp_info["cta_text"]

    try:
        temp_out = clip_path.parent / f"temp_fix_{int(time.time())}_{clip_path.name}"
        res = video_captioner.burn_captions_to_video(
            str(clip_path),
            output_video=str(temp_out),
            style_key="hormozi_gold",
            brand_cta=effective_cta
        )
        if res.get("status") == "success" and temp_out.exists() and temp_out.stat().st_size > 100000:
            shutil.move(str(temp_out), str(clip_path))
            print(f"[AUDIT ADAPTATION] ✅ Clip '{clip_path.name}' aggiornata con CTA '{effective_cta}'!")
            return True
        else:
            if temp_out.exists():
                temp_out.unlink()
            return False
    except Exception as ex:
        print(f"[AUDIT ADAPTATION ERROR] Impossibile aggiornare clip {clip_path.name}: {ex}")
        return False


def audit_recent_submissions(hours_window=4, use_cache=False):
    """
    Controlla lo stato di approvazione su Klippify (accepted / pending / rejected) per tutti i video inviati:
    1. Sincronizza le submission da Klippify (con fallback sicuro alla cache locale se offline).
    2. Collega ogni submission al file MP4 locale, hook, CTA e segmenti tramite published_content.json e clip_metadata.json.
    3. Calcola metriche globali e per campagna (tasso di approvazione, pattern vincenti approvati, diagnosi rifiuti con ai_reasoning).
    4. Salva il report completo in data/approval_audit_report.json per l'Agente AI Director e la Dashboard.
    """
    print(f"\n🔍 [CONTROLLO APPROVAZIONI KLIPPIFY] Verifica stato video inviati (finestra recente: {hours_window}h)...")

    state = load_audit_state()
    now = datetime.now()
    cutoff_time = now - timedelta(hours=hours_window)

    submissions = []
    try:
        submissions = fetch_klippify_submissions(use_cache_if_available=use_cache)
    except Exception as e:
        print(f"[AUDIT WARNING] Impossibile sincronizzare live da Klippify ({e}), uso cache locale se presente.")
        submissions = _load_json_safe(SUBMISSIONS_CACHE_FILE, [])

    if submissions is None:
        submissions = []

    published_records = _load_json_safe(PUBLISHED_CONTENT_FILE, [])
    clip_metadata = _load_json_safe(CLIP_METADATA_FILE, {})

    # Calcola il timestamp dell'ultima approvazione per ciascuna campagna
    latest_accepted_dt_by_camp = {}
    for s in submissions:
        if (s.get("status") or "").lower() == "accepted":
            cid = str(s.get("campaign_id") or s.get("campaign_token") or "unknown")
            dt = _parse_iso_dt(s.get("created_at"), datetime.min)
            if cid not in latest_accepted_dt_by_camp or dt > latest_accepted_dt_by_camp[cid]:
                latest_accepted_dt_by_camp[cid] = dt

    all_accepted = []
    all_pending = []
    all_rejected = []

    recent_accepted = []
    recent_pending = []
    recent_rejections = []

    by_campaign = {}

    for s in submissions:
        created_str = s.get("created_at")
        sub_time = _parse_iso_dt(created_str, now)
        is_recent = sub_time >= cutoff_time
        sub_id = s.get("id")
        status = (s.get("status") or "pending").lower()
        camp_id = str(s.get("campaign_id") or s.get("campaign_token") or "unknown")
        camp_info = get_campaign_cta_and_brief(camp_id)
        camp_name = s.get("campaign_name") or camp_info["campaign_name"]
        ai_reasoning = s.get("ai_reasoning") or ""
        is_ai_verified = bool(s.get("is_ai_verified", False))

        local_match = match_submission_to_local_clip(s, published_records, clip_metadata)

        enriched_sub = {
            "submission_id": sub_id,
            "campaign_id": camp_id,
            "campaign_name": camp_name,
            "post_url": s.get("post_url", ""),
            "status": status,
            "is_ai_verified": is_ai_verified,
            "ai_reasoning": ai_reasoning,
            "views": s.get("views", 0),
            "likes": s.get("likes", 0),
            "earnings": s.get("earnings", 0.0),
            "created_at": created_str,
            "is_recent": is_recent,
            "local_clip": local_match
        }

        if camp_id not in by_campaign:
            by_campaign[camp_id] = {
                "campaign_id": camp_id,
                "campaign_name": camp_name,
                "expected_cta": camp_info["cta_text"],
                "mandatory_mentions": camp_info["mandatory_mentions"],
                "mandatory_hashtags": camp_info["mandatory_hashtags"],
                "total_submitted": 0,
                "accepted_count": 0,
                "pending_count": 0,
                "rejected_count": 0,
                "approval_rate_pct": 0.0,
                "total_views": 0,
                "total_earnings": 0.0,
                "winning_patterns": [],
                "rejection_diagnostics": [],
                "pending_submissions": []
            }

        c_bucket = by_campaign[camp_id]
        c_bucket["total_submitted"] += 1
        c_bucket["total_views"] += int(s.get("views", 0) or 0)
        c_bucket["total_earnings"] = round(c_bucket["total_earnings"] + float(s.get("earnings", 0.0) or 0.0), 4)

        if status == "accepted":
            all_accepted.append(enriched_sub)
            c_bucket["accepted_count"] += 1
            if is_recent:
                recent_accepted.append(enriched_sub)
            if len(c_bucket["winning_patterns"]) < 5:
                c_bucket["winning_patterns"].append({
                    "submission_id": sub_id,
                    "post_url": s.get("post_url", ""),
                    "clip_filename": local_match.get("clip_filename"),
                    "hook_text": local_match.get("hook_text"),
                    "cta_text": local_match.get("cta_text"),
                    "views": s.get("views", 0),
                    "ai_reasoning": ai_reasoning
                })
        elif status == "rejected":
            all_rejected.append(enriched_sub)
            c_bucket["rejected_count"] += 1
            diag = diagnose_rejection_reason(ai_reasoning, camp_info)
            latest_acc_dt = latest_accepted_dt_by_camp.get(camp_id, datetime.min)
            superseded = bool(created_str and latest_acc_dt > sub_time)

            c_bucket["rejection_diagnostics"].append({
                "submission_id": sub_id,
                "post_url": s.get("post_url", ""),
                "created_at": created_str,
                "clip_filename": local_match.get("clip_filename"),
                "hook_text": local_match.get("hook_text"),
                "cta_text": local_match.get("cta_text"),
                "superseded_by_newer_approval": superseded,
                "categories": diag["categories"],
                "ai_reasoning": diag["ai_reasoning"],
                "ai_director_instruction": diag["ai_director_instruction"]
            })

            if superseded and sub_id and sub_id not in state.get("resolved_rejections", []):
                state["resolved_rejections"].append(sub_id)
                if camp_id in state.get("campaigns_needing_attention", {}):
                    del state["campaigns_needing_attention"][camp_id]

            if is_recent or (not superseded and sub_id not in state.get("resolved_rejections", [])):
                recent_rejections.append(enriched_sub)
        else:
            all_pending.append(enriched_sub)
            c_bucket["pending_count"] += 1
            c_bucket["pending_submissions"].append({
                "submission_id": sub_id,
                "post_url": s.get("post_url", ""),
                "created_at": created_str,
                "clip_filename": local_match.get("clip_filename")
            })
            if is_recent:
                recent_pending.append(enriched_sub)

    for cid, c_bucket in by_campaign.items():
        decided = c_bucket["accepted_count"] + c_bucket["rejected_count"]
        if decided > 0:
            c_bucket["approval_rate_pct"] = round((c_bucket["accepted_count"] / decided) * 100.0, 1)
        elif c_bucket["total_submitted"] > 0:
            c_bucket["approval_rate_pct"] = 0.0

    total_subs = len(submissions)
    total_decided = len(all_accepted) + len(all_rejected)
    overall_approval_rate = round((len(all_accepted) / total_decided) * 100.0, 1) if total_decided > 0 else 0.0

    print(f"📊 Riepilogo Globale Sottomissioni Klippify ({total_subs} totali):")
    print(f"   - ✅ Approvati totali: {len(all_accepted)} (Tasso approvazione: {overall_approval_rate}%) | Recenti ({hours_window}h): {len(recent_accepted)}")
    print(f"   - ⏳ In revisione (pending): {len(all_pending)} | Recenti ({hours_window}h): {len(recent_pending)}")
    print(f"   - ❌ Rifiutati attivi da gestire: {len(recent_rejections)} (Totale storico rifiuti: {len(all_rejected)})")

    # 1. VERIFICA EFFICACIA ESPERIMENTO ATTIVO
    active_exp = state.get("active_experiment")
    if active_exp and active_exp.get("status") == "waiting_validation":
        tested_url = active_exp.get("tested_post_url")
        tested_clip = active_exp.get("tested_clip_name")
        camp_id = str(active_exp.get("campaign_id") or "")

        is_validated = False
        for acc in recent_accepted:
            if str(acc.get("campaign_id")) == camp_id:
                if not tested_url or (tested_url in acc.get("post_url", "")):
                    is_validated = True
                    break

        if is_validated and camp_id:
            print(f"\n🎉 [VALIDAZIONE CONFERMATA] L'AI di Klippify ha APPROVATO il video per la campagna '{camp_id}' ('{tested_clip}')!")
            camp_info = get_campaign_cta_and_brief(camp_id)
            avail_clips = get_chronological_available_clips(camp_id)
            propagated = []
            for cl in avail_clips[:6]:
                ok = apply_fix_to_clip(cl, campaign_id=camp_id, brand_cta=camp_info["cta_text"])
                if ok:
                    propagated.append(cl.name)

            state["propagation_history"].append({
                "validated_at": now.strftime("%Y-%m-%d %H:%M:%S"),
                "campaign_id": camp_id,
                "tested_clip": tested_clip,
                "propagated_count": len(propagated),
                "propagated_clips": propagated
            })
            state["active_experiment"] = None
            if camp_id in state.get("campaigns_needing_attention", {}):
                del state["campaigns_needing_attention"][camp_id]

    # 2. GESTIONE DEI NUOVI RIFIUTI PER CAMPAGNA SPECIFICA
    corrective_actions = []
    if recent_rejections:
        print(f"\n⚠️ [ALERT] Rilevati {len(recent_rejections)} video rifiutati dall'AI di Klippify da gestire!")
        for idx, rej in enumerate(recent_rejections, 1):
            sub_id = rej.get("submission_id")
            camp_name = rej.get("campaign_name", "N/D")
            camp_id = str(rej.get("campaign_id") or "unknown")
            post_url = rej.get("post_url", "N/D")
            reason = rej.get("ai_reasoning") or "Nessuna motivazione fornita."
            camp_info = get_campaign_cta_and_brief(camp_id)
            diag = diagnose_rejection_reason(reason, camp_info)

            print(f"\n--- Rifiuto #{idx} [ID: {sub_id}] ---")
            print(f"   Campagna: {camp_name} ({camp_id})")
            print(f"   Link: {post_url}")
            print(f"   Motivo AI Klippify: {reason}")
            print(f"   Direttiva AI Director: {diag['ai_director_instruction']}")

            state.setdefault("campaigns_needing_attention", {})[camp_id] = {
                "campaign_id": camp_id,
                "campaign_name": camp_name,
                "last_rejected_submission_id": sub_id,
                "last_rejected_url": post_url,
                "ai_reasoning": reason,
                "categories": diag["categories"],
                "ai_director_instruction": diag["ai_director_instruction"],
                "expected_cta": camp_info["cta_text"],
                "flagged_at": now.strftime("%Y-%m-%d %H:%M:%S")
            }

            avail_clips = get_chronological_available_clips(camp_id)
            target_clip = avail_clips[0] if avail_clips else None

            if target_clip:
                ok = apply_fix_to_clip(target_clip, campaign_id=camp_id, brand_cta=camp_info["cta_text"])
                if ok:
                    state["active_experiment"] = {
                        "tested_clip_name": target_clip.name,
                        "tested_clip_path": str(target_clip),
                        "tested_post_url": None,
                        "rejection_reason": reason,
                        "campaign_id": camp_id,
                        "status": "waiting_validation",
                        "created_at": now.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    action_desc = (
                        f"Aggiornata la clip '{target_clip.name}' con la CTA della campagna '{camp_name}' "
                        f"('{camp_info['cta_text']}')."
                    )
                else:
                    action_desc = (
                        f"Campagna '{camp_name}' segnalata per l'AI Director: ri-tagliare la prossima clip "
                        f"seguendo la direttiva: {diag['ai_director_instruction']}"
                    )
            else:
                action_desc = (
                    f"Nessuna clip in coda per '{camp_name}'. L'AI Director applicherà la correzione "
                    f"al prossimo taglio: {diag['ai_director_instruction']}"
                )

            corrective_actions.append({
                "submission_id": sub_id,
                "campaign_id": camp_id,
                "campaign_name": camp_name,
                "reason": reason,
                "categories": diag["categories"],
                "ai_director_instruction": diag["ai_director_instruction"],
                "action": action_desc
            })

            if sub_id and sub_id not in state.get("resolved_rejections", []):
                state["resolved_rejections"].append(sub_id)
    else:
        print("✅ [PERFETTO] Nessun nuovo rifiuto irrisolto registrato su Klippify.")

    audit_ts = now.strftime("%Y-%m-%d %H:%M:%S")
    state["last_audit_time"] = audit_ts
    save_audit_state(state)

    report = {
        "status": "success",
        "audit_timestamp": audit_ts,
        "hours_window": hours_window,
        "summary": {
            "total_submissions": total_subs,
            "total_accepted": len(all_accepted),
            "total_pending": len(all_pending),
            "total_rejected": len(all_rejected),
            "overall_approval_rate_pct": overall_approval_rate,
            "recent_accepted_count": len(recent_accepted),
            "recent_pending_count": len(recent_pending),
            "recent_rejections_count": len(recent_rejections)
        },
        "by_campaign": by_campaign,
        "campaigns_needing_attention": state.get("campaigns_needing_attention", {}),
        "corrective_actions": corrective_actions,
        "recent_accepted_count": len(recent_accepted),
        "recent_pending_count": len(recent_pending),
        "recent_rejections_count": len(recent_rejections)
    }
    save_approval_report(report)
    return report


if __name__ == "__main__":
    audit_recent_submissions(hours_window=4)
