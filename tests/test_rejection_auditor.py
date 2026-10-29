import json
import sys
from pathlib import Path
from unittest.mock import patch

ROOT_DIR = Path(__file__).resolve().parent.parent
CORE_DIR = ROOT_DIR / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

import rejection_auditor


def test_get_campaign_cta_never_hardcodes_other_campaign():
    with patch("video_inspector.load_campaign_brief") as mock_brief:
        mock_brief.return_value = {
            "name": "Saikoo × Theory SPA — Il bilancio 2025 in anteprima",
            "brand": "Saikoo",
            "call_to_action": "Guarda il video completo su Klippify!",
            "mandatory_mentions": ["@saikooai"],
            "mandatory_hashtags": ["#saikootheoryspailbilancio2025inanteprima", "#klippify"],
            "rules": ["Durata 30-60s"],
            "video_prompt": "Mostra i dati di bilancio con Saikoo"
        }
        info = rejection_auditor.get_campaign_cta_and_brief("6a91676284a29ab01b754c33")
        assert "sara" not in info["cta_text"].lower()
        assert "su klippify" not in info["cta_text"].lower()
        assert "@saikooai" in info["cta_text"]
        assert info["primary_mention"] == "@saikooai"


def test_match_submission_to_local_clip_links_metadata():
    sub = {
        "id": "sub_1",
        "post_url": "https://www.tiktok.com/@jiemli/video/7679999999999999999"
    }
    published_records = [
        {
            "filename": "clip_SaikooTheory_slot1_20261030_002748.mp4",
            "post_url": "https://www.tiktok.com/@jiemli/video/7679999999999999999",
            "video_id": "7679999999999999999",
            "title": "Test caption @saikooai",
            "published_at": "2026-10-30 00:30:00"
        }
    ]
    clip_meta = {
        "clip_SaikooTheory_slot1_20261030_002748.mp4": {
            "hook_text": "FATTURIAMO 4,5 MILIONI AL MESE",
            "cta_text": "ANALIZZA I BILANCI DI 6M+ AZIENDE SU SAIKOO.AI!",
            "brand_mention": "👉 Segui @saikooai",
            "segments": [{"start": 891.9, "end": 898.3, "role": "teaser"}],
            "raw_source_video": "source.mp4",
            "directed_by": "antigravity_ai_director"
        }
    }
    matched = rejection_auditor.match_submission_to_local_clip(sub, published_records, clip_meta)
    assert matched["clip_filename"] == "clip_SaikooTheory_slot1_20261030_002748.mp4"
    assert matched["hook_text"] == "FATTURIAMO 4,5 MILIONI AL MESE"
    assert matched["cta_text"] == "ANALIZZA I BILANCI DI 6M+ AZIENDE SU SAIKOO.AI!"
    assert matched["directed_by"] == "antigravity_ai_director"


def test_diagnose_rejection_reason_extracts_categories_and_instructions():
    camp_info = {
        "campaign_name": "Saikoo × Theory SPA",
        "cta_text": "ANALIZZA I BILANCI SU SAIKOO.AI!",
        "primary_mention": "@saikooai",
        "video_prompt": "Parla del bilancio 2025 da 18M"
    }
    diag = rejection_auditor.diagnose_rejection_reason(
        "The video fails to follow the hook guidelines in the first 3 seconds and lacks the call to action at the end.",
        camp_info
    )
    assert "weak_hook" in diag["categories"]
    assert "missing_or_weak_cta" in diag["categories"]
    assert "ANALIZZA I BILANCI SU SAIKOO.AI!" in diag["ai_director_instruction"]


def test_audit_recent_submissions_classifies_approvals_and_active_rejections(tmp_path):
    fake_subs = [
        {
            "id": "sub_acc_1",
            "campaign_id": "camp_saikoo",
            "campaign_name": "Saikoo Campaign",
            "post_url": "https://www.tiktok.com/@user/video/111111",
            "status": "accepted",
            "is_ai_verified": True,
            "ai_reasoning": "Complies with all guidelines and strong hook.",
            "views": 1500,
            "likes": 90,
            "earnings": 1.5,
            "created_at": "2026-10-30T00:10:00Z"
        },
        {
            "id": "sub_rej_2",
            "campaign_id": "camp_saikoo",
            "campaign_name": "Saikoo Campaign",
            "post_url": "https://www.tiktok.com/@user/video/222222",
            "status": "rejected",
            "is_ai_verified": True,
            "ai_reasoning": "Missing call to action at the end of the video.",
            "views": 50,
            "likes": 2,
            "earnings": 0.0,
            "created_at": "2026-10-30T00:40:00Z"
        },
        {
            "id": "sub_pend_3",
            "campaign_id": "camp_saikoo",
            "campaign_name": "Saikoo Campaign",
            "post_url": "https://www.tiktok.com/@user/video/333333",
            "status": "pending",
            "is_ai_verified": False,
            "ai_reasoning": "",
            "views": 10,
            "likes": 1,
            "earnings": 0.0,
            "created_at": "2026-10-30T00:45:00Z"
        }
    ]

    state_file = tmp_path / "rejection_audit_state.json"
    report_file = tmp_path / "approval_audit_report.json"

    with patch.object(rejection_auditor, "AUDIT_STATE_FILE", state_file), \
         patch.object(rejection_auditor, "APPROVAL_REPORT_FILE", report_file), \
         patch("rejection_auditor.fetch_klippify_submissions", return_value=fake_subs), \
         patch("rejection_auditor.get_chronological_available_clips", return_value=[]):

        rep = rejection_auditor.audit_recent_submissions(hours_window=24, use_cache=True)

        assert rep["status"] == "success"
        assert rep["summary"]["total_submissions"] == 3
        assert rep["summary"]["total_accepted"] == 1
        assert rep["summary"]["total_rejected"] == 1
        assert rep["summary"]["total_pending"] == 1
        assert rep["summary"]["overall_approval_rate_pct"] == 50.0
        assert "camp_saikoo" in rep["by_campaign"]
        assert "camp_saikoo" in rep["campaigns_needing_attention"]
        assert report_file.exists()
