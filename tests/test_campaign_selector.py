import sys
from pathlib import Path
from unittest.mock import patch

ROOT_DIR = Path(__file__).resolve().parent.parent
CORE_DIR = ROOT_DIR / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

import campaign_selector


def test_campaign_selector_promotes_winners_drops_losers_and_tests_promising(tmp_path):
    fake_ranked = [
        {
            "id": "camp_winner",
            "name": "Sara Dizdari Academy",
            "brand": "Sara Dizdari",
            "section": "Iscritte",
            "status": "Active",
            "budget_remaining": 300.0,
            "payout_per_1k_views": 0.5,
            "total_views": 380000,
            "creators_count": 20,
            "description": "Clip verticali podcast interviste ecommerce"
        },
        {
            "id": "camp_loser",
            "name": "Flop Podcast Campaign",
            "brand": "Flop",
            "section": "Nuove",
            "status": "Active",
            "budget_remaining": 200.0,
            "payout_per_1k_views": 0.5,
            "total_views": 10000,
            "creators_count": 50,
            "description": "Podcast clip"
        },
        {
            "id": "camp_promising",
            "name": "Le 9 Bugie di FitActive",
            "brand": "Theory Spa",
            "section": "Nuove",
            "status": "Active",
            "budget_remaining": 180.0,
            "payout_per_1k_views": 0.75,
            "total_views": 1200000,
            "creators_count": 250,
            "description": "Podcast Theory Spa"
        }
    ]

    fake_audit = {
        "by_campaign": {
            "camp_winner": {
                "total_submitted": 4,
                "accepted_count": 4,
                "rejected_count": 0,
                "pending_count": 0,
                "approval_rate_pct": 100.0
            },
            "camp_loser": {
                "total_submitted": 3,
                "accepted_count": 1,
                "rejected_count": 2,
                "pending_count": 0,
                "approval_rate_pct": 33.3
            }
        }
    }

    fake_subs = [
        {"campaign_id": "camp_winner", "views": 500},
        {"campaign_id": "camp_winner", "views": 300},
        {"campaign_id": "camp_winner", "views": 250},
        {"campaign_id": "camp_winner", "views": 400},
        {"campaign_id": "camp_loser", "views": 5},
        {"campaign_id": "camp_loser", "views": 8},
        {"campaign_id": "camp_loser", "views": 2},
    ]

    def fake_load(path, default):
        name = Path(path).name
        if name == "campaigns_ranked.json":
            return fake_ranked
        if name == "approval_audit_report.json":
            return fake_audit
        if name == "klippify_submissions.json":
            return fake_subs
        if name == "ai_campaign_decisions.json":
            return {"campaigns": {"camp_promising": {"feasible": True, "recommended_stage": "testing"}}}
        return default

    saved_files = {}
    def fake_save(path, data):
        saved_files[Path(path).name] = data

    with patch.object(campaign_selector, "_load_json_safe", side_effect=fake_load), \
         patch.object(campaign_selector, "_save_json_safe", side_effect=fake_save):
        plan = campaign_selector.evaluate_and_select_campaigns(
            max_scaling=3,
            max_testing=2,
            min_test_submissions=3,
            apply_changes=True
        )

    assert len(plan["scaling_campaigns"]) == 1
    assert plan["scaling_campaigns"][0]["campaign_id"] == "camp_winner"

    assert len(plan["dropped_campaigns"]) == 1
    assert plan["dropped_campaigns"][0]["campaign_id"] == "camp_loser"

    assert len(plan["testing_campaigns"]) == 1
    assert plan["testing_campaigns"][0]["campaign_id"] == "camp_promising"

    sched = saved_files["campaign_schedules.json"]
    assert len(sched["camp_winner"]["slots"]) == 6
    assert sched["camp_winner"]["lifecycle_stage"] == "scaling"
    assert len(sched["camp_promising"]["slots"]) == 2
    assert sched["camp_promising"]["lifecycle_stage"] == "testing"
