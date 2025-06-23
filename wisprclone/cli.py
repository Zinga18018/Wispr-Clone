import argparse
import sys
import time
import signal
import threading
from pathlib import Path
from typing import Optional

from .core.config import Config
from .core.transcriber import WhisperTranscriber
from .core.audio_processor import AudioProcessor
from .utils.output_handler import OutputHandler
from .utils.hotkey_manager import HotkeyManager


class WisprCloneCLI:
    """Command-line interface for WisprClone"""
    
    def __init__(self):
        self.config = Config()
        self.transcriber = None
        self.audio_processor = None
        self.output_handler = None
        self.hotkey_manager = None
        self.running = False
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle interrupt signals"""
        print("\nShutting down WisprClone...")
        self.stop()
        sys.exit(0)
    
    def initialize(self) -> bool:
        """Initialize all components"""
        try:
            print("Initializing WisprClone...")
            
            # Initialize transcriber
            self.transcriber = WhisperTranscriber(self.config)
            if not self.transcriber.model:
                print("Failed to load Whisper model")
                return False
            
            # Initialize audio processor
            self.audio_processor = AudioProcessor(self.config)
            
            # Initialize output handler
            self.output_handler = OutputHandler(self.config)
            
            # Initialize hotkey manager
            self.hotkey_manager = HotkeyManager(self.config)
            
            print("WisprClone initialized successfully!")
            return True
            
        except Exception as e:
            print(f"Initialization failed: {e}")
            return False
    
    def run_real_time(self) -> None:
        """Run real-time transcription mode"""
        if not self.initialize():
            return
        
        print("\n🎤 Real-time transcription mode")
        print("Press Ctrl+C to stop")
        print("=" * 50)
        
        try:
            # Setup transcription callback
            def transcription_callback(result):
                self.output_handler.handle_transcription(result)
            
            # Setup audio callback
            def audio_callback(audio_data, sample_rate):
                self.transcriber.queue_audio_for_transcription(audio_data, sample_rate)
            
            # Setup hotkeys
            hotkey_callbacks = {
                "toggle_recording": self._toggle_recording,
                "stop_recording": self._stop_recording,
                "toggle_typing": self._toggle_typing,
                "clear_output": self._clear_output
            }
            self.hotkey_manager.setup_default_hotkeys(hotkey_callbacks)
            
            # Start real-time transcription
            self.transcriber.start_real_time_transcription(transcription_callback)
            self.audio_processor.start_recording(audio_callback)
            
            self.running = True
            
            # Keep running until stopped
            while self.running:
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()
    
    def run_file_transcription(self, file_path: str, language: Optional[str] = None) -> None:
        """Transcribe an audio file"""
        if not self.initialize():
            return
        
        print(f"\n📁 Transcribing file: {file_path}")
        
        if not Path(file_path).exists():
            print(f"Error: File not found: {file_path}")
            return
        
        try:
            # Transcribe file
            result = self.transcriber.transcribe_file(file_path, language=language)
            
            # Handle result
            self.output_handler.handle_transcription(result)
            
            if "error" not in result:
                print(f"\n✅ Transcription completed successfully!")
                print(f"Processing time: {result.get('processing_time', 0):.2f}s")
                print(f"Audio duration: {result.get('audio_duration', 0):.2f}s")
                print(f"Language: {result.get('language', 'unknown')}")
                print(f"Confidence: {result.get('confidence', 0):.2f}")
            
        except Exception as e:
            print(f"Error transcribing file: {e}")
    
    def run_quick_recording(self, duration: float = 5.0) -> None:
        """Record and transcribe audio for specified duration"""
        if not self.initialize():
            return
        
        print(f"\n🎤 Quick recording mode ({duration} seconds)")
        print("Recording will start in 3 seconds...")
        
        # Countdown
        for i in range(3, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        
        try:
            # Record audio
            audio_data = self.audio_processor.record_audio_chunk(duration)
            
            if audio_data is None:
                print("Failed to record audio")
                return
            
            print("Recording complete. Transcribing...")
            
            # Transcribe audio
            result = self.transcriber.transcribe_audio(audio_data, self.config.audio.sample_rate)
            
            # Handle result
            self.output_handler.handle_transcription(result)
            
            if "error" not in result:
                print(f"\n✅ Transcription completed!")
                print(f"Processing time: {result.get('processing_time', 0):.2f}s")
                print(f"Language: {result.get('language', 'unknown')}")
                print(f"Confidence: {result.get('confidence', 0):.2f}")
            
        except Exception as e:
            print(f"Error in quick recording: {e}")
    
    def list_audio_devices(self) -> None:
        """List available audio input devices"""
        print("\n🎧 Available audio input devices:")
        print("=" * 50)
        
        if not self.audio_processor:
            self.audio_processor = AudioProcessor(self.config)
        
        devices = self.audio_processor.get_available_devices()
        
        if not devices:
            print("No audio input devices found")
            return
        
        for device in devices:
            print(f"Device {device['index']}: {device['name']}")
            print(f"  Channels: {device['channels']}")
            print(f"  Sample Rate: {device['sample_rate']}")
            print()
    
    def benchmark_model(self, duration: float = 10.0) -> None:
        """Benchmark current Whisper model"""
        if not self.initialize():
            return
        
        print(f"\n⚡ Benchmarking Whisper model: {self.config.whisper.model_size}")
        
        result = self.transcriber.benchmark_model(duration)
        
        if "error" in result:
            print(f"Benchmark failed: {result['error']}")
            return
        
        print(f"✅ Benchmark completed!")
        print(f"Model: {result['model_size']}")
        print(f"Device: {result['device']}")
        print(f"Test duration: {result['test_duration']:.2f}s")
        print(f"Processing time: {result['processing_time']:.2f}s")
        print(f"Real-time factor: {result['real_time_factor']:.2f}x")
        
        if result['real_time_factor'] < 1.0:
            print("🚀 Model can process audio faster than real-time!")
        else:
            print("⚠️  Model processes slower than real-time")
    
    def show_statistics(self) -> None:
        """Show transcription statistics"""
        if not self.transcriber:
            print("No transcription statistics available")
            return
        
        stats = self.transcriber.get_statistics()
        
        print("\n📊 Transcription Statistics:")
        print("=" * 30)
        print(f"Total transcriptions: {stats.get('total_transcriptions', 0)}")
        print(f"Total processing time: {stats.get('total_processing_time', 0):.2f}s")
        print(f"Average processing time: {stats.get('average_processing_time', 0):.2f}s")
        print(f"Total audio duration: {stats.get('total_audio_duration', 0):.2f}s")
        print(f"Real-time factor: {stats.get('real_time_factor', 0):.2f}x")
        
        if self.output_handler:
            session_stats = self.output_handler.get_session_statistics()
            if session_stats:
                print(f"\n📝 Session Statistics:")
                print(f"Total entries: {session_stats.get('total_entries', 0)}")
                print(f"Total words: {session_stats.get('total_words', 0)}")
                print(f"Total characters: {session_stats.get('total_characters', 0)}")
                print(f"Average confidence: {session_stats.get('average_confidence', 0):.2f}")
                print(f"Words per minute: {session_stats.get('words_per_minute', 0):.1f}")
    
    def _toggle_recording(self) -> None:
        """Hotkey callback to toggle recording"""
        if self.audio_processor and self.audio_processor.is_recording:
            print("\n⏹️  Stopping recording...")
            self.audio_processor.stop_recording()
        else:
            print("\n▶️  Starting recording...")
            def audio_callback(audio_data, sample_rate):
                self.transcriber.queue_audio_for_transcription(audio_data, sample_rate)
            self.audio_processor.start_recording(audio_callback)
    
    def _stop_recording(self) -> None:
        """Hotkey callback to stop recording"""
        if self.audio_processor and self.audio_processor.is_recording:
            print("\n⏹️  Recording stopped")
            self.audio_processor.stop_recording()
    
    def _toggle_typing(self) -> None:
        """Hotkey callback to toggle typing simulation"""
        if self.config.output.typing_enabled:
            self.config.output.typing_enabled = False
            print("\n⌨️  Typing simulation disabled")
        else:
            self.config.output.typing_enabled = True
            print("\n⌨️  Typing simulation enabled")
        self.config.save()
    
    def _clear_output(self) -> None:
        """Hotkey callback to clear output"""
        if self.output_handler:
            self.output_handler.clear_session_log()
            print("\n🗑️  Output cleared")
    
    def stop(self) -> None:
        """Stop all components"""
        self.running = False
        
        if self.audio_processor:
            self.audio_processor.stop_recording()
        
        if self.transcriber:
            self.transcriber.stop_real_time_transcription()
        
        if self.hotkey_manager:
            self.hotkey_manager.cleanup()
        
        if self.output_handler:
            self.output_handler.close()


def create_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser"""
    parser = argparse.ArgumentParser(
        description="WisprClone - A powerful, real-time speech-to-text application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  wisprclone-cli                          # Start real-time transcription
  wisprclone-cli -f audio.wav             # Transcribe a file
  wisprclone-cli -r 10                    # Quick 10-second recording
  wisprclone-cli --benchmark              # Benchmark current model
  wisprclone-cli --devices                # List audio devices
  wisprclone-cli --stats                  # Show statistics
        """
    )
    
    # Mode selection
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "-f", "--file",
        help="Transcribe an audio file"
    )
    mode_group.add_argument(
        "-r", "--record",
        type=float,
        metavar="DURATION",
        help="Quick recording mode (duration in seconds)"
    )
    mode_group.add_argument(
        "--devices",
        action="store_true",
        help="List available audio input devices"
    )
    mode_group.add_argument(
        "--benchmark",
        nargs="?",
        const=10.0,
        type=float,
        metavar="DURATION",
        help="Benchmark model performance (default: 10 seconds)"
    )
    mode_group.add_argument(
        "--stats",
        action="store_true",
        help="Show transcription statistics"
    )
    
    # Configuration options
    parser.add_argument(
        "-m", "--model",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size"
    )
    parser.add_argument(
        "-l", "--language",
        help="Language code for transcription (e.g., en, es, fr)"
    )
    parser.add_argument(
        "-d", "--device",
        type=int,
        help="Audio input device index"
    )
    parser.add_argument(
        "--output-file",
        help="Output file for transcriptions"
    )
    parser.add_argument(
        "--clipboard",
        action="store_true",
        help="Copy transcriptions to clipboard"
    )
    parser.add_argument(
        "--typing",
        action="store_true",
        help="Enable typing simulation"
    )
    parser.add_argument(
        "--no-console",
        action="store_true",
        help="Disable console output"
    )
    
    return parser


def main():
    """Main CLI entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    # Create CLI instance
    cli = WisprCloneCLI()
    
    # Apply command-line arguments to config
    if args.model:
        cli.config.whisper.model_size = args.model
    if args.language:
        cli.config.whisper.language = args.language
    if args.device is not None:
        cli.config.audio.device_index = args.device
    if args.output_file:
        cli.config.output.output_to_file = True
        cli.config.output.output_file_path = args.output_file
    if args.clipboard:
        cli.config.output.output_to_clipboard = True
    if args.typing:
        cli.config.output.typing_enabled = True
    if args.no_console:
        cli.config.output.output_to_console = False
    
    # Save updated config
    cli.config.save()
    
    # Execute requested mode
    try:
        if args.devices:
            cli.list_audio_devices()
        elif args.benchmark is not None:
            cli.benchmark_model(args.benchmark)
        elif args.stats:
            cli.show_statistics()
        elif args.file:
            cli.run_file_transcription(args.file, args.language)
        elif args.record is not None:
            cli.run_quick_recording(args.record)
        else:
            # Default: real-time mode
            cli.run_real_time()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 