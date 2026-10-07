"""Transcript text stays literal while generated karaoke markup remains active."""
import json

import pytest

from tools.subtitle.subtitle_gen import SubtitleGen


@pytest.mark.parametrize("fmt", ["srt", "vtt"])
@pytest.mark.parametrize("style", ["none", "word_by_word", "karaoke"])
def test_transcript_markup_is_escaped(tmp_path, fmt, style):
    output = tmp_path / f"captions.{fmt}"
    result = SubtitleGen().execute({
        "segments": [{"words": [
            {"word": "<b>tag</b>", "start": 0, "end": 1},
            {"word": "&amp;", "start": 1, "end": 2},
        ]}],
        "format": fmt,
        "highlight_style": style,
        "output_path": str(output),
    })
    assert result.success, result.error
    content = output.read_text()
    assert "&lt;b&gt;tag&lt;/b&gt;" in content
    assert "&amp;amp;" in content
    if style == "karaoke":
        assert "<b>&lt;b&gt;tag&lt;/b&gt;</b>" in content
    else:
        assert "<b>" not in content


def test_caption_json_keeps_raw_text(tmp_path):
    output = tmp_path / "captions.json"
    result = SubtitleGen().execute({
        "segments": [{"text": "<b>tag</b> &amp;", "start": 0, "end": 1}],
        "format": "json", "output_path": str(output),
    })
    assert result.success, result.error
    assert json.loads(output.read_text())["cues"][0]["text"] == "<b>tag</b> &amp;"
