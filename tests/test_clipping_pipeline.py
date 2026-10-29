import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "core"))
import clipping_pipeline

def test_purge_legacy_blind_clips_removes_all_hardcoded_fallback_entries(tmp_path):
    meta_file = tmp_path / "clip_metadata.json"
    sched_file = tmp_path / "campaign_schedules.json"

    meta_data = {
        "blind_1.mp4": {
            "filename": "blind_1.mp4",
            "campaign_id": "camp1",
            "transcript": "Estratto dal video originale",
            "start_time": "00:10",
            "end_time": "00:45"
        },
        "ai_directed_1.mp4": {
            "filename": "ai_directed_1.mp4",
            "campaign_id": "camp1",
            "transcript": "In 30 giorni abbiamo raggiunto 3.200 euro.",
            "segments": [{"start": "02:10", "end": "02:13"}, {"start": "00:40", "end": "01:08"}]
        }
    }
    sched_data = {
        "camp1": {
            "target_count": 2,
            "slots": [
                {"time": "15:00", "video": "blind_1.mp4"},
                {"time": "18:00", "video": "ai_directed_1.mp4"}
            ]
        }
    }
    meta_file.write_text(json.dumps(meta_data), encoding="utf-8")
    sched_file.write_text(json.dumps(sched_data), encoding="utf-8")

    res = clipping_pipeline.purge_legacy_blind_clips(tmp_path)
    assert res["removed_count"] == 1
    cleaned_meta = json.loads(meta_file.read_text(encoding="utf-8"))
    assert "blind_1.mp4" not in cleaned_meta
    assert "ai_directed_1.mp4" in cleaned_meta

    cleaned_sched = json.loads(sched_file.read_text(encoding="utf-8"))
    assert cleaned_sched["camp1"]["slots"][0]["video"] == ""
    assert cleaned_sched["camp1"]["slots"][1]["video"] == "ai_directed_1.mp4"

def test_load_ai_director_cuts_reads_matching_cuts(tmp_path):
    cuts_path = tmp_path / "ai_director_cuts.json"
    cuts_payload = {
        "campaign_id": "camp1",
        "video_file": "source.mp4",
        "clips": [
            {
                "clip_number": 1,
                "concept": "Risultato concreto",
                "hook_text": "12.400€ IN 60 GIORNI DA ZERO",
                "crop_mode": "face_crop",
                "center_x_ratio": 0.52,
                "segments": [
                    {"start": "02:14.2", "end": "02:17.1", "role": "teaser"},
                    {"start": "00:42.5", "end": "01:08.0", "role": "body"}
                ],
                "transcript": "In sessanta giorni siamo arrivati a 12.400 euro.",
                "tiktok_caption": "Storia incredibile!"
            }
        ]
    }
    cuts_path.write_text(json.dumps(cuts_payload), encoding="utf-8")
    loaded = clipping_pipeline.load_ai_director_cuts(cuts_path, video_name="source.mp4", campaign_id="camp1")
    assert len(loaded) == 1
    assert loaded[0]["hook_text"] == "12.400€ IN 60 GIORNI DA ZERO"
    assert len(loaded[0]["segments"]) == 2


def test_workflow_finds_cuts_in_data_subdir_with_case_insensitive_video_name(tmp_path, monkeypatch):
    monkeypatch.setattr(clipping_pipeline.paths, "PROJECT_ROOT", tmp_path)
    raw_dir = tmp_path / "clipping_sources" / "camp1"
    raw_dir.mkdir(parents=True)
    dummy_vid = raw_dir / "Source_Video.MP4"
    dummy_vid.write_bytes(b"00" * 1024)

    data_dir = tmp_path / "data"
    data_dir.mkdir(parents=True)
    cuts_file = data_dir / "ai_director_cuts.json"
    cuts_file.write_text(json.dumps({
        "campaign_id": "camp1",
        "video_file": "source_video.mp4",
        "clips": [
            {
                "clip_number": 1,
                "concept": "Clip trovata in data/",
                "hook_text": "HOOK DA DATA DIR",
                "crop_mode": "face_crop",
                "center_x_ratio": 0.5,
                "segments": [{"start": "00:05", "end": "00:30"}],
                "transcript": "Testo reale",
                "tiktok_caption": "Caption reale"
            }
        ]
    }), encoding="utf-8")

    monkeypatch.setattr(
        clipping_pipeline.clip_processor,
        "process_clip_ffmpeg",
        lambda **kwargs: True
    )

    res = clipping_pipeline.run_clipping_workflow("camp1", video_source_path=str(dummy_vid))
    assert res["status"] == "success"
    assert len(res["clips"]) == 1
    assert res["clips"][0]["hook_text"] == "HOOK DA DATA DIR"

def test_workflow_without_ai_cuts_does_not_cut_blindly_and_prepares_inspection(tmp_path, monkeypatch):
    monkeypatch.setattr(clipping_pipeline.paths, "PROJECT_ROOT", tmp_path)
    raw_dir = tmp_path / "clipping_sources" / "camp_test"
    raw_dir.mkdir(parents=True)
    dummy_vid = raw_dir / "source_video.mp4"
    dummy_vid.write_bytes(b"00" * 1024)

    monkeypatch.setattr(
        clipping_pipeline.video_inspector,
        "inspect_video",
        lambda vp, campaign_id="general": {"inspection_file": str(tmp_path / "source_video_inspection.json")}
    )

    res = clipping_pipeline.run_clipping_workflow("camp_test", video_source_path=str(dummy_vid))
    assert res["status"] == "awaiting_ai_director"
    assert "inspection_file" in res
