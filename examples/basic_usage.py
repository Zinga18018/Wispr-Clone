#!/usr/bin/env python3
"""
WisprClone Basic Usage Examples

This file demonstrates how to use WisprClone programmatically.
"""

import time
import numpy as np
from pathlib import Path

# Import WisprClone components
from wisprclone.core.config import Config
from wisprclone.core.transcriber import WhisperTranscriber
from wisprclone.core.audio_processor import AudioProcessor
from wisprclone.utils.output_handler import OutputHandler


def example_file_transcription():
    """Example: Transcribe an audio file"""
    print("🎵 Example: File Transcription")
    print("=" * 40)
    
    # Initialize configuration
    config = Config()
    
    # Initialize transcriber
    transcriber = WhisperTranscriber(config)
    
    # Example file path (replace with your audio file)
    audio_file = "path/to/your/audio.wav"
    
    if Path(audio_file).exists():
        print(f"Transcribing: {audio_file}")
        
        # Transcribe the file
        result = transcriber.transcribe_file(audio_file)
        
        if "error" not in result:
            print(f"✅ Transcription: {result['text']}")
            print(f"Language: {result['language']}")
            print(f"Confidence: {result['confidence']:.2f}")
            print(f"Processing time: {result['processing_time']:.2f}s")
        else:
            print(f"❌ Error: {result['error']}")
    else:
        print(f"⚠️  File not found: {audio_file}")
        print("Please replace 'audio_file' with a valid audio file path")


def example_quick_recording():
    """Example: Quick recording and transcription"""
    print("\n🎤 Example: Quick Recording")
    print("=" * 40)
    
    # Initialize components
    config = Config()
    transcriber = WhisperTranscriber(config)
    audio_processor = AudioProcessor(config)
    
    print("Recording 5 seconds of audio...")
    print("Speak now!")
    
    # Record audio
    audio_data = audio_processor.record_audio_chunk(5.0)
    
    if audio_data is not None:
        print("Recording complete. Transcribing...")
        
        # Transcribe audio
        result = transcriber.transcribe_audio(audio_data, config.audio.sample_rate)
        
        if "error" not in result:
            print(f"✅ Transcription: {result['text']}")
            print(f"Language: {result['language']}")
            print(f"Confidence: {result['confidence']:.2f}")
        else:
            print(f"❌ Error: {result['error']}")
    else:
        print("❌ Failed to record audio")


def example_real_time_transcription():
    """Example: Real-time transcription with callback"""
    print("\n🔄 Example: Real-time Transcription")
    print("=" * 40)
    
    # Initialize components
    config = Config()
    transcriber = WhisperTranscriber(config)
    audio_processor = AudioProcessor(config)
    output_handler = OutputHandler(config)
    
    # Define transcription callback
    def transcription_callback(result):
        print(f"🎯 Real-time result: {result.get('text', 'No text')}")
        # Handle the result (save, display, etc.)
        output_handler.handle_transcription(result)
    
    # Define audio callback
    def audio_callback(audio_data, sample_rate):
        # Queue audio for transcription
        transcriber.queue_audio_for_transcription(audio_data, sample_rate)
    
    print("Starting real-time transcription...")
    print("Speak for 10 seconds, then it will stop automatically")
    
    try:
        # Start real-time transcription
        transcriber.start_real_time_transcription(transcription_callback)
        audio_processor.start_recording(audio_callback)
        
        # Record for 10 seconds
        time.sleep(10)
        
    finally:
        # Stop transcription
        audio_processor.stop_recording()
        transcriber.stop_real_time_transcription()
        output_handler.close()
        
        print("Real-time transcription stopped")


def example_language_detection():
    """Example: Language detection"""
    print("\n🌍 Example: Language Detection")
    print("=" * 40)
    
    # Initialize components
    config = Config()
    transcriber = WhisperTranscriber(config)
    audio_processor = AudioProcessor(config)
    
    print("Recording 5 seconds for language detection...")
    print("Speak in any language!")
    
    # Record audio
    audio_data = audio_processor.record_audio_chunk(5.0)
    
    if audio_data is not None:
        print("Detecting language...")
        
        # Detect language
        language, confidence = transcriber.detect_language(audio_data, config.audio.sample_rate)
        
        print(f"✅ Detected language: {language}")
        print(f"Confidence: {confidence:.2f}")
        
        # Now transcribe with detected language
        result = transcriber.transcribe_audio(
            audio_data, 
            config.audio.sample_rate, 
            language=language
        )
        
        if "error" not in result:
            print(f"📝 Transcription: {result['text']}")
        else:
            print(f"❌ Transcription error: {result['error']}")
    else:
        print("❌ Failed to record audio")


