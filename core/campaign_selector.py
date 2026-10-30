import paths
import json
import re
import sys
from datetime import datetime
from pathlib import Path
import rejection_auditor

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = paths.PROJECT_ROOT
RANKED_FILE = BASE_DIR / "campaigns_ranked.json"
CLASSIFIED_FILE = BASE_DIR / "active_campaigns_classified.json"
DETAILED_FILE = BASE_DIR / "active_campaigns_detailed.json"
SELECTED_FILE = BASE_DIR / "campagne_selezionate.json"
SCHEDULES_FILE = BASE_DIR / "campaign_schedules.json"
SOURCES_FILE = BASE_DIR / "campaign_sources.json"
AI_DECISIONS_FILE = BASE_DIR / "ai_campaign_decisions.json"
PORTFOLIO_REPORT_FILE = BASE_DIR / "campaign_portfolio_plan.json"

MAX_DAILY_UPLOADS_PER_ACCOUNT = 3
GLOBAL_DAILY_SLOTS = ["13:00", "17:30", "21:00"]
SCALING_SLOTS = ["13:00", "21:00"]
MIN_BUDGET_REMAINING_USD = 35.0       # sotto questa soglia la campagna è considerata SENZA SOLDI
MAX_BUDGET_PROGRESS_PCT = 95.0        # oltre il 95% di budget speso non si lavora più sulla campagna


def has_sufficient_budget(camp: dict) -> tuple[bool, str]:
    """Controllo budget: True solo se la campagna ha ancora soldi reali da pagare."""
    try:
        rem = float(camp.get("budget_remaining") or 0.0)
    except Exception:
        rem = 0.0
    try:
        tot = float(camp.get("budget_total") or 0.0)
        spent = float(camp.get("budget_spent") or 0.0)
    except Exception:
        tot, spent = 0.0, 0.0
    pct = (spent / tot * 100.0) if tot > 0 else 0.0
    if camp.get("budget_exhausted") is True:
        return False, "Budget segnalato come esaurito"
    if rem < MIN_BUDGET_REMAINING_USD:
        return False, f"Budget residuo insufficiente (${rem:.2f} < ${MIN_BUDGET_REMAINING_USD:.0f})"
    if pct >= MAX_BUDGET_PROGRESS_PCT:
        return False, f"Budget quasi esaurito ({pct:.1f}% speso)"
    return True, f"Budget OK (${rem:.2f} residui)"
TESTING_SLOTS = ["17:30"]

KNOWN_YOUTUBE_SOURCES = {
    "6a71c6f7245627c68999eae2": ["https://www.youtube.com/@SaraDizdariEcommerce"],
    "6a91676284a29ab01b754c33": ["https://www.youtube.com/@MarcoCappelli", "https://www.youtube.com/@AlexTheory"],
    "6a719c80a2d57190f5d7a38b": ["https://www.youtube.com/@AlexTheory"],
    "6a7628ca922613d297f2e2c5": ["https://www.youtube.com/@AldoMasolo"],
    "6a64cf756cdfd98478f11f28": ["https://www.youtube.com/@MarcoCappelli"],
    "6a426231e6a21896f769dc80": ["https://www.youtube.com/@RiccardoDose"],
}


def _load_json_safe(file_path: Path, default_val):
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return default_val


def _save_json_safe(file_path: Path, data):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[CAMPAIGN SELECTOR ERROR] Impossibile salvare {file_path.name}: {e}")


def load_ai_campaign_decisions() -> dict:
    data = _load_json_safe(AI_DECISIONS_FILE, {})
    if isinstance(data, dict):
        return data.get("campaigns", {})
    return {}


def _is_clipping_compatible(camp: dict, classified_map: dict, sources_map: dict, ai_decisions: dict = None) -> tuple[bool, list[str]]:
    """
    Determina se una campagna Klippify è fattibile per il Clipping AI 9:16:
    1. Controlla prima la valutazione esplicita dell'Agente AI in data/ai_campaign_decisions.json.
    2. Controlla disponibilità di video sorgente (YouTube, Drive, clip locali).
    3. Esclude campagne che richiedono riprese fisiche in location esterna senza materiale video.
    """
    cid = str(camp.get("id") or camp.get("campaign_token") or "")
    ai_dec = (ai_decisions or {}).get(cid, {})
    if "feasible" in ai_dec:
        if not ai_dec["feasible"]:
            return False, [ai_dec.get("ai_feasibility_notes") or "Scartata dall'Agente AI per bassa fattibilità"]
        notes = ai_dec.get("ai_feasibility_notes")
        return True, [notes] if notes else ["Certificata fattibile dall'Agente AI"]

    name = (camp.get("name") or "").strip()
    brand = (camp.get("brand") or "").strip()
    desc = (camp.get("description") or "").strip()
    rules_txt = " ".join(camp.get("rules") or [])
    full_text = f"{name} {brand} {desc} {rules_txt}".lower()

    reasons = []
    cl_entry = classified_map.get(cid, {})

    clips_dir = BASE_DIR / "generated_videos" / cid / "clips"
    raw_dir = BASE_DIR / "clipping_sources" / cid
    has_local_files = (clips_dir.exists() and any(clips_dir.glob("*.mp4"))) or (
        raw_dir.exists() and any(raw_dir.glob("*.mp4"))
    )
    if has_local_files:
        reasons.append("Video sorgenti o clip 9:16 già presenti su disco")

    has_yt = bool(
        cid in KNOWN_YOUTUBE_SOURCES
        or any("youtube" in str(u).lower() or "youtu.be" in str(u).lower() for u in (sources_map.get(cid, {}).get("sources") or []))
    )
    has_drive = bool(cl_entry.get("drive_links"))
    if has_yt:
        reasons.append("Canale YouTube ufficiale collegato per download automatico")
    elif has_drive:
        reasons.append("Cartella Drive/Asset collegata")

    clipping_kws = [
        "clip", "podcast", "intervist", "spezzon", "youtube", "episod",
        "bilancio", "academy", "talk", "theory", "gurulandia",
        "what's next", "hospitality", "masolo", "dizdari", "dose", "collecto"
    ]
    matched_kws = [k for k in clipping_kws if k in full_text]
    if matched_kws:
        reasons.append(f"Format adatto a clipping ({', '.join(matched_kws[:3])})")

    physical_only_kws = ["lago maggiore", "peschiera del garda", "dormire sotto le stelle", "film anything, just show the site"]
    if any(pk in full_text for pk in physical_only_kws) and not has_local_files and not has_yt:
        return False, ["Richiede riprese fisiche o screen recording manuale non automatizzabile"]

    is_ok = bool(has_local_files or has_yt or has_drive or matched_kws or cl_entry.get("category") == "CLIPPING")
    return is_ok, reasons


def compute_promising_score(camp: dict, classified_map: dict, sources_map: dict, ai_decisions: dict = None) -> dict:
    """
    Calcola il Promising Score combinando la valutazione dell'Agente AI (ai_campaign_decisions.json)
    con i parametri economici e di trazione reali su Klippify:
    - Valore Atteso per Creator (views_per_creator / 1000 * payout_per_1k)
    - Trazione organica su Klippify (views medie per creator)
    - Automazione Fonti Video (Canale YouTube / query di ricerca AI / clip pronte su disco)
    - Capienza del budget residuo ($) e affinità lingua italiana
    """
    cid = str(camp.get("id") or camp.get("campaign_token") or "")
    budget_rem = float(camp.get("budget_remaining") or 0.0)
    payout = float(camp.get("payout_per_1k_views") or 0.5)
    total_views = int(camp.get("total_views") or 0)
    creators = max(1, int(camp.get("creators_count") or 1))
    section = (camp.get("section") or "").strip().lower()
    status = (camp.get("status") or "Active").strip().lower()
    desc_lower = f"{camp.get('name', '')} {camp.get('description', '')}".lower()

    budget_ok, _budget_msg = has_sufficient_budget(camp)
    if not budget_ok or section in ["passate", "in pausa", "rifiutate"] or status != "active":
        return {
            "promising_score": -1000.0,
            "is_eligible": False,
            "views_per_creator": 0.0,
            "expected_rev_per_creator": 0.0,
            "reasons": [_budget_msg if not budget_ok else "Campagna non attiva su Klippify"]
        }

    is_clip_ok, clip_reasons = _is_clipping_compatible(camp, classified_map, sources_map, ai_decisions=ai_decisions)
    if not is_clip_ok:
        return {
            "promising_score": -500.0,
            "is_eligible": False,
            "views_per_creator": 0.0,
            "expected_rev_per_creator": 0.0,
            "reasons": clip_reasons
        }

    views_per_creator = round(total_views / creators, 1)
    expected_rev_per_creator = round((views_per_creator / 1000.0) * payout, 2)

    rev_pts = min(expected_rev_per_creator, 15.0) * 90.0
    traction_pts = min(views_per_creator, 15000.0) * 0.08
    budget_pts = min(budget_rem, 1200.0) * 0.25

    readiness_pts = 0.0
    clips_dir = BASE_DIR / "generated_videos" / cid / "clips"
    raw_dir = BASE_DIR / "clipping_sources" / cid
    if clips_dir.exists() and any(clips_dir.glob("*.mp4")):
        readiness_pts += 450.0
    elif raw_dir.exists() and any(raw_dir.glob("*.mp4")):
        readiness_pts += 300.0

    ai_dec = (ai_decisions or {}).get(cid, {})
    if ai_dec.get("feasible") and ai_dec.get("recommended_stage") in ["scaling", "testing"]:
        readiness_pts += 300.0

    if cid in KNOWN_YOUTUBE_SOURCES or cid in sources_map or ai_dec.get("source_urls"):
        readiness_pts += 450.0
    elif cid in classified_map:
        readiness_pts += 100.0

    english_markers = ["this campaign is for", "english", "- eng", "us audience", "woodworking brand"]
    is_english = any(em in desc_lower for em in english_markers)
    lang_pts = -250.0 if is_english else 150.0

    total_score = round(rev_pts + traction_pts + budget_pts + readiness_pts + lang_pts, 1)
    return {
        "promising_score": total_score,
        "is_eligible": True,
        "views_per_creator": views_per_creator,
        "expected_rev_per_creator": expected_rev_per_creator,
        "reasons": clip_reasons
    }


