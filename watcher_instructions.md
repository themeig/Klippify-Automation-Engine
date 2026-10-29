# 📋 ISTRUZIONI OPERATIVE PER L'AGENTE AI: REGIA VIDEO MULTI-SEGMENTO & AUDIT KLIPPIFY

> **NOTA PER ANTIGRAVITY:** La procedura completa è incapsulata nella Skill nativa di questo workspace:
> 👉 [`.agents/skills/klippify-ai-director/SKILL.md`](.agents/skills/klippify-ai-director/SKILL.md)
> e nelle regole automatiche [`GEMINI.md`](GEMINI.md).

## 🎯 Flusso in 4 Passi del Regista AI (Ogni 4 Ore):
1. **Audit Rifiuti & Analisi Views:** esegui `python core/rejection_auditor.py` e controlla `data/klippify_submissions.json`.
2. **Download & Ispezione Video (`video_inspector.py`):** scarica un nuovo video con `core/source_downloader.py` e genera `<video_stem>_inspection.json` + le Storyboard JPG con `python core/video_inspector.py <video.mp4> <campaign_id>`.
3. **Regia AI (Cosa Tenere e Cosa Buttare):** leggi `<video_stem>_inspection.json`, guarda le Storyboard JPG con `read_file`, scegli i segmenti multipli (`teaser` + `body` + `payoff`), il `crop_mode` 9:16 sul volto, l'`hook_text` (primi 3.2s) e la `tiktok_caption`, salvandoli in `data/ai_director_cuts.json`.
4. **Montaggio FFmpeg & Coda Autopilota:** esegui `python core/clipping_pipeline.py <campaign_id> --video <video.mp4> --cuts data/ai_director_cuts.json`.
