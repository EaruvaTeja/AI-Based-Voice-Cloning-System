# validation.py
"""Input validation for the AI-Based Voice Cloning System.

Covers the project-statement requirements:
- Audio format, size, and duration
- Text presence and maximum length
- Output path normalization
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Dict

import soundfile as sf

SUPPORTED_AUDIO_EXTENSIONS = {".wav", ".flac", ".mp3", ".ogg", ".m4a"}
MAX_AUDIO_SIZE_MB = 25
MIN_AUDIO_DURATION_SEC = 3.0
MAX_AUDIO_DURATION_SEC = 30.0
MAX_TEXT_LENGTH = 500


def validate_reference_audio(file_path: str) -> Dict[str, object]:
    """Validate a reference audio file. Returns metadata dict on success."""
    if not file_path:
        raise ValueError("Reference audio path is empty.")

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Reference audio not found: {file_path}")

    if path.suffix.lower() not in SUPPORTED_AUDIO_EXTENSIONS:
        raise ValueError(
            f"Unsupported audio format '{path.suffix}'. "
            f"Allowed: {sorted(SUPPORTED_AUDIO_EXTENSIONS)}"
        )

    size_mb = path.stat().st_size / (1024 * 1024)
    if size_mb > MAX_AUDIO_SIZE_MB:
        raise ValueError(
            f"Audio file too large ({size_mb:.1f} MB > "
            f"{MAX_AUDIO_SIZE_MB} MB limit)."
        )

    try:
        info = sf.info(str(path))
    except Exception as exc:
        raise ValueError(f"Could not read audio file: {exc}") from exc

    if info.duration < MIN_AUDIO_DURATION_SEC:
        raise ValueError(
            f"Audio too short ({info.duration:.1f}s < "
            f"{MIN_AUDIO_DURATION_SEC}s minimum)."
        )
    if info.duration > MAX_AUDIO_DURATION_SEC:
        raise ValueError(
            f"Audio too long ({info.duration:.1f}s > "
            f"{MAX_AUDIO_DURATION_SEC}s maximum)."
        )

    return {
        "path": str(path.resolve()),
        "duration_sec": round(info.duration, 2),
        "sample_rate": info.samplerate,
        "channels": info.channels,
        "size_mb": round(size_mb, 2),
    }


def validate_text(text: str) -> str:
    """Validate and return cleaned text input."""
    if text is None:
        raise ValueError("Text input is missing.")
    text = text.strip()
    if not text:
        raise ValueError("Text input is empty.")
    if len(text) > MAX_TEXT_LENGTH:
        raise ValueError(
            f"Text too long ({len(text)} chars > "
            f"{MAX_TEXT_LENGTH} character limit). Please shorten it."
        )
    return text


def validate_output_path(output_path: str) -> str:
    """Ensure the output path ends in .wav and its parent folder exists."""
    if not output_path:
        raise ValueError("Output path is empty.")
    if not output_path.lower().endswith(".wav"):
        raise ValueError("Output file must have a .wav extension.")
    parent = Path(output_path).parent
    parent.mkdir(parents=True, exist_ok=True)
    return str(Path(output_path).resolve())