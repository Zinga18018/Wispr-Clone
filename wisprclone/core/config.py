import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class AudioConfig:
    """Audio processing configuration"""
    sample_rate: int = 16000
    chunk_size: int = 1024
    channels: int = 1
    device_index: Optional[int] = None
    noise_reduction: bool = True
    silence_threshold: float = 0.01
    silence_duration: float = 1.0


@dataclass
class WhisperConfig:
    """Whisper model configuration"""
    model_size: str = "base"  # tiny, base, small, medium, large
    language: Optional[str] = None  # Auto-detect if None
    task: str = "transcribe"  # transcribe or translate
    temperature: float = 0.0
    no_speech_threshold: float = 0.6
    logprob_threshold: float = -1.0
    compression_ratio_threshold: float = 2.4


@dataclass
class OutputConfig:
    """Output configuration"""
    output_to_console: bool = True
    output_to_clipboard: bool = False
    output_to_file: bool = False
    output_file_path: str = "transcription.txt"
    typing_enabled: bool = False
    typing_delay: float = 0.01


@dataclass
class HotkeyConfig:
    """Hotkey configuration"""
    toggle_recording: str = "ctrl+shift+r"
    stop_recording: str = "escape"
    toggle_typing: str = "ctrl+shift+t"
    clear_output: str = "ctrl+shift+c"


@dataclass
class UIConfig:
    """UI configuration"""
    theme: str = "dark"  # dark, light, system
    window_size: tuple = (800, 600)
    always_on_top: bool = False
    minimize_to_tray: bool = True
    show_waveform: bool = True


class Config:
    """Main configuration manager for WisprClone"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._get_default_config_path()
        self.audio = AudioConfig()
        self.whisper = WhisperConfig()
        self.output = OutputConfig()
        self.hotkeys = HotkeyConfig()
        self.ui = UIConfig()
        
        # Load configuration if file exists
        self.load()
    
    def _get_default_config_path(self) -> str:
        """Get default configuration file path"""
        config_dir = Path.home() / ".wisprclone"
        config_dir.mkdir(exist_ok=True)
        return str(config_dir / "config.json")
    
    def load(self) -> None:
        """Load configuration from file"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Update configurations
                if 'audio' in data:
                    self.audio = AudioConfig(**data['audio'])
                if 'whisper' in data:
                    self.whisper = WhisperConfig(**data['whisper'])
                if 'output' in data:
                    self.output = OutputConfig(**data['output'])
                if 'hotkeys' in data:
                    self.hotkeys = HotkeyConfig(**data['hotkeys'])
                if 'ui' in data:
                    self.ui = UIConfig(**data['ui'])
                    
            except Exception as e:
                print(f"Error loading config: {e}")
                print("Using default configuration")
    
    def save(self) -> None:
        """Save configuration to file"""
        try:
            data = {
                'audio': asdict(self.audio),
                'whisper': asdict(self.whisper),
                'output': asdict(self.output),
                'hotkeys': asdict(self.hotkeys),
                'ui': asdict(self.ui)
            }
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def reset_to_defaults(self) -> None:
        """Reset all configuration to defaults"""
        self.audio = AudioConfig()
        self.whisper = WhisperConfig()
        self.output = OutputConfig()
        self.hotkeys = HotkeyConfig()
        self.ui = UIConfig()
        self.save()
    
    def get_whisper_model_path(self) -> str:
        """Get path for storing Whisper models"""
        model_dir = Path.home() / ".wisprclone" / "models"
        model_dir.mkdir(exist_ok=True)
        return str(model_dir)
    
    def get_available_models(self) -> list:
        """Get list of available Whisper model sizes"""
        return ["tiny", "base", "small", "medium", "large"]
    
    def get_supported_languages(self) -> list:
        """Get list of supported languages"""
        return [
            "auto", "en", "zh", "de", "es", "ru", "ko", "fr", "ja", "pt", "tr", "pl",
            "ca", "nl", "ar", "sv", "it", "id", "hi", "fi", "vi", "he", "uk", "el",
            "ms", "cs", "ro", "da", "hu", "ta", "no", "th", "ur", "hr", "bg", "lt",
            "la", "mi", "ml", "cy", "sk", "te", "fa", "lv", "bn", "sr", "az", "sl",
            "kn", "et", "mk", "br", "eu", "is", "hy", "ne", "mn", "bs", "kk", "sq",
            "sw", "gl", "mr", "pa", "si", "km", "sn", "yo", "so", "af", "oc", "ka",
            "be", "tg", "sd", "gu", "am", "yi", "lo", "uz", "fo", "ht", "ps", "tk",
            "nn", "mt", "sa", "lb", "my", "bo", "tl", "mg", "as", "tt", "haw", "ln",
            "ha", "ba", "jw", "su"
        ] 