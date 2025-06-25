# WisprClone

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](https://github.com/yourusername/wisprclone)

**WisprClone** is a powerful, real-time speech-to-text application built with OpenAI's Whisper model. It provides multiple interfaces (GUI, CLI, API) for accurate speech recognition with advanced features like noise reduction, multiple output formats, and real-time transcription.

## ✨ Features

### 🎯 Core Features
- **Real-time Speech Recognition** - Live transcription with minimal latency
- **Multiple Whisper Models** - Support for tiny, base, small, medium, and large models
- **Cross-platform** - Works on Windows, macOS, and Linux
- **Multiple Interfaces** - GUI, CLI, and programmatic API
- **Language Detection** - Automatic language detection for 100+ languages
- **High Accuracy** - Powered by OpenAI's state-of-the-art Whisper model

### 🔧 Advanced Features
- **Audio Preprocessing** - Noise reduction, filtering, and enhancement
- **Multiple Output Formats** - Console, file, clipboard, and typing simulation
- **Hotkey Support** - Global keyboard shortcuts for easy control
- **Batch Processing** - Process multiple audio files at once
- **Session Management** - Save and export transcription sessions
- **Model Benchmarking** - Compare performance across different models
- **Custom Configuration** - Flexible settings for all components

### 🎨 User Interface
- **Modern GUI** - Beautiful, dark-themed interface with CustomTkinter
- **Comprehensive CLI** - Full-featured command-line interface
- **System Tray Integration** - Minimize to system tray (coming soon)
- **Real-time Visualization** - Audio waveform display (coming soon)

## 🚀 Quick Start

### Installation

#### Option 1: Quick Install (Recommended)
```bash
# Clone the repository
git clone https://github.com/yourusername/wisprclone.git
cd wisprclone

# Run the installation script
python scripts/install.py
```

#### Option 2: Manual Install
```bash
# Install dependencies
pip install -r requirements.txt

# Install WisprClone
pip install -e .
```

#### Option 3: Using pip (when published)
```bash
pip install wisprclone
```

### Basic Usage

#### GUI Interface
```bash
# Launch the GUI (default)
wisprclone

# Or explicitly launch GUI
wisprclone --gui
```

#### CLI Interface
```bash
# Launch CLI
wisprclone --cli

# Quick 5-second recording
wisprclone --cli -r 5

# Transcribe an audio file
wisprclone --cli -f audio.wav

# Real-time transcription with specific model
wisprclone --cli --model small
```

## 📖 Documentation

### Command Line Options

#### Main Entry Point
```bash
wisprclone [OPTIONS]

Options:
  --gui                    Launch GUI interface (default)
  --cli                    Launch CLI interface
  --no-gui                 Force CLI interface
  --version                Show version information
  --config                 Show configuration file location
  --reset-config           Reset configuration to defaults
  --help                   Show help message
```

#### CLI Interface
```bash
wisprclone --cli [OPTIONS]

Mode Options:
  -f FILE, --file FILE     Transcribe an audio file
  -r DURATION              Quick recording mode (seconds)
  --devices                List available audio devices
  --benchmark [DURATION]   Benchmark model performance
  --stats                  Show transcription statistics

Configuration:
  -m MODEL, --model MODEL  Whisper model (tiny/base/small/medium/large)
  -l LANG, --language LANG Language code (en, es, fr, etc.)
  -d INDEX, --device INDEX Audio input device index
  --output-file FILE       Output file for transcriptions
  --clipboard              Copy transcriptions to clipboard
  --typing                 Enable typing simulation
  --no-console             Disable console output
```

### Configuration

WisprClone uses a JSON configuration file located at `~/.wisprclone/config.json`. You can customize all aspects of the application:

```json
{
  "audio": {
    "sample_rate": 16000,
    "chunk_size": 1024,
    "channels": 1,
    "device_index": null,
    "noise_reduction": true,
    "silence_threshold": 0.01,
    "silence_duration": 1.0
  },
  "whisper": {
    "model_size": "base",
    "language": null,
    "task": "transcribe",
    "temperature": 0.0,
    "no_speech_threshold": 0.6,
    "logprob_threshold": -1.0,
    "compression_ratio_threshold": 2.4
  },
  "output": {
    "output_to_console": true,
    "output_to_clipboard": false,
    "output_to_file": false,
    "output_file_path": "transcription.txt",
    "typing_enabled": false,
    "typing_delay": 0.01
  },
  "hotkeys": {
    "toggle_recording": "ctrl+shift+r",
    "stop_recording": "escape",
    "toggle_typing": "ctrl+shift+t",
    "clear_output": "ctrl+shift+c"
  },
  "ui": {
    "theme": "dark",
    "window_size": [800, 600],
    "always_on_top": false,
    "minimize_to_tray": true,
    "show_waveform": true
  }
}
```

### Programming API

WisprClone can be used programmatically in your own applications:

```python
from wisprclone.core.config import Config
from wisprclone.core.transcriber import WhisperTranscriber
from wisprclone.core.audio_processor import AudioProcessor

# Initialize components
config = Config()
transcriber = WhisperTranscriber(config)
audio_processor = AudioProcessor(config)

# Quick recording and transcription
audio_data = audio_processor.record_audio_chunk(5.0)
result = transcriber.transcribe_audio(audio_data, config.audio.sample_rate)

print(f"Transcription: {result['text']}")
print(f"Language: {result['language']}")
print(f"Confidence: {result['confidence']}")
```

See the `examples/` directory for more detailed examples.

## 🎬 Screenshots

### GUI Interface
![WisprClone GUI](https://via.placeholder.com/800x600/2b2b2b/ffffff?text=WisprClone+GUI+Interface)

### CLI Interface
```
🎤 WisprClone - Real-time transcription mode
Press Ctrl+C to stop
==================================================

[14:32:15] (en, 0.92, 0.45s)
📝 Hello, this is a test of the WisprClone speech recognition system.
--------------------------------------------------

[14:32:18] (en, 0.88, 0.52s)
📝 It's working really well and the accuracy is impressive.
--------------------------------------------------
```

## 🔧 Requirements

### System Requirements
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space (for models)
- **Audio**: Microphone or audio input device

### Platform-Specific Requirements

#### Windows
- Microsoft Visual C++ Build Tools
- Windows SDK

#### macOS
- Xcode Command Line Tools
- Homebrew (recommended)

#### Linux
- Build essentials (`gcc`, `make`)
- Audio development libraries (`portaudio19-dev`)
- FFmpeg

### Python Dependencies
All Python dependencies are listed in `requirements.txt`:

- `openai-whisper` - Core speech recognition
- `torch` / `torchaudio` - PyTorch for neural networks
- `sounddevice` / `soundfile` - Audio I/O
- `customtkinter` - Modern GUI framework
- `keyboard` - Global hotkey support
- `pyperclip` - Clipboard integration
- `scipy` / `librosa` - Audio processing
- `noisereduce` - Noise reduction
- And more...

## 🏗️ Architecture

WisprClone is built with a modular architecture:

```
wisprclone/
├── core/                   # Core functionality
│   ├── config.py          # Configuration management
│   ├── transcriber.py     # Whisper integration
│   └── audio_processor.py # Audio handling
├── utils/                  # Utility modules
│   ├── output_handler.py  # Output management
│   ├── hotkey_manager.py  # Hotkey handling
│   └── typing_simulator.py # Auto-typing
├── gui.py                 # GUI interface
├── cli.py                 # CLI interface
└── main.py               # Main entry point
```

### Key Components

- **Transcriber**: Manages Whisper models and transcription
- **AudioProcessor**: Handles audio input, preprocessing, and recording
- **OutputHandler**: Manages different output formats and logging
- **HotkeyManager**: Global keyboard shortcut management
- **Config**: Centralized configuration management

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/wisprclone.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate the environment: `source venv/bin/activate` (Unix) or `venv\Scripts\activate` (Windows)
5. Install in development mode: `pip install -e .`
6. Install development dependencies: `pip install -r requirements-dev.txt`

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=wisprclone
```

### Building

Use the build script to create distributable packages:

```bash
# Build wheel and source distribution
python scripts/build.py

# Build everything
python scripts/build.py --all

# Build standalone executable
python scripts/build.py --executable
```

## 🐛 Troubleshooting

### Common Issues

#### Audio Device Issues
```bash
# List available audio devices
wisprclone --cli --devices

# Test with specific device
wisprclone --cli --device 1
```

#### Model Download Issues
Models are downloaded automatically on first use. If you encounter issues:
```bash
# Check available models
python -c "import whisper; print(whisper.available_models())"

# Download manually
python -c "import whisper; whisper.load_model('base')"
```

#### Permission Issues (Linux/macOS)
```bash
# Add user to audio group (Linux)
sudo usermod -a -G audio $USER

# Fix microphone permissions (macOS)
# Go to System Preferences > Security & Privacy > Privacy > Microphone
```

### Performance Optimization

- Use smaller models (`tiny`, `base`) for faster processing
- Enable noise reduction for better accuracy in noisy environments
- Adjust silence thresholds for your speaking patterns
- Use GPU acceleration when available (CUDA/MPS)

## 📊 Model Comparison

| Model | Size | Speed | Accuracy | Use Case |
|-------|------|-------|----------|----------|
| tiny | 39 MB | ~32x realtime | Good | Quick transcription, low-power devices |
| base | 74 MB | ~16x realtime | Better | Balanced speed/accuracy |
| small | 244 MB | ~6x realtime | Good | Higher accuracy, moderate speed |
| medium | 769 MB | ~2x realtime | Very Good | High accuracy applications |
| large | 1550 MB | ~1x realtime | Excellent | Maximum accuracy, research |

## 🗺️ Roadmap

### Version 1.1 (Next Release)
- [ ] System tray integration
- [ ] Audio waveform visualization
- [ ] Plugin system for custom outputs
- [ ] WebRTC support for browser integration

### Version 1.2
- [ ] Real-time translation
- [ ] Speaker identification
- [ ] Custom model fine-tuning
- [ ] Cloud integration (AWS, Google Cloud)

### Version 2.0
- [ ] Multi-speaker transcription
- [ ] Video transcription support
- [ ] Advanced noise cancellation
- [ ] Mobile app support

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) - The amazing speech recognition model
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern GUI framework
- [PyTorch](https://pytorch.org/) - Deep learning framework
- All the open-source libraries that make this project possible

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/wisprclone/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/wisprclone/discussions)
- **Email**: support@wisprclone.com (coming soon)

## ⭐ Star History

If you find WisprClone useful, please consider giving it a star!

[![Star History Chart](https://api.star-history.com/svg?repos=Zinga18018/wisprclone&type=Date)](https://star-history.com/#Zinga18018/wisprclone&Date)

---

**Made with ❤️ by the WisprClone Team**

*Ready to transform your voice into text? Start transcribing with WisprClone today!* 
