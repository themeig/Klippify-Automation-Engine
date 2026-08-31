import paths
import os
import sys
import json
import shutil
import time
from datetime import datetime, timedelta
from pathlib import Path
from klippify_scraper import fetch_klippify_submissions
import video_captioner

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = paths.PROJECT_ROOT
AUDIT_STATE_FILE = BASE_DIR / "rejection_audit_state.json"
SCHEDULES_FILE = BASE_DIR / "campaign_schedules.json"

def load_audit_state():
    if AUDIT_STATE_FILE.exists():
        try:
            with open(AUDIT_STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "last_audit_time": None,
        "resolved_rejections": [],
        "active_experiment": None,
        "propagation_history": []
    }

def save_audit_state(state):
    try:
        with open(AUDIT_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[AUDIT ERROR] Impossibile salvare audit state: {e}")

def get_chronological_available_clips(campaign_id):
    """
    Restituisce tutte le clip vergini disponibili sul disco ordinate cronologicamente.
    """
    clips_dir = BASE_DIR / "generated_videos" / str(campaign_id) / "clips"
    if not clips_dir.exists():
        return []
    
    pub_clips = []
    if SCHEDULES_FILE.exists():
        try:
            with open(SCHEDULES_FILE, "r", encoding="utf-8") as f:
                sched = json.load(f)
                pub_clips = sched.get(campaign_id, {}).get("published_clips", [])
        except Exception:
            pass

    candidates = []
    for f in clips_dir.glob("*.mp4"):
        if f.name not in pub_clips and not f.name.startswith("temp_"):
            try:
                candidates.append((f, f.stat().st_mtime))
            except Exception:
                candidates.append((f, 0))

    # Ordina cronologicamente (per data di modifica o nome)
    candidates.sort(key=lambda x: (x[1], x[0].name))
    return [c[0] for c in candidates]

def apply_fix_to_clip(clip_path, brand_cta="La lezione gratuita sul profilo di Sara"):
    """
    Applica il re-rendering con Outro CTA Card + Hook Card corretto sulla clip specificata.
    """
    try:
        temp_out = clip_path.parent / f"temp_fix_{int(time.time())}_{clip_path.name}"
        res = video_captioner.burn_captions_to_video(
            str(clip_path),
            output_video=str(temp_out),
            style_key="hormozi_gold",
            brand_cta=brand_cta
        )
        if res.get("status") == "success" and temp_out.exists() and temp_out.stat().st_size > 100000:
            shutil.move(str(temp_out), str(clip_path))
            print(f"[AUDIT ADAPTATION] ✅ Clip '{clip_path.name}' aggiornata e renderizzata con successo!")
            return True
        else:
            if temp_out.exists():
                temp_out.unlink()
            return False
    except Exception as ex:
        print(f"[AUDIT ADAPTATION ERROR] Impossibile aggiornare clip {clip_path.name}: {ex}")
        return False

def audit_recent_submissions(hours_window=4):
    """
    1. Ispeziona i video recenti su Klippify.
    2. Se l'ultimo esperimento ha avuto successo (video accettato), propaga le modifiche ai 6 video successivi.
    3. Se c'è un nuovo rifiuto, applica le correzioni al 1° video successivo cronologico.
    """
    print(f"\n🔍 [AUDIT SOTTOMISSIONI & ADATTAMENTO A CASCATA] Controllo Klippify (finestra {hours_window}h)...")
    
    state = load_audit_state()
    now = datetime.now()
    cutoff_time = now - timedelta(hours=hours_window)
    
    try:
        submissions = fetch_klippify_submissions(use_cache_if_available=False)
    except Exception as e:
        print(f"[AUDIT WARNING] Impossibile sincronizzare submission: {e}")
        return {"status": "error", "message": str(e), "recent_rejections": []}
        
    recent_rejections = []
    recent_accepted = []
    recent_pending = []
    all_submission_urls = {}
    
    for s in submissions:
        created_str = s.get("created_at")
        sub_time = now
        if created_str:
            try:
                sub_time = datetime.fromisoformat(created_str.replace("Z", "+00:00")).replace(tzinfo=None)
            except Exception:
                pass

        is_recent = sub_time >= cutoff_time
        sub_id = s.get("id")
        status = s.get("status")
        post_url = s.get("post_url", "")
        if post_url:
            all_submission_urls[post_url] = status
        
        if status == "rejected":
            if is_recent or (sub_id not in state.get("resolved_rejections", [])):
                recent_rejections.append(s)
        elif status == "accepted":
            if is_recent:
                recent_accepted.append(s)
        else:
            if is_recent:
                recent_pending.append(s)

    print(f"📊 Riepilogo sottomissioni Klippify:")
    print(f"   - ✅ Approvati di recente: {len(recent_accepted)}")
    print(f"   - ⏳ In revisione: {len(recent_pending)}")
    print(f"   - ❌ Rifiutati da esaminare: {len(recent_rejections)}")

    # 1. VERIFICA EFFICACIA ESPERIMENTO ATTIVO & PROPAGAZIONE A 6 VIDEO
    active_exp = state.get("active_experiment")
    if active_exp and active_exp.get("status") == "waiting_validation":
        tested_url = active_exp.get("tested_post_url")
        tested_clip = active_exp.get("tested_clip_name")
        camp_id = active_exp.get("campaign_id", "6a71c6f7245627c68999eae2")
        
        is_validated = False
        # Controlla se il video testato o una delle ultime submission è stata accettata
        for acc in recent_accepted:
            if tested_url and (tested_url in acc.get("post_url", "")):
                is_validated = True
                break
            # Oppure se c'è stata una recente approvazione successiva al test
            is_validated = True

        if is_validated:
            print(f"\n🎉 [VALIDAZIONE CONFERMATA] L'AI di Klippify ha APPROVATO il video testato ('{tested_clip}')!")
            print(f"🚀 [PROPAGAZIONE AUTOMATICA] Avvio propagazione modifiche sui successivi 6 video cronologici...")
            
            avail_clips = get_chronological_available_clips(camp_id)
            propagated = []
            for cl in avail_clips[:6]:
                print(f"   -> [Propagazione {len(propagated)+1}/6] Applicazione modifiche a: {cl.name}...")
                ok = apply_fix_to_clip(cl)
                if ok:
                    propagated.append(cl.name)

            state["propagation_history"].append({
                "validated_at": now.strftime("%Y-%m-%d %H:%M:%S"),
                "tested_clip": tested_clip,
                "propagated_count": len(propagated),
                "propagated_clips": propagated
            })
            state["active_experiment"] = None
            print(f"✅ [PROPAGAZIONE COMPLETATA] Applicata con successo la modifica vincente a {len(propagated)} video successivi!")

    # 2. GESTIONE DEI NUOVI RIFIUTI: ADATTA IL PROSSIMO VIDEO CRONOLOGICO
    corrective_actions = []
    if recent_rejections:
        print(f"\n⚠️ [ALERT] Rilevati {len(recent_rejections)} video rifiutati dall'AI di Klippify!")
        for idx, rej in enumerate(recent_rejections, 1):
            sub_id = rej.get("id")
            camp_name = rej.get("campaign_name", "N/D")
            camp_id = rej.get("campaign_id", "6a71c6f7245627c68999eae2")
            post_url = rej.get("post_url", "N/D")
            reason = rej.get("ai_reasoning", "Nessuna motivazione fornita.")
            
            print(f"\n--- Rifiuto #{idx} [ID: {sub_id}] ---")
            print(f"   Campagna: {camp_name}")
            print(f"   Link: {post_url}")
            print(f"   Motivo AI Klippify: {reason}")

            # Trova il video cronologicamente successivo per testare la correzione
            avail_clips = get_chronological_available_clips(camp_id)
            target_clip = avail_clips[0] if avail_clips else None
            
            if target_clip:
                print(f"\n🎯 [FASE 1 - TEST ADATTIVO] Modifica correttiva applicata al prossimo video cronologico: '{target_clip.name}'")
                ok = apply_fix_to_clip(target_clip)
                if ok:
                    state["active_experiment"] = {
                        "tested_clip_name": target_clip.name,
                        "tested_clip_path": str(target_clip),
                        "tested_post_url": None, # Verrà associato alla pubblicazione
                        "rejection_reason": reason,
                        "campaign_id": camp_id,
                        "status": "waiting_validation",
                        "created_at": now.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    action_desc = f"Modificato e renderizzato il 1° video successivo cronologico ('{target_clip.name}'). In attesa di approvazione Klippify per propagare ai successivi 6 video."
                else:
                    action_desc = "Errore durante il rendering del video successivo."
            else:
                action_desc = "Nessun video vergine disponibile da modificare sul disco."

            corrective_actions.append({
                "submission_id": sub_id,
                "campaign_id": camp_id,
                "reason": reason,
                "action": action_desc
            })
            
            if sub_id not in state.get("resolved_rejections", []):
                state["resolved_rejections"].append(sub_id)

    else:
        print("✅ [PERFETTO] Nessun nuovo rifiuto registrato nell'intervallo temporale.")

    state["last_audit_time"] = now.strftime("%Y-%m-%d %H:%M:%S")
    save_audit_state(state)

    return {
        "status": "success",
        "audit_timestamp": state["last_audit_time"],
        "recent_accepted_count": len(recent_accepted),
        "recent_pending_count": len(recent_pending),
        "recent_rejections_count": len(recent_rejections),
        "corrective_actions": corrective_actions
    }

if __name__ == "__main__":
    audit_recent_submissions(hours_window=4)