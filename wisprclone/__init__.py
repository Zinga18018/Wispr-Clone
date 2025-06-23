"""
WisprClone - A powerful, real-time speech-to-text application using OpenAI Whisper

This package provides multiple interfaces for speech recognition:
- GUI interface with customtkinter
- CLI interface for terminal usage
- System tray integration
- Real-time transcription with multiple Whisper models
- Audio preprocessing and noise reduction
- Multiple output formats and hotkey support
"""

__version__ = "1.0.0"
__author__ = "WisprClone Team"
__email__ = "contact@wisprclone.com"

from .core.transcriber import WhisperTranscriber
from .core.audio_processor import AudioProcessor
from .core.config import Config

__all__ = ["WhisperTranscriber", "AudioProcessor", "Config"] 