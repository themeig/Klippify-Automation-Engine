# 🧠 Klippify Automation Engine — Agent Rules (`AGENTS.md`)

Leggi e segui integralmente le regole definite in [`GEMINI.md`](./GEMINI.md) e la skill operativa [`.agents/skills/klippify-ai-director/SKILL.md`](./.agents/skills/klippify-ai-director/SKILL.md).

- Al primo avvio su un computer, assicurati che il cronjob di Antigravity sia allineato ai percorsi locali eseguendo `python core/setup_antigravity_cron.py`.
- Non usare mai tagli fissi o casuali: ispeziona sempre il video con `core/video_inspector.py`, leggi `<video_stem>_inspection.json`, guarda le Storyboard JPG con `read_file`, scrivi i segmenti da tenere in `data/ai_director_cuts.json` e lancia `core/clipping_pipeline.py --cuts data/ai_director_cuts.json`.
