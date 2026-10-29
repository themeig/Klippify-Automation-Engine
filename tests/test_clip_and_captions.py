import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "core"))
import clip_processor
import video_captioner

def test_hook_card_disappears_after_3_2_seconds():
    events = video_captioner.format_hook_card("3.200€ NEL PRIMO MESE")
    assert len(events) == 2
    for ev in events:
        assert "0:00:00.00,0:00:03.20" in ev
        assert "1:00:00.00" not in ev
        assert "SUL PROFILO DI SARA" not in ev

def test_generate_ass_file_uses_dynamic_campaign_cta_and_mention(tmp_path):
    ass_file = tmp_path / "test.ass"
    words = [
        {"word": "Ecco", "start": 0.2, "end": 0.6},
        {"word": "il", "start": 0.6, "end": 0.8},
        {"word": "risultato", "start": 0.8, "end": 1.4},
    ]
    video_captioner.generate_ass_file(
        words=words,
        output_ass_path=ass_file,
        duration_sec=30.0,
        hook_title="IL RISULTATO REALE",
        brand_cta="Guarda il video completo al link in bio!",
        brand_mention="@millionhospitality"
    )
    content = ass_file.read_text(encoding="utf-8")
    assert "GUARDA IL VIDEO COMPLETO AL LINK IN BIO!" in content
    assert "@millionhospitality" in content
    assert "@saradizdari_ecom" not in content

def test_generate_ass_file_without_mention_does_not_leak_sara_dizdari(tmp_path):
    ass_file = tmp_path / "test_nomention.ass"
    video_captioner.generate_ass_file(
        words=[{"word": "Ciao", "start": 0.1, "end": 0.5}],
        output_ass_path=ass_file,
        duration_sec=25.0,
        hook_title="TEST HOOK",
        brand_cta=None,
        brand_mention=None
    )
    content = ass_file.read_text(encoding="utf-8")
    assert "@saradizdari_ecom" not in content
    assert "Sara" not in content

def test_build_multisegment_ffmpeg_cmd_concatenates_ai_selected_segments(tmp_path):
    dummy_in = tmp_path / "in.mp4"
    dummy_out = tmp_path / "out.mp4"
    segments = [
        {"start": "02:10.5", "end": "02:13.0", "role": "teaser"},
        {"start": "00:30.0", "end": "00:45.0", "role": "body"},
        {"start": "01:12.0", "end": "01:28.5", "role": "payoff"}
    ]
    cmd = clip_processor.build_multisegment_ffmpeg_cmd(
        input_video_path=dummy_in,
        segments=segments,
        output_video_path=dummy_out,
        mode="face_crop",
        center_x_ratio=0.55
    )
    cmd_str = " ".join(cmd)
    assert "concat=n=3:v=1:a=1" in cmd_str
    assert "crop=" in cmd_str
    assert "-preset veryfast" in cmd_str

def test_build_crop_filter_supports_face_crop_split_screen_and_zoomed_blur():
    f_face, _ = clip_processor.build_crop_filter(mode="face_crop", center_x_ratio=0.6)
    assert "crop=1080:1920" in f_face

    f_split, _ = clip_processor.build_crop_filter(mode="split_screen", left_x=0.25, right_x=0.75)
    assert "vstack" in f_split

    f_zoom, _ = clip_processor.build_crop_filter(mode="zoomed_blur")
    assert "boxblur" in f_zoom and "1458" in f_zoom


def test_process_clip_ffmpeg_restores_video_if_captioner_fails(tmp_path, monkeypatch):
    in_vid = tmp_path / "in.mp4"
    in_vid.write_bytes(b"fake_input" * 100)
    out_vid = tmp_path / "out.mp4"

    class DummyCompleted:
        returncode = 0
        stderr = ""

    def fake_run(cmd, **kwargs):
        out_vid.write_bytes(b"rendered_9_16_video" * 1000)
        return DummyCompleted()

    monkeypatch.setattr(clip_processor.subprocess, "run", fake_run)
    monkeypatch.setattr(
        video_captioner,
        "burn_captions_to_video",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("Simulated Whisper failure"))
    )

    ok = clip_processor.process_clip_ffmpeg(
        input_video_path=in_vid,
        start_time="00:05",
        end_time="00:25",
        output_video_path=out_vid
    )
    assert ok is True
    assert out_vid.exists()
    assert out_vid.stat().st_size > 1000