def example_batch_processing():
    """Example: Batch process multiple files"""
    print("\n📁 Example: Batch Processing")
    print("=" * 40)
    
    # Initialize components
    config = Config()
    transcriber = WhisperTranscriber(config)
    
    # Example: process all WAV files in a directory
    audio_dir = Path("path/to/audio/files")  # Replace with your directory
    
    if audio_dir.exists():
        audio_files = list(audio_dir.glob("*.wav")) + list(audio_dir.glob("*.mp3"))
        
        if audio_files:
            print(f"Found {len(audio_files)} audio files")
            
            results = []
            for audio_file in audio_files:
                print(f"\nProcessing: {audio_file.name}")
                
                result = transcriber.transcribe_file(str(audio_file))
                results.append({
                    "file": audio_file.name,
                    "result": result
                })
                
                if "error" not in result:
                    print(f"✅ {result['text'][:100]}...")
                else:
                    print(f"❌ Error: {result['error']}")
            
            # Save results to file
            import json
            results_file = audio_dir / "transcription_results.json"
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            print(f"\n📄 Results saved to: {results_file}")
        else:
            print("No audio files found in directory")
    else:
        print(f"⚠️  Directory not found: {audio_dir}")
        print("Please replace 'audio_dir' with a valid directory path")


def example_model_comparison():
    """Example: Compare different Whisper models"""
    print("\n⚖️  Example: Model Comparison")
    print("=" * 40)
    
    # Models to compare
    models = ["tiny", "base", "small"]
    
    # Initialize audio processor
    config = Config()
    audio_processor = AudioProcessor(config)
    
    print("Recording 5 seconds for model comparison...")
    audio_data = audio_processor.record_audio_chunk(5.0)
    
    if audio_data is not None:
        results = {}
        
        for model_size in models:
            print(f"\n🤖 Testing {model_size} model...")
            
            # Update config and create new transcriber
            config.whisper.model_size = model_size
            transcriber = WhisperTranscriber(config)
            
            # Transcribe with this model
            result = transcriber.transcribe_audio(audio_data, config.audio.sample_rate)
            
            if "error" not in result:
                results[model_size] = {
                    "text": result["text"],
                    "processing_time": result["processing_time"],
                    "confidence": result["confidence"],
                    "real_time_factor": result["real_time_factor"]
                }
                
                print(f"✅ {model_size}: {result['text'][:50]}...")
                print(f"   Time: {result['processing_time']:.2f}s")
                print(f"   RTF: {result['real_time_factor']:.2f}x")
                print(f"   Confidence: {result['confidence']:.2f}")
            else:
                print(f"❌ {model_size} failed: {result['error']}")
        
        # Show comparison
        print("\n📊 Model Comparison Summary:")
        print("-" * 40)
        for model, data in results.items():
            print(f"{model:8} | {data['processing_time']:6.2f}s | {data['real_time_factor']:6.2f}x | {data['confidence']:6.2f}")
    else:
        print("❌ Failed to record audio")


def example_custom_configuration():
    """Example: Custom configuration"""
    print("\n⚙️  Example: Custom Configuration")
    print("=" * 40)
    
    # Create custom configuration
    config = Config()
    
    # Modify audio settings
    config.audio.sample_rate = 16000
    config.audio.noise_reduction = True
    config.audio.silence_threshold = 0.02
    
    # Modify Whisper settings
    config.whisper.model_size = "small"
    config.whisper.language = "en"  # Force English
    config.whisper.temperature = 0.0  # More deterministic
    
    # Modify output settings
    config.output.output_to_console = True
    config.output.output_to_clipboard = True
    config.output.output_to_file = True
    config.output.output_file_path = "custom_transcription.txt"
    
    # Save configuration
    config.save()
    
    print("✅ Custom configuration saved")
    print(f"Config file: {config.config_path}")
    
    # Use the custom configuration
    transcriber = WhisperTranscriber(config)
    audio_processor = AudioProcessor(config)
    output_handler = OutputHandler(config)
    
    print("Configuration applied successfully!")


def main():
    """Run all examples"""
    print("🎤 WisprClone Programming Examples")
    print("=" * 50)
    
    examples = [
        example_custom_configuration,
        example_file_transcription,
        example_quick_recording,
        example_language_detection,
        example_batch_processing,
        example_model_comparison,
        example_real_time_transcription,
    ]
    
    for i, example in enumerate(examples, 1):
        try:
            print(f"\n[{i}/{len(examples)}] Running {example.__name__}...")
            example()
        except KeyboardInterrupt:
            print("\n⏹️  Stopped by user")
            break
        except Exception as e:
            print(f"❌ Example failed: {e}")
            continue
        
        if i < len(examples):
            input("\nPress Enter to continue to next example...")
    
    print("\n🎉 All examples completed!")


if __name__ == "__main__":
    main() 