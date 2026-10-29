import json
import sys
import urllib.parse
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def _path_to_file_uri(p: Path) -> str:
    resolved = p.resolve()
    posix_str = str(resolved).replace("\\", "/")
    if not posix_str.startswith("/"):
        posix_str = "/" + posix_str
    return f"file://{posix_str}"


def install_or_update_sidecar(
    repo_root: Path = None,
    config_dir: Path = None,
    cron_expr: str = "CRON_TZ=Europe/Rome 0 */4 * * *"
) -> Path:
    """
    Crea o aggiorna automaticamente la Scheduled Automation nativa di Antigravity
    ('Klippify AI Director (4h)') usando i percorsi assoluti reali del PC corrente.
    Funziona su qualsiasi computer dove viene clonata la repository.
    """
    root_p = Path(repo_root).resolve() if repo_root else Path(__file__).resolve().parent.parent
    cfg_p = Path(config_dir).resolve() if config_dir else (Path.home() / ".gemini" / "config")

    sidecar_dir = cfg_p / "sidecars" / "klippify-ai-director"
    sidecar_dir.mkdir(parents=True, exist_ok=True)
    sidecar_file = sidecar_dir / "sidecar.json"

    skill_path = (root_p / ".agents" / "skills" / "klippify-ai-director" / "SKILL.md").resolve()
    root_posix = str(root_p).replace("\\", "/")
    skill_posix = str(skill_path).replace("\\", "/")

    prompt = (
        f"Sei il Regista AI di Klippify Automation Engine nella cartella '{root_posix}'. "
        f"Leggi e segui passo-passo la skill '{skill_posix}': "
        f"1) Esegui l'audit dei rifiuti e analizza le views in data/klippify_submissions.json; "
        f"2) Controlla se ci sono video sorgente da montare (o scaricane uno nuovo da data/campaign_sources.json con core/source_downloader.py) ed esegui core/video_inspector.py sul video; "
        f"3) Leggi il file <video_stem>_inspection.json (controllando prima di tutto campaign_brief per allineare il contenuto e la CTA alle richieste specifiche della campagna Klippify) e guarda le Storyboard JPG con read_file per decidere esattamente quali segmenti tenere e quali scartare (Teaser + Corpo + Payoff), il center_x_ratio a schermo intero (face_crop) per ogni segmento, l'hook (3.2s), la cta_text e la caption, salvandoli in data/ai_director_cuts.json; "
        f"4) Lancia 'python core/clipping_pipeline.py <campaign_id> --video <video_path> --cuts data/ai_director_cuts.json' per generare le clip 9:16 e accodarle all'autopilota."
    )

    sidecar_payload = {
        "builtin": "schedule",
        "args": [
            cron_expr,
            "agentapi",
            "new-conversation",
            "--",
            prompt
        ],
        "restart_policy": "always",
        "display_name": "Klippify AI Director (4h)",
        "description": "Ogni 4 ore (Europe/Rome), l'Agente AI di Antigravity ispeziona i video sorgente (trascrizione + Storyboard JPG), decide cosa tenere e cosa scartare in data/ai_director_cuts.json e avvia il montaggio FFmpeg 9:16.",
        "agent_permissions": {
            "workspace_uris": [
                _path_to_file_uri(root_p)
            ],
            "access_grants": [
                "command(python)",
                "command(ffmpeg)",
                "command(ffprobe)",
                f"read_file({root_posix})",
                f"write_file({root_posix})"
            ]
        }
    }

    sidecar_file.write_text(json.dumps(sidecar_payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[ANTIGRAVITY-SETUP] Cronjob 'Klippify AI Director (4h)' configurato per questo PC in: {sidecar_file}")
    return sidecar_file


if __name__ == "__main__":
    cron = sys.argv[1] if len(sys.argv) > 1 else "CRON_TZ=Europe/Rome 0 */4 * * *"
    install_or_update_sidecar(cron_expr=cron)
