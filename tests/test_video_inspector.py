import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "core"))
import video_inspector

def test_parse_json3_and_group_into_timed_lines(tmp_path):
    sample_json3 = {
        "events": [
            {"tStartMs": 0, "dDurationMs": 1000, "segs": [{"utf8": "\n"}]},
            {
                "tStartMs": 1500,
                "dDurationMs": 1800,
                "segs": [
                    {"utf8": "Nel "},
                    {"utf8": "primo ", "tOffsetMs": 400},
                    {"utf8": "mese ", "tOffsetMs": 800},
                    {"utf8": "3.200€.", "tOffsetMs": 1200}
                ]
            },
            {
                "tStartMs": 5000,
                "dDurationMs": 1500,
                "segs": [
                    {"utf8": "Senza "},
                    {"utf8": "esperienza!", "tOffsetMs": 600}
                ]
            }
        ]
    }
    sub_file = tmp_path / "video.it.json3"
    sub_file.write_text(json.dumps(sample_json3), encoding="utf-8")

    words = video_inspector.parse_subtitle_file(sub_file)
    assert len(words) == 6
    lines = video_inspector.group_words_into_timed_lines(words, pause_sec=0.5)
    assert len(lines) == 2
    assert lines[0]["text"] == "Nel primo mese 3.200€."
    assert lines[0]["start"] == 1.5
    assert lines[1]["text"] == "Senza esperienza!"
    assert lines[1]["start"] == 5.0

def test_parse_vtt_subtitles(tmp_path):
    vtt = """WEBVTT

00:00:10.000 --> 00:00:13.000
Ecco cosa tenere nel montaggio.
"""
    vtt_file = tmp_path / "video.it.vtt"
    vtt_file.write_text(vtt, encoding="utf-8")
    words = video_inspector.parse_subtitle_file(vtt_file)
    assert [w["word"] for w in words] == ["Ecco", "cosa", "tenere", "nel", "montaggio."]
    assert words[0]["start"] == 10.0
    assert round(words[-1]["end"], 1) == 13.0
