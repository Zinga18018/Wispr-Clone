#!/usr/bin/env python3
"""
WisprClone Installation Script

This script helps users install WisprClone and its dependencies.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def run_command(command, description="", check=True):
    """Run a command and handle errors"""
    print(f"\n🔧 {description}...")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version} - Compatible")
    return True


def check_system_dependencies():
    """Check and install system dependencies"""
    system = platform.system().lower()
    
    print(f"\n🖥️  Detected system: {system}")
    
    if system == "windows":
        print("📝 On Windows, please ensure you have:")
        print("  - Microsoft Visual C++ Build Tools")
        print("  - Windows SDK")
        print("  - Git for Windows (for development)")
        
    elif system == "darwin":  # macOS
        print("🍎 Installing macOS dependencies...")
        
        # Check if Homebrew is installed
        if run_command("which brew", "Checking for Homebrew", check=False):
            run_command("brew install portaudio", "Installing PortAudio via Homebrew")
            run_command("brew install ffmpeg", "Installing FFmpeg via Homebrew")
        else:
            print("⚠️  Homebrew not found. Please install it from https://brew.sh/")
            print("   Then run: brew install portaudio ffmpeg")
            
    elif system == "linux":
        print("🐧 Installing Linux dependencies...")
        
        # Try to detect the distribution
        try:
            with open("/etc/os-release") as f:
                os_info = f.read().lower()
            
            if "ubuntu" in os_info or "debian" in os_info:
                run_command("sudo apt update", "Updating package list")
                run_command(
                    "sudo apt install -y python3-dev portaudio19-dev ffmpeg git",
                    "Installing system dependencies"
                )
            elif "fedora" in os_info or "rhel" in os_info or "centos" in os_info:
                run_command(
                    "sudo dnf install -y python3-devel portaudio-devel ffmpeg git",
                    "Installing system dependencies"
                )
            elif "arch" in os_info:
                run_command(
                    "sudo pacman -S python portaudio ffmpeg git",
                    "Installing system dependencies"
                )
            else:
                print("⚠️  Unknown Linux distribution. Please install manually:")
                print("   - python3-dev/python3-devel")
                print("   - portaudio19-dev/portaudio-devel")
                print("   - ffmpeg")
                print("   - git")
                
        except Exception as e:
            print(f"⚠️  Could not detect Linux distribution: {e}")


def install_python_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing Python dependencies...")
    
    # Upgrade pip first
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip"):
        print("⚠️  Failed to upgrade pip, continuing anyway...")
    
    # Install PyTorch first (platform-specific)
    system = platform.system().lower()
    
    if system == "darwin" and platform.machine() == "arm64":
        # Apple Silicon Mac
        print("🍎 Installing PyTorch for Apple Silicon...")
        torch_command = f"{sys.executable} -m pip install torch torchaudio"
    else:
        # Default PyTorch installation
        print("⚡ Installing PyTorch...")
        torch_command = f"{sys.executable} -m pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu"
    
    if not run_command(torch_command, "Installing PyTorch"):
        print("❌ Failed to install PyTorch. This may cause issues.")
    
    # Install other dependencies
    requirements_path = Path(__file__).parent.parent / "requirements.txt"
    
    if requirements_path.exists():
        if not run_command(
            f"{sys.executable} -m pip install -r {requirements_path}",
            "Installing WisprClone dependencies"
        ):
            print("❌ Failed to install some dependencies")
            return False
    else:
        print("⚠️  requirements.txt not found, installing core dependencies...")
        core_deps = [
            "openai-whisper",
            "sounddevice",
            "soundfile",
            "pyaudio",
            "pydub",
            "keyboard",
            "pyperclip",
            "scipy",
            "librosa",
            "noisereduce",
            "customtkinter",
            "Pillow",
            "requests"
        ]
        
        for dep in core_deps:
            run_command(
                f"{sys.executable} -m pip install {dep}",
                f"Installing {dep}",
                check=False
            )
    
    return True


def install_wisprclone():
    """Install WisprClone package"""
    print("\n📱 Installing WisprClone...")
    
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    
    # Install in development mode
    return run_command(
        f"{sys.executable} -m pip install -e {project_root}",
        "Installing WisprClone package"
    )


def download_whisper_models():
    """Download basic Whisper models"""
    print("\n🤖 Downloading Whisper models...")
    
    try:
        import whisper
        
        # Download small model by default
        print("📥 Downloading 'base' model (recommended for most users)...")
        model = whisper.load_model("base")
        print("✅ Base model downloaded successfully")
        
        # Optionally download tiny model for faster processing
        print("📥 Downloading 'tiny' model (for fast processing)...")
        model = whisper.load_model("tiny")
        print("✅ Tiny model downloaded successfully")
        
        return True
        
    except Exception as e:
        print(f"⚠️  Could not download models: {e}")
        print("   Models will be downloaded automatically when first used")
        return False


def test_installation():
    """Test if installation was successful"""
    print("\n🧪 Testing installation...")
    
    try:
        # Test basic imports
        import wisprclone
        print("✅ WisprClone package imported successfully")
        
        # Test core components
        from wisprclone.core.config import Config
        config = Config()
        print("✅ Configuration system working")
        
        # Test audio system
        from wisprclone.core.audio_processor import AudioProcessor
        audio_processor = AudioProcessor(config)
        devices = audio_processor.get_available_devices()
        print(f"✅ Audio system working ({len(devices)} input devices found)")
        
        # Test Whisper
        from wisprclone.core.transcriber import WhisperTranscriber
        transcriber = WhisperTranscriber(config)
        if transcriber.model:
            print("✅ Whisper model loaded successfully")
        else:
            print("⚠️  Whisper model failed to load")
        
        return True
        
    except Exception as e:
        print(f"❌ Installation test failed: {e}")
        return False


def create_desktop_shortcuts():
    """Create desktop shortcuts (platform-specific)"""
    print("\n🖥️  Creating desktop shortcuts...")
    
    system = platform.system().lower()
    
    if system == "windows":
        # Windows shortcut creation would go here
        print("📝 On Windows, you can create shortcuts manually:")
        print("   - Right-click on desktop > New > Shortcut")
        print(f"   - Target: {sys.executable} -m wisprclone")
        
    elif system == "darwin":  # macOS
        print("🍎 On macOS, you can add WisprClone to Applications:")
        print("   - Use Automator to create an Application")
        print(f"   - Shell script: {sys.executable} -m wisprclone")
        
    elif system == "linux":
        # Create .desktop file
        desktop_entry = f"""[Desktop Entry]
Name=WisprClone
Comment=AI Speech Recognition
Exec={sys.executable} -m wisprclone
Icon=audio-input-microphone
Terminal=false
Type=Application
Categories=AudioVideo;Audio;
"""
        
        desktop_path = Path.home() / ".local/share/applications/wisprclone.desktop"
        try:
            desktop_path.parent.mkdir(parents=True, exist_ok=True)
            desktop_path.write_text(desktop_entry)
            os.chmod(desktop_path, 0o755)
            print(f"✅ Desktop shortcut created: {desktop_path}")
        except Exception as e:
            print(f"⚠️  Could not create desktop shortcut: {e}")


def main():
    """Main installation function"""
    print("🎤 WisprClone Installation Script")
    print("=" * 40)
    
    # Step 1: Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Step 2: Check system dependencies
    check_system_dependencies()
    
    # Step 3: Install Python dependencies
    if not install_python_dependencies():
        print("\n❌ Failed to install Python dependencies")
        sys.exit(1)
    
    # Step 4: Install WisprClone
    if not install_wisprclone():
        print("\n❌ Failed to install WisprClone")
        sys.exit(1)
    
    # Step 5: Download models
    download_whisper_models()
    
    # Step 6: Test installation
    if not test_installation():
        print("\n❌ Installation test failed")
        sys.exit(1)
    
    # Step 7: Create shortcuts
    create_desktop_shortcuts()
    
    # Success message
    print("\n" + "=" * 50)
    print("🎉 WisprClone installed successfully!")
    print("=" * 50)
    print("\n📚 Quick Start:")
    print("  wisprclone                    # Launch GUI")
    print("  wisprclone --cli              # Launch CLI")
    print("  wisprclone --help             # Show help")
    print("\n🔧 Configuration:")
    print("  wisprclone --config           # Show config info")
    print("  wisprclone --reset-config     # Reset to defaults")
    print("\n📖 For more information, see the README.md file")
    print("\n🎤 Ready to transcribe! Enjoy using WisprClone!")


if __name__ == "__main__":
    main() 