import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "core"))
import setup_antigravity_cron

def test_install_or_update_sidecar_writes_valid_portable_config(tmp_path):
    fake_repo = tmp_path / "KlippifyOnOldLaptop"
    fake_repo.mkdir()
    fake_config = tmp_path / ".gemini" / "config"

    sidecar_path = setup_antigravity_cron.install_or_update_sidecar(
        repo_root=fake_repo,
        config_dir=fake_config,
        cron_expr="CRON_TZ=Europe/Rome 0 */4 * * *"
    )
    assert sidecar_path.exists()
    data = json.loads(sidecar_path.read_text(encoding="utf-8"))
    assert data["builtin"] == "schedule"
    assert data["restart_policy"] == "always"
    assert data["display_name"] == "Klippify AI Director (4h)"
    assert data["args"][0] == "CRON_TZ=Europe/Rome 0 */4 * * *"
    assert data["args"][1:4] == ["agentapi", "new-conversation", "--"]
    assert str(fake_repo).replace("\\", "/") in data["args"][4].replace("\\", "/")
    assert any(str(fake_repo).replace("\\", "/") in u.replace("\\", "/") for u in data["agent_permissions"]["workspace_uris"])

def test_workspace_rules_and_skill_files_exist_and_have_valid_frontmatter():
    gemini_md = REPO_ROOT / "GEMINI.md"
    agents_md = REPO_ROOT / "AGENTS.md"
    skill_md = REPO_ROOT / ".agents" / "skills" / "klippify-ai-director" / "SKILL.md"

    assert gemini_md.exists()
    assert agents_md.exists()
    assert skill_md.exists()

    skill_text = skill_md.read_text(encoding="utf-8")
    assert skill_text.startswith("---\nname: klippify-ai-director\n")
    assert "ai_director_cuts.json" in skill_text
    assert "setup_antigravity_cron.py" in gemini_md.read_text(encoding="utf-8")