def evaluate_and_select_campaigns(
    max_scaling: int = 3,
    max_testing: int = 3,
    min_test_submissions: int = 3,
    min_approval_rate_pct: float = 50.0,
    min_avg_views_to_scale: float = 80.0,
    min_peak_views_to_scale: int = 200,
    apply_changes: bool = True
) -> dict:
    """
    Motore AI di gestione portafoglio campagne Klippify (Seleziona -> Testa -> Spingi Vincenti):
    1. Legge le decisioni di fattibilità e ricerca fonti dell'Agente AI (data/ai_campaign_decisions.json).
    2. Analizza le performance reali delle campagne già testate (approvazioni Klippify + views TikTok).
    3. Promuove in SCALING (6 slot/giorno) solo le campagne che vanno bene (alta approvazione + buone views).
    4. Mette in PAUSA (DROPPED_UNDERPERFORMING) le campagne che dopo >= 3 video hanno troppi rifiuti o poche views.
    5. Seleziona automaticamente dal catalogo Klippify le campagne più promettenti per riempire gli slot di TESTING (2 slot/giorno).
    """
    print("\n🧠 [AI CAMPAIGN SELECTOR] Valutazione portafoglio campagne Klippify (Seleziona -> Testa -> Spingi Vincenti)...")

    ranked_camps = _load_json_safe(RANKED_FILE, [])
    classified_list = _load_json_safe(CLASSIFIED_FILE, [])
    detailed_list = _load_json_safe(DETAILED_FILE, [])
    sources_map = _load_json_safe(SOURCES_FILE, {})
    schedules = _load_json_safe(SCHEDULES_FILE, {})
    selected_ids = _load_json_safe(SELECTED_FILE, [])
    ai_decisions = load_ai_campaign_decisions()

    audit_report = _load_json_safe(BASE_DIR / "approval_audit_report.json", {})
    if not audit_report or "by_campaign" not in audit_report:
        try:
            audit_report = rejection_auditor.audit_recent_submissions(hours_window=24, use_cache=True)
        except Exception:
            audit_report = {"by_campaign": {}}

    by_camp_perf = audit_report.get("by_campaign", {})
    submissions_list = _load_json_safe(BASE_DIR / "klippify_submissions.json", [])

    views_stats_by_camp = {}
    for s in submissions_list:
        cid = str(s.get("campaign_id") or s.get("campaign_token") or "")
        if not cid:
            continue
        v = int(s.get("views") or 0)
        bucket = views_stats_by_camp.setdefault(cid, {"views_list": [], "max_views": 0, "total_views": 0})
        bucket["views_list"].append(v)
        bucket["total_views"] += v
        if v > bucket["max_views"]:
            bucket["max_views"] = v

    classified_map = {}
    for c in classified_list + detailed_list:
        cid = str(c.get("id") or c.get("campaign_token") or c.get("campaign_id") or "")
        if cid:
            classified_map[cid] = c

    all_camps_map = {}
    for c in ranked_camps:
        cid = str(c.get("id") or c.get("campaign_token") or "")
        if cid:
            all_camps_map[cid] = dict(c)

    has_live_ranked_catalog = len(ranked_camps) > 0
    enrolled_classified_ids = set(classified_map.keys())
    submitted_camp_ids = {
        str(s.get("campaign_id") or s.get("campaign_token") or "")
        for s in submissions_list
        if s.get("campaign_id") or s.get("campaign_token")
    }

    for cid, cl in classified_map.items():
        if cid not in all_camps_map:
            # Se abbiamo il catalogo live di Klippify (ranked_camps) e questa campagna non è più presente,
            # significa che è terminata/scaduta su Klippify!
            all_camps_map[cid] = {
                "id": cid,
                "campaign_token": cid,
                "name": cl.get("name") or cl.get("campaign_name") or cid,
                "brand": cl.get("brand") or "",
                "section": "Passate" if has_live_ranked_catalog else "Iscritte",
                "status": "Ended" if has_live_ranked_catalog else "Active",
                "budget_remaining": 0.0 if has_live_ranked_catalog else (cl.get("budget_remaining") or 100.0),
                "payout_per_1k_views": cl.get("payout_per_1k_views") or cl.get("payout_per_1k") or 0.5,
                "total_views": 50000,
                "creators_count": 50,
                "description": cl.get("description") or "",
                "rules": cl.get("rules") or [],
                "mandatory_hashtags": cl.get("mandatory_hashtags") or [],
                "mandatory_mentions": cl.get("mandatory_mentions") or []
            }

    scaling_campaigns = []
    testing_campaigns = []
    dropped_campaigns = []
    depleted_campaigns = []
    candidate_pool = []

    for cid, camp in all_camps_map.items():
        cname = camp.get("name") or cid
        budget_rem = float(camp.get("budget_remaining") or 0.0)
        payout = float(camp.get("payout_per_1k_views") or 0.5)
        ai_dec = ai_decisions.get(cid, {})

        prom_eval = compute_promising_score(camp, classified_map, sources_map, ai_decisions=ai_decisions)
        prom_score = prom_eval["promising_score"]

        perf = by_camp_perf.get(cid, {})
        total_sub = int(perf.get("total_submitted") or 0)
        acc_cnt = int(perf.get("accepted_count") or 0)
        rej_cnt = int(perf.get("rejected_count") or 0)
        pend_cnt = int(perf.get("pending_count") or 0)
        decided_cnt = acc_cnt + rej_cnt
        app_rate = float(perf.get("approval_rate_pct") or 0.0)

        v_stats = views_stats_by_camp.get(cid, {"views_list": [], "max_views": 0, "total_views": 0})
        my_total_views = v_stats["total_views"]
        my_max_views = v_stats["max_views"]
        my_avg_views = round(my_total_views / total_sub, 1) if total_sub > 0 else 0.0

        clips_dir = BASE_DIR / "generated_videos" / cid / "clips"
        pub_clips_set = set(schedules.get(cid, {}).get("published_clips", []))
        virgin_clips = [
            f.name for f in (clips_dir.glob("*.mp4") if clips_dir.exists() else [])
            if f.name not in pub_clips_set and not f.name.startswith("temp_")
        ]

        recommended_sources = (
            ai_dec.get("source_urls")
            or sources_map.get(cid, {}).get("sources")
            or KNOWN_YOUTUBE_SOURCES.get(cid, [])
        )
        search_queries = ai_dec.get("search_queries") or [f"{cname} {camp.get('brand', '')} podcast intervista".strip()]
        selection_criteria = ai_dec.get("video_selection_criteria") or (
            "Scegli video lunghi 16:9 (3-60 min) pertinenti al brief della campagna, non ancora presenti in downloaded_sources_history.json."
        )

        section_raw = (camp.get("section") or "").strip()
        status_raw = (camp.get("status") or "Active").strip()
        is_klippify_active = (
            status_raw.lower() == "active"
            and section_raw.lower() not in ["passate", "in pausa", "rifiutate", "concluse", "scadute", "ended"]
            and budget_rem >= 35.0
            and str(camp.get("budget_progress_percent") or "").strip() not in ["100%", "100.0%"]
        )
        is_user_enrolled = bool(
            section_raw.lower() == "iscritte"
            or cid in enrolled_classified_ids
            or cid in submitted_camp_ids
            or schedules.get(cid, {}).get("user_confirmed_enrolled") is True
        )
        requires_user_activation = bool(is_klippify_active and not is_user_enrolled)
        klippify_url = camp.get("campaign_url") or f"https://app.klippify.com/campaigns/{cid}"

        entry = {
            "campaign_id": cid,
            "campaign_name": cname,
            "brand": camp.get("brand") or "",
            "klippify_url": klippify_url,
            "klippify_section": section_raw or "Nuove",
            "klippify_status": status_raw,
            "is_klippify_active": is_klippify_active,
            "is_user_enrolled": is_user_enrolled,
            "requires_user_activation": requires_user_activation,
            "budget_remaining": budget_rem,
            "payout_per_1k_views": payout,
            "views_per_creator_klippify": prom_eval["views_per_creator"],
            "expected_rev_per_creator": prom_eval.get("expected_rev_per_creator", 0.0),
            "promising_score": prom_score,
            "reasons": prom_eval["reasons"],
            "recommended_sources": recommended_sources,
            "search_queries": search_queries,
            "video_selection_criteria": selection_criteria,
            "my_submitted_count": total_sub,
            "my_accepted_count": acc_cnt,
            "my_rejected_count": rej_cnt,
            "my_pending_count": pend_cnt,
            "my_approval_rate_pct": app_rate,
            "my_total_views": my_total_views,
            "my_avg_views": my_avg_views,
            "my_max_views": my_max_views,
            "virgin_clips_ready": len(virgin_clips),
            "virgin_clip_Showcases": virgin_clips[:5],
            "lifecycle_stage": "candidate",
            "decision_reason": ""
        }

        if not prom_eval["is_eligible"]:
            entry["lifecycle_stage"] = "depleted"
            entry["decision_reason"] = "; ".join(prom_eval["reasons"])
            depleted_campaigns.append(entry)
            continue

        if decided_cnt >= min_test_submissions:
            is_approved_ok = app_rate >= min_approval_rate_pct
            is_views_ok = (my_avg_views >= min_avg_views_to_scale) or (my_max_views >= min_peak_views_to_scale)

            if is_approved_ok and is_views_ok:
                entry["lifecycle_stage"] = "scaling"
                entry["decision_reason"] = (
                    f"VINCENTE: Tasso approvazione {app_rate}% ({acc_cnt}/{decided_cnt}) e picco di {my_max_views} views "
                    f"(media {my_avg_views} views/video). Spinta in SCALING prioritario (fino a 2 slot/giorno su 3 max account TikTok)."
                )
                scaling_campaigns.append(entry)
            else:
                entry["lifecycle_stage"] = "dropped_underperforming"
                fail_reasons = []
                if not is_approved_ok:
                    fail_reasons.append(f"tasso approvazione troppo basso ({app_rate}%)")
                if not is_views_ok:
                    fail_reasons.append(f"views insufficienti dopo {decided_cnt} video (media {my_avg_views}, max {my_max_views})")
                entry["decision_reason"] = (
                    f"FERMATA DOPO TEST: {', '.join(fail_reasons)}. Sostituita con campagne più promettenti."
                )
                dropped_campaigns.append(entry)
            continue

        if total_sub > 0 or len(virgin_clips) > 0 or ai_dec.get("recommended_stage") == "testing":
            entry["lifecycle_stage"] = "testing"
            entry["decision_reason"] = (
                f"IN TEST ATTIVO: {total_sub}/{min_test_submissions} clip inviate finora, "
                f"{len(virgin_clips)} clip 9:16 pronte in magazzino (Promising Score: {prom_score})."
            )
            testing_campaigns.append(entry)
        else:
            candidate_pool.append(entry)

    scaling_campaigns.sort(key=lambda x: (x["my_max_views"], x["my_approval_rate_pct"], x["promising_score"]), reverse=True)
    scaling_campaigns = scaling_campaigns[:max_scaling]

    candidate_pool.sort(key=lambda x: x["promising_score"], reverse=True)
    testing_campaigns.sort(key=lambda x: (x["virgin_clips_ready"] > 0, x["promising_score"]), reverse=True)
    if len(testing_campaigns) > max_testing:
        overflow = testing_campaigns[max_testing:]
        testing_campaigns = testing_campaigns[:max_testing]
        for ov in overflow:
            ov["lifecycle_stage"] = "candidate"
            candidate_pool.insert(0, ov)

    while len(testing_campaigns) < max_testing and candidate_pool:
        best_cand = candidate_pool.pop(0)
        best_cand["lifecycle_stage"] = "testing"
        best_cand["decision_reason"] = (
            f"SELEZIONATA PER TEST: Promising Score {best_cand['promising_score']} "
            f"({best_cand['views_per_creator_klippify']} views/creator, ${best_cand['payout_per_1k_views']}/1k, "
            f"budget ${best_cand['budget_remaining']}). Inserita nel pool di TEST AI (max 3 video/giorno globali per account TikTok)."
        )
        testing_campaigns.append(best_cand)

    next_clipping_priorities = []
    for camp_entry in scaling_campaigns + testing_campaigns:
        if camp_entry["virgin_clips_ready"] < 2:
            next_clipping_priorities.append({
                "campaign_id": camp_entry["campaign_id"],
                "campaign_name": camp_entry["campaign_name"],
                "lifecycle_stage": camp_entry["lifecycle_stage"],
                "virgin_clips_ready": camp_entry["virgin_clips_ready"],
                "recommended_sources": camp_entry["recommended_sources"],
                "search_queries": camp_entry["search_queries"],
                "video_selection_criteria": camp_entry["video_selection_criteria"],
                "reason": (
                    f"Campagna in {camp_entry['lifecycle_stage'].upper()} con sole "
                    f"{camp_entry['virgin_clips_ready']} clip pronte in magazzino."
                )
            })

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Identifica le campagne selezionate per il TEST che richiedono prima l'attivazione manuale dell'utente su Klippify
    campaigns_requiring_activation = []
    for c_item in scaling_campaigns + testing_campaigns:
        if c_item.get("requires_user_activation"):
            warn_msg = (
                f"⚠️ AZIONE RICHIESTA SU KLIPPIFY: Devi prima attivare/iscriverti alla campagna "
                f"'{c_item['campaign_name']}' su {c_item['klippify_url']} altrimenti Klippify non permette di caricare i suoi video!"
            )
            c_item["activation_warning"] = warn_msg
            c_item["decision_reason"] = f"[DA ATTIVARE SU KLIPPIFY] {c_item['decision_reason']} -> Attivala su Klippify per sbloccare l'upload automatico."
            campaigns_requiring_activation.append({
                "campaign_id": c_item["campaign_id"],
                "campaign_name": c_item["campaign_name"],
                "brand": c_item["brand"],
                "lifecycle_stage": c_item["lifecycle_stage"],
                "klippify_url": c_item["klippify_url"],
                "virgin_clips_ready": c_item["virgin_clips_ready"],
                "message": warn_msg
            })
        else:
            c_item["activation_warning"] = None

    # Allocazione rigorosa degli slot giornalieri: MAX 3 VIDEO/GIORNO IN TOTALE PER ACCOUNT TIKTOK
    slot_allocations = {}
    if scaling_campaigns and testing_campaigns:
        if len(scaling_campaigns) == 1:
            slot_allocations[scaling_campaigns[0]["campaign_id"]] = ["13:00", "21:00"]
        else:
            slot_allocations[scaling_campaigns[0]["campaign_id"]] = ["13:00"]
            slot_allocations[scaling_campaigns[1]["campaign_id"]] = ["21:00"]
        # Assegna lo slot di test 17:30 prioritariamente a una campagna già iscritta, o prenota 17:30 in attesa di attivazione
        enrolled_testing = [t for t in testing_campaigns if t.get("is_user_enrolled")]
        chosen_test = enrolled_testing[0] if enrolled_testing else testing_campaigns[0]
        slot_allocations[chosen_test["campaign_id"]] = ["17:30"]
        for extra_t in testing_campaigns:
            if extra_t["campaign_id"] != chosen_test["campaign_id"]:
                slot_allocations[extra_t["campaign_id"]] = []
    elif scaling_campaigns and not testing_campaigns:
        if len(scaling_campaigns) == 1:
            slot_allocations[scaling_campaigns[0]["campaign_id"]] = list(GLOBAL_DAILY_SLOTS)
        else:
            slot_allocations[scaling_campaigns[0]["campaign_id"]] = ["13:00", "21:00"]
            slot_allocations[scaling_campaigns[1]["campaign_id"]] = ["17:30"]
    elif testing_campaigns and not scaling_campaigns:
        if len(testing_campaigns) == 1:
            slot_allocations[testing_campaigns[0]["campaign_id"]] = list(GLOBAL_DAILY_SLOTS)
        elif len(testing_campaigns) == 2:
            slot_allocations[testing_campaigns[0]["campaign_id"]] = ["13:00", "21:00"]
            slot_allocations[testing_campaigns[1]["campaign_id"]] = ["17:30"]
        else:
            for idx, t_c in enumerate(testing_campaigns[:3]):
                slot_allocations[t_c["campaign_id"]] = [GLOBAL_DAILY_SLOTS[idx]]
            for extra_t in testing_campaigns[3:]:
                slot_allocations[extra_t["campaign_id"]] = []

    total_allocated_slots = 0
    for c_item in scaling_campaigns + testing_campaigns:
        c_slots = slot_allocations.get(c_item["campaign_id"], [])
        c_item["daily_slots"] = c_slots
        c_item["daily_target_count"] = len(c_slots)
        total_allocated_slots += len(c_slots)
        if c_item["lifecycle_stage"] == "testing" and not c_slots and not c_item.get("requires_user_activation"):
            c_item["decision_reason"] += " [In coda di rotazione: attende il completamento dello slot di test giornaliero per rispettare il limite di max 3 video/giorno su TikTok]." 

    if apply_changes:
        active_portfolio_ids = [c["campaign_id"] for c in (scaling_campaigns + testing_campaigns)]
        dropped_or_depleted_ids = {c["campaign_id"] for c in (dropped_campaigns + depleted_campaigns)}
        merged_selected = list(active_portfolio_ids)
        for old_id in selected_ids:
            if old_id not in merged_selected and old_id not in dropped_or_depleted_ids:
                merged_selected.append(old_id)
        _save_json_safe(SELECTED_FILE, merged_selected)

        sources_changed = False
        for c_entry in scaling_campaigns + testing_campaigns:
            cid = c_entry["campaign_id"]
            rec_urls = c_entry.get("recommended_sources") or []
            if cid not in sources_map and rec_urls:
                sources_map[cid] = {
                    "sources": rec_urls,
                    "auto_download": True,
                    "updated_at": now_str
                }
                sources_changed = True
        if sources_changed:
            _save_json_safe(SOURCES_FILE, sources_map)

        for s_camp in scaling_campaigns:
            cid = s_camp["campaign_id"]
            assigned_times = s_camp.get("daily_slots", SCALING_SLOTS)
            sched = schedules.get(cid, {"published_clips": []})
            pub_list = sched.get("published_clips", [])
            v_clips = s_camp.get("virgin_clip_Showcases", [])
            slots = []
            for idx, t_str in enumerate(assigned_times):
                vid_name = v_clips[idx] if idx < len(v_clips) else ""
                slots.append({"time": t_str, "video": vid_name})
            sched.update({
                "target_count": len(assigned_times),
                "slots": slots,
                "autopilot_enabled": len(assigned_times) > 0,
                "is_paused": False,
                "is_ended": False,
                "lifecycle_stage": "scaling",
                "decision_reason": s_camp["decision_reason"],
                "published_clips": pub_list,
                "updated_at": now_str
            })
            schedules[cid] = sched

        for t_camp in testing_campaigns:
            cid = t_camp["campaign_id"]
            assigned_times = t_camp.get("daily_slots", [])
            sched = schedules.get(cid, {"published_clips": []})
            pub_list = sched.get("published_clips", [])
            v_clips = t_camp.get("virgin_clip_Showcases", [])
            slots = []
            for idx, t_str in enumerate(assigned_times):
                vid_name = v_clips[idx] if idx < len(v_clips) else ""
                slots.append({"time": t_str, "video": vid_name})
            needs_act = bool(t_camp.get("requires_user_activation"))
            sched.update({
                "target_count": max(1, len(assigned_times)),
                "slots": slots,
                "autopilot_enabled": (len(assigned_times) > 0) and (not needs_act),
                "waiting_klippify_activation": needs_act,
                "klippify_url": t_camp.get("klippify_url"),
                "is_paused": False,
                "is_ended": False,
                "lifecycle_stage": "testing",
                "decision_reason": t_camp["decision_reason"],
                "published_clips": pub_list,
                "updated_at": now_str
            })
            schedules[cid] = sched

        for d_camp in dropped_campaigns:
            cid = d_camp["campaign_id"]
            if cid in schedules:
                schedules[cid]["autopilot_enabled"] = False
                schedules[cid]["is_paused"] = True
                schedules[cid]["lifecycle_stage"] = "dropped_underperforming"
                schedules[cid]["decision_reason"] = d_camp["decision_reason"]
                schedules[cid]["updated_at"] = now_str

        for dep_camp in depleted_campaigns:
            cid = dep_camp["campaign_id"]
            if cid in schedules:
                schedules[cid]["autopilot_enabled"] = False
                schedules[cid]["is_ended"] = True
                schedules[cid]["lifecycle_stage"] = "depleted"
                schedules[cid]["decision_reason"] = dep_camp["decision_reason"]
                schedules[cid]["updated_at"] = now_str

        _save_json_safe(SCHEDULES_FILE, schedules)

    plan = {
        "status": "success",
        "evaluated_at": now_str,
        "summary": {
            "max_daily_uploads_per_account": MAX_DAILY_UPLOADS_PER_ACCOUNT,
            "global_daily_slots": GLOBAL_DAILY_SLOTS,
            "total_daily_slots_allocated": total_allocated_slots,
            "scaling_count": len(scaling_campaigns),
            "testing_count": len(testing_campaigns),
            "requires_user_activation_count": len(campaigns_requiring_activation),
            "dropped_underperforming_count": len(dropped_campaigns),
            "candidate_pool_count": len(candidate_pool),
            "needs_clipping_count": len(next_clipping_priorities)
        },
        "campaigns_requiring_user_activation": campaigns_requiring_activation,
        "scaling_campaigns": scaling_campaigns,
        "testing_campaigns": testing_campaigns,
        "dropped_campaigns": dropped_campaigns,
        "top_candidates_reserve": candidate_pool[:8],
        "next_clipping_priorities": next_clipping_priorities
    }

    _save_json_safe(PORTFOLIO_REPORT_FILE, plan)

    print(f"🚀 Campagne VINCENTI in SCALING (Max {MAX_DAILY_UPLOADS_PER_ACCOUNT} video/giorno totali per account TikTok): {len(scaling_campaigns)}")
    for c in scaling_campaigns:
        print(f"   - [{c['campaign_id']}] {c['campaign_name']} -> {c['decision_reason']}")

    print(f"🧪 Campagne PROMETTENTI in TESTING (Rotazione slot di test): {len(testing_campaigns)}")
    for c in testing_campaigns:
        print(f"   - [{c['campaign_id']}] {c['campaign_name']} -> {c['decision_reason']}")

    if dropped_campaigns:
        print(f"⏸️ Campagne FERMATE (Sotto-performanti): {len(dropped_campaigns)}")
        for c in dropped_campaigns:
            print(f"   - [{c['campaign_id']}] {c['campaign_name']} -> {c['decision_reason']}")

    if campaigns_requiring_activation:
        print(f"\n⚠️ [AZIONE RICHIESTA ALL'UTENTE SU KLIPPIFY] ({len(campaigns_requiring_activation)} campagne in TEST da attivare):")
        for act in campaigns_requiring_activation:
            print(f"   👉 DEVI ATTIVARE SU KLIPPIFY: {act['campaign_name']} ({act['campaign_id']}) -> {act['klippify_url']}")
            print(f"      (Upload bloccato finché non clicchi 'Partecipa' su Klippify; clip già pronte in magazzino: {act['virgin_clips_ready']})")

    if next_clipping_priorities:
        print(f"🎬 Priorità di Taglio per l'AI Director ({len(next_clipping_priorities)} campagne da rifornire):")
        for p in next_clipping_priorities:
            print(f"   - [{p['lifecycle_stage'].upper()}] {p['campaign_name']} ({p['campaign_id']}) | Clip pronte: {p['virgin_clips_ready']}")

    return plan


if __name__ == "__main__":
    evaluate_and_select_campaigns()
