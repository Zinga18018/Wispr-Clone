import whisper
import torch
import numpy as np
import threading
import time
from typing import Optional, Dict, List, Callable, Tuple
import os
from pathlib import Path
from .config import Config


class WhisperTranscriber:
    """Main transcription engine using OpenAI Whisper"""
    
    def __init__(self, config: Config):
        self.config = config
        self.model = None
        self.model_size = None
        self.device = self._get_optimal_device()
        self.is_processing = False
        self.processing_queue = []
        self.processing_thread = None
        self.transcription_callback = None
        
        # Load the initial model
        self.load_model(config.whisper.model_size)
        
        # Statistics
        self.stats = {
            'total_transcriptions': 0,
            'total_processing_time': 0,
            'average_processing_time': 0,
            'total_audio_duration': 0
        }
    
    def _get_optimal_device(self) -> str:
        """Determine the best device for processing"""
        if torch.cuda.is_available():
            device = "cuda"
            print(f"Using CUDA GPU: {torch.cuda.get_device_name()}")
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            device = "mps"
            print("Using Apple Metal Performance Shaders (MPS)")
        else:
            device = "cpu"
            print("Using CPU for processing")
        
        return device
    
    def load_model(self, model_size: str) -> bool:
        """Load Whisper model"""
        try:
            print(f"Loading Whisper model: {model_size}")
            start_time = time.time()
            
            # Set model download directory
            model_dir = self.config.get_whisper_model_path()
            os.environ['WHISPER_CACHE_DIR'] = model_dir
            
            # Load model
            self.model = whisper.load_model(
                model_size, 
                device=self.device,
                download_root=model_dir
            )
            self.model_size = model_size
            
            load_time = time.time() - start_time
            print(f"Model loaded in {load_time:.2f} seconds")
            
            # Update config
            self.config.whisper.model_size = model_size
            self.config.save()
            
            return True
            
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def get_model_info(self) -> Dict:
        """Get information about the current model"""
        if self.model is None:
            return {}
        
        return {
            'model_size': self.model_size,
            'device': self.device,
            'dimensions': self.model.dims.n_mels if hasattr(self.model, 'dims') else 'Unknown',
            'parameters': sum(p.numel() for p in self.model.parameters()) if self.model else 0,
            'languages': self.config.get_supported_languages()
        }
    
    def transcribe_audio(self, 
                        audio_data: np.ndarray, 
                        sample_rate: int = 16000,
                        language: Optional[str] = None,
                        task: str = "transcribe") -> Dict:
        """Transcribe audio data"""
        if self.model is None:
            return {"error": "Model not loaded"}
        
        try:
            start_time = time.time()
            
            # Prepare audio data
            if sample_rate != 16000:
                # Whisper expects 16kHz audio
                import librosa
                audio_data = librosa.resample(audio_data, orig_sr=sample_rate, target_sr=16000)
                sample_rate = 16000
            
            # Ensure audio is float32 and in correct range
            if audio_data.dtype != np.float32:
                audio_data = audio_data.astype(np.float32)
            
            # Normalize to [-1, 1] range
            if np.max(np.abs(audio_data)) > 1.0:
                audio_data = audio_data / np.max(np.abs(audio_data))
            
            # Configure transcription options
            options = {
                "language": language or self.config.whisper.language,
                "task": task or self.config.whisper.task,
                "temperature": self.config.whisper.temperature,
                "no_speech_threshold": self.config.whisper.no_speech_threshold,
                "logprob_threshold": self.config.whisper.logprob_threshold,
                "compression_ratio_threshold": self.config.whisper.compression_ratio_threshold,
            }
            
            # Remove None values
            options = {k: v for k, v in options.items() if v is not None}
            
            # Perform transcription
            result = self.model.transcribe(audio_data, **options)
            
            processing_time = time.time() - start_time
            audio_duration = len(audio_data) / sample_rate
            
            # Update statistics
            self.stats['total_transcriptions'] += 1
            self.stats['total_processing_time'] += processing_time
            self.stats['total_audio_duration'] += audio_duration
            self.stats['average_processing_time'] = (
                self.stats['total_processing_time'] / self.stats['total_transcriptions']
            )
            
            # Prepare result
            transcription_result = {
                "text": result["text"].strip(),
                "language": result.get("language", "unknown"),
                "confidence": self._calculate_confidence(result),
                "processing_time": processing_time,
                "audio_duration": audio_duration,
                "real_time_factor": processing_time / audio_duration if audio_duration > 0 else 0,
                "segments": result.get("segments", []),
                "model_size": self.model_size,
                "timestamp": time.time()
            }
            
            return transcription_result
            
        except Exception as e:
            return {
                "error": f"Transcription failed: {str(e)}",
                "timestamp": time.time()
            }
    
    def _calculate_confidence(self, result: Dict) -> float:
        """Calculate confidence score from transcription result"""
        try:
            if "segments" in result and result["segments"]:
                # Calculate average probability from segments
                total_prob = 0
                total_tokens = 0
                
                for segment in result["segments"]:
                    if "tokens" in segment:
                        for token in segment["tokens"]:
                            if isinstance(token, dict) and "logprob" in token:
                                total_prob += np.exp(token["logprob"])
                                total_tokens += 1
                
                if total_tokens > 0:
                    return total_prob / total_tokens
            
            # Fallback: use compression ratio as confidence indicator
            if "compression_ratio" in result:
                # Lower compression ratio typically means better transcription
                compression_ratio = result["compression_ratio"]
                return max(0.0, min(1.0, 3.0 - compression_ratio / 2.0))
            
            return 0.5  # Default confidence
            
        except:
            return 0.0
    
    def transcribe_file(self, file_path: str, **kwargs) -> Dict:
        """Transcribe audio file"""
        try:
            from .audio_processor import AudioProcessor
            
            # Load audio file
            audio_processor = AudioProcessor(self.config)
            audio_data = audio_processor.load_audio_file(file_path)
            
            if audio_data is None:
                return {"error": f"Could not load audio file: {file_path}"}
            
            # Transcribe
            result = self.transcribe_audio(
                audio_data, 
                sample_rate=self.config.audio.sample_rate,
                **kwargs
            )
            
            result["source_file"] = file_path
            return result
            
        except Exception as e:
            return {"error": f"File transcription failed: {str(e)}"}
    
    def start_real_time_transcription(self, callback: Callable[[Dict], None]) -> None:
        """Start real-time transcription mode"""
        self.transcription_callback = callback
        self.is_processing = True
        
        if self.processing_thread is None or not self.processing_thread.is_alive():
            self.processing_thread = threading.Thread(target=self._process_transcription_queue)
            self.processing_thread.daemon = True
            self.processing_thread.start()
    
    def stop_real_time_transcription(self) -> None:
        """Stop real-time transcription mode"""
        self.is_processing = False
        self.transcription_callback = None
        
        if self.processing_thread and self.processing_thread.is_alive():
            self.processing_thread.join(timeout=2.0)
    
    def queue_audio_for_transcription(self, audio_data: np.ndarray, sample_rate: int = 16000) -> None:
        """Add audio to transcription queue"""
        if self.is_processing:
            self.processing_queue.append((audio_data, sample_rate, time.time()))
    
    def _process_transcription_queue(self) -> None:
        """Process transcription queue in background thread"""
        while self.is_processing:
            if self.processing_queue:
                try:
                    audio_data, sample_rate, timestamp = self.processing_queue.pop(0)
                    
                    # Skip if audio is too old (older than 5 seconds)
                    if time.time() - timestamp > 5.0:
                        continue
                    
                    # Transcribe audio
                    result = self.transcribe_audio(audio_data, sample_rate)
                    
                    # Call callback if available
                    if self.transcription_callback and result.get("text"):
                        self.transcription_callback(result)
                        
                except Exception as e:
                    print(f"Error in transcription queue processing: {e}")
            else:
                time.sleep(0.1)
    
    def get_available_models(self) -> List[str]:
        """Get list of available Whisper models"""
        return self.config.get_available_models()
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        return self.config.get_supported_languages()
    
    def detect_language(self, audio_data: np.ndarray, sample_rate: int = 16000) -> Tuple[str, float]:
        """Detect language from audio"""
        if self.model is None:
            return "unknown", 0.0
        
        try:
            # Prepare audio (first 30 seconds max for language detection)
            max_samples = 30 * sample_rate
            if len(audio_data) > max_samples:
                audio_data = audio_data[:max_samples]
            
            # Ensure correct format
            if sample_rate != 16000:
                import librosa
                audio_data = librosa.resample(audio_data, orig_sr=sample_rate, target_sr=16000)
            
            if audio_data.dtype != np.float32:
                audio_data = audio_data.astype(np.float32)
            
            # Detect language
            mel = whisper.log_mel_spectrogram(audio_data).to(self.model.device)
            _, probs = self.model.detect_language(mel)
            
            # Get most likely language
            most_likely_language = max(probs, key=probs.get)
            confidence = probs[most_likely_language]
            
            return most_likely_language, confidence
            
        except Exception as e:
            print(f"Language detection error: {e}")
            return "unknown", 0.0
    
    def get_statistics(self) -> Dict:
        """Get transcription statistics"""
        stats = self.stats.copy()
        
        if stats['total_audio_duration'] > 0:
            stats['real_time_factor'] = stats['total_processing_time'] / stats['total_audio_duration']
        else:
            stats['real_time_factor'] = 0.0
        
        return stats
    
    def clear_statistics(self) -> None:
        """Clear transcription statistics"""
        self.stats = {
            'total_transcriptions': 0,
            'total_processing_time': 0,
            'average_processing_time': 0,
            'total_audio_duration': 0
        }
    
    def benchmark_model(self, test_duration: float = 10.0) -> Dict:
        """Benchmark current model performance"""
        try:
            from .audio_processor import AudioProcessor
            
            print(f"Benchmarking model '{self.model_size}' for {test_duration} seconds...")
            
            # Generate test audio (sine wave)
            sample_rate = 16000
            t = np.linspace(0, test_duration, int(sample_rate * test_duration), False)
            test_audio = np.sin(2 * np.pi * 440 * t).astype(np.float32)  # 440 Hz sine wave
            
            # Perform transcription
            start_time = time.time()
            result = self.transcribe_audio(test_audio, sample_rate)
            end_time = time.time()
            
            benchmark_result = {
                'model_size': self.model_size,
                'device': self.device,
                'test_duration': test_duration,
                'processing_time': end_time - start_time,
                'real_time_factor': (end_time - start_time) / test_duration,
                'success': 'error' not in result,
                'model_info': self.get_model_info()
            }
            
            print(f"Benchmark completed: {benchmark_result['real_time_factor']:.2f}x real-time")
            return benchmark_result
            
        except Exception as e:
            return {
                'error': f"Benchmark failed: {str(e)}",
                'model_size': self.model_size
            } 