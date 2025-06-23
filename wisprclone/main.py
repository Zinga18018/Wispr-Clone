import sys
import argparse
from pathlib import Path

from .core.config import Config


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for main entry point"""
    parser = argparse.ArgumentParser(
        description="WisprClone - A powerful, real-time speech-to-text application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Interface Options:
  --gui                               Launch GUI interface (default)
  --cli                               Launch CLI interface
  --no-gui                            Force CLI interface

Examples:
  wisprclone                          # Launch GUI
  wisprclone --cli                    # Launch CLI
  wisprclone --cli -f audio.wav       # Transcribe file with CLI
  wisprclone --gui                    # Launch GUI explicitly
        """
    )
    
    # Interface selection
    interface_group = parser.add_mutually_exclusive_group()
    interface_group.add_argument(
        "--gui",
        action="store_true",
        help="Launch GUI interface (default)"
    )
    interface_group.add_argument(
        "--cli",
        action="store_true",
        help="Launch CLI interface"
    )
    interface_group.add_argument(
        "--no-gui",
        action="store_true",
        help="Force CLI interface (disable GUI)"
    )
    
    # Quick actions
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version information"
    )
    parser.add_argument(
        "--config",
        action="store_true",
        help="Show configuration file location"
    )
    parser.add_argument(
        "--reset-config",
        action="store_true",
        help="Reset configuration to defaults"
    )
    
    return parser


def show_version():
    """Show version information"""
    from . import __version__, __author__
    
    print(f"WisprClone v{__version__}")
    print(f"Author: {__author__}")
    print("A powerful, real-time speech-to-text application using OpenAI Whisper")
    print()
    
    # Show system information
    try:
        import torch
        print(f"PyTorch: {torch.__version__}")
        print(f"CUDA Available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"CUDA Device: {torch.cuda.get_device_name()}")
    except ImportError:
        print("PyTorch: Not installed")
    
    try:
        import whisper
        print("OpenAI Whisper: Available")
    except ImportError:
        print("OpenAI Whisper: Not installed")


def show_config_info():
    """Show configuration information"""
    config = Config()
    
    print("WisprClone Configuration")
    print("=" * 30)
    print(f"Config file: {config.config_path}")
    print(f"Model directory: {config.get_whisper_model_path()}")
    print()
    print(f"Current model: {config.whisper.model_size}")
    print(f"Language: {config.whisper.language or 'Auto-detect'}")
    print(f"Audio device: {config.audio.device_index or 'Default'}")
    print(f"Sample rate: {config.audio.sample_rate} Hz")
    print()
    print("Output settings:")
    print(f"  Console: {config.output.output_to_console}")
    print(f"  Clipboard: {config.output.output_to_clipboard}")
    print(f"  File: {config.output.output_to_file}")
    print(f"  Typing: {config.output.typing_enabled}")


def reset_config():
    """Reset configuration to defaults"""
    try:
        config = Config()
        config.reset_to_defaults()
        print("Configuration reset to defaults successfully!")
        print(f"Config file: {config.config_path}")
    except Exception as e:
        print(f"Error resetting configuration: {e}")
        sys.exit(1)


def check_dependencies():
    """Check if required dependencies are available"""
    missing_deps = []
    
    try:
        import whisper
    except ImportError:
        missing_deps.append("openai-whisper")
    
    try:
        import torch
    except ImportError:
        missing_deps.append("torch")
    
    try:
        import sounddevice
    except ImportError:
        missing_deps.append("sounddevice")
    
    try:
        import numpy
    except ImportError:
        missing_deps.append("numpy")
    
    if missing_deps:
        print("Missing required dependencies:")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("\nPlease install missing dependencies:")
        print("pip install -r requirements.txt")
        return False
    
    return True


def launch_gui():
    """Launch GUI interface"""
    try:
        # Check if GUI dependencies are available
        import customtkinter
        import tkinter
        
        from .gui import main as gui_main
        print("Launching WisprClone GUI...")
        gui_main()
        
    except ImportError as e:
        print(f"GUI dependencies not available: {e}")
        print("Falling back to CLI interface...")
        launch_cli()
    except Exception as e:
        print(f"Failed to launch GUI: {e}")
        print("Falling back to CLI interface...")
        launch_cli()


def launch_cli():
    """Launch CLI interface"""
    try:
        from .cli import main as cli_main
        cli_main()
    except Exception as e:
        print(f"Failed to launch CLI: {e}")
        sys.exit(1)


def detect_environment():
    """Detect if GUI is available in current environment"""
    try:
        # Check if display is available (Linux/macOS)
        import os
        if os.name == 'posix' and 'DISPLAY' not in os.environ:
            return False
        
        # Try to import GUI dependencies
        import tkinter
        import customtkinter
        
        # Test if GUI can be created
        root = tkinter.Tk()
        root.withdraw()  # Hide window
        root.destroy()
        
        return True
        
    except Exception:
        return False


def main():
    """Main entry point for WisprClone"""
    parser = create_parser()
    
    # Parse known args to handle CLI passthrough
    args, unknown_args = parser.parse_known_args()
    
    # Handle quick actions
    if args.version:
        show_version()
        return
    
    if args.config:
        show_config_info()
        return
    
    if args.reset_config:
        reset_config()
        return
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Determine interface to launch
    if args.cli or args.no_gui:
        # CLI requested or GUI disabled
        launch_cli()
    elif args.gui:
        # GUI explicitly requested
        launch_gui()
    else:
        # Auto-detect best interface
        if detect_environment():
            launch_gui()
        else:
            print("GUI not available in current environment, launching CLI...")
            launch_cli()


if __name__ == "__main__":
    main() 