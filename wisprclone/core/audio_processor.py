import numpy as np
import sounddevice as sd
import soundfile as sf
import threading
import queue
import time
from typing import Optional, Callable, Generator
import noisereduce as nr
from scipy import signal
import librosa
from .config import Config


class AudioProcessor:
    """Audio processing and recording manager for WisprClone"""
    
    def __init__(self, config: Config):
        self.config = config
        self.is_recording = False
        self.audio_queue = queue.Queue()
        self.recording_thread = None
        self.callback_function = None
        
        # Audio buffers
        self.current_buffer = np.array([])
        self.silence_buffer = []
        self.last_audio_time = 0
        
        # Recording parameters
        self.sample_rate = config.audio.sample_rate
        self.channels = config.audio.channels
        self.chunk_size = config.audio.chunk_size
        self.device_index = config.audio.device_index
        
        # Silence detection
        self.silence_threshold = config.audio.silence_threshold
        self.silence_duration = config.audio.silence_duration
        
        # Initialize audio device
        self._initialize_audio_device()
    
    def _initialize_audio_device(self) -> None:
        """Initialize and test audio device"""
        try:
            # Test if device is available
            if self.device_index is not None:
                device_info = sd.query_devices(self.device_index)
                print(f"Using audio device: {device_info['name']}")
            else:
                device_info = sd.query_devices(kind='input')
                print(f"Using default input device: {device_info['name']}")
                
        except Exception as e:
            print(f"Audio device initialization error: {e}")
            print("Using system default audio device")
            self.device_index = None
    
    def get_available_devices(self) -> list:
        """Get list of available audio input devices"""
        devices = []
        try:
            device_list = sd.query_devices()
            for i, device in enumerate(device_list):
                if device['max_input_channels'] > 0:
                    devices.append({
                        'index': i,
                        'name': device['name'],
                        'channels': device['max_input_channels'],
                        'sample_rate': device['default_samplerate']
                    })
        except Exception as e:
            print(f"Error getting audio devices: {e}")
        
        return devices
    
    def preprocess_audio(self, audio_data: np.ndarray) -> np.ndarray:
        """Apply audio preprocessing including noise reduction"""
        try:
            # Ensure audio is float32
            if audio_data.dtype != np.float32:
                audio_data = audio_data.astype(np.float32)
            
            # Normalize audio
            if np.max(np.abs(audio_data)) > 0:
                audio_data = audio_data / np.max(np.abs(audio_data))
            
            # Apply noise reduction if enabled
            if self.config.audio.noise_reduction and len(audio_data) > self.sample_rate:
                try:
                    # Estimate noise from first 0.5 seconds
                    noise_sample_length = min(len(audio_data), int(0.5 * self.sample_rate))
                    audio_data = nr.reduce_noise(
                        y=audio_data,
                        sr=self.sample_rate,
                        stationary=False,
                        prop_decrease=0.8
                    )
                except Exception as e:
                    print(f"Noise reduction failed: {e}")
            
            # Apply high-pass filter to remove low-frequency noise
            nyquist = self.sample_rate // 2
            low_cutoff = 80  # Hz
            high_cutoff = min(8000, nyquist - 1)  # Hz
            
            # Design bandpass filter
            sos = signal.butter(4, [low_cutoff, high_cutoff], 
                              btype='band', fs=self.sample_rate, output='sos')
            audio_data = signal.sosfilt(sos, audio_data)
            
            # Apply gentle compression
            threshold = 0.3
            ratio = 3.0
            mask = np.abs(audio_data) > threshold
            audio_data[mask] = np.sign(audio_data[mask]) * (
                threshold + (np.abs(audio_data[mask]) - threshold) / ratio
            )
            
            return audio_data
            
        except Exception as e:
            print(f"Audio preprocessing error: {e}")
            return audio_data
    
    def detect_silence(self, audio_chunk: np.ndarray) -> bool:
        """Detect if audio chunk contains silence"""
        # Calculate RMS energy
        rms = np.sqrt(np.mean(audio_chunk ** 2))
        return rms < self.silence_threshold
    
    def audio_callback(self, indata, frames, time, status):
        """Callback function for audio stream"""
        if status:
            print(f"Audio callback status: {status}")
        
        # Convert to mono if stereo
        if len(indata.shape) > 1:
            audio_chunk = np.mean(indata, axis=1)
        else:
            audio_chunk = indata.flatten()
        
        # Add to queue for processing
        self.audio_queue.put(audio_chunk.copy())
    
    def start_recording(self, callback: Optional[Callable] = None) -> None:
        """Start audio recording"""
        if self.is_recording:
            print("Already recording")
            return
        
        self.callback_function = callback
        self.is_recording = True
        self.current_buffer = np.array([])
        self.last_audio_time = time.time()
        
        try:
            # Start audio stream
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                callback=self.audio_callback,
                blocksize=self.chunk_size,
                device=self.device_index,
                dtype=np.float32
            )
            self.stream.start()
            
            # Start processing thread
            self.recording_thread = threading.Thread(target=self._process_audio_stream)
            self.recording_thread.daemon = True
            self.recording_thread.start()
            
            print("Recording started")
            
        except Exception as e:
            print(f"Error starting recording: {e}")
            self.is_recording = False
    
    def stop_recording(self) -> Optional[np.ndarray]:
        """Stop audio recording and return final buffer"""
        if not self.is_recording:
            return None
        
        self.is_recording = False
        
        try:
            if hasattr(self, 'stream'):
                self.stream.stop()
                self.stream.close()
            
            # Wait for processing thread to finish
            if self.recording_thread and self.recording_thread.is_alive():
                self.recording_thread.join(timeout=2.0)
            
            print("Recording stopped")
            
            # Return final processed buffer
            if len(self.current_buffer) > 0:
                return self.preprocess_audio(self.current_buffer)
            
        except Exception as e:
            print(f"Error stopping recording: {e}")
        
        return None
    
    def _process_audio_stream(self) -> None:
        """Process audio stream in separate thread"""
        silence_start_time = None
        
        while self.is_recording:
            try:
                # Get audio chunk from queue
                audio_chunk = self.audio_queue.get(timeout=0.1)
                
                # Add to current buffer
                self.current_buffer = np.concatenate([self.current_buffer, audio_chunk])
                
                # Check for silence
                is_silent = self.detect_silence(audio_chunk)
                current_time = time.time()
                
                if is_silent:
                    if silence_start_time is None:
                        silence_start_time = current_time
                    elif current_time - silence_start_time > self.silence_duration:
                        # Long silence detected, process current buffer
                        if len(self.current_buffer) > self.sample_rate * 0.5:  # At least 0.5 seconds
                            self._process_complete_utterance()
                        silence_start_time = None
                else:
                    silence_start_time = None
                    self.last_audio_time = current_time
                
                # Process if buffer gets too long (prevent memory issues)
                if len(self.current_buffer) > self.sample_rate * 30:  # 30 seconds max
                    self._process_complete_utterance()
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error in audio processing: {e}")
    
    def _process_complete_utterance(self) -> None:
        """Process a complete utterance"""
        if len(self.current_buffer) == 0:
            return
        
        try:
            # Preprocess the audio
            processed_audio = self.preprocess_audio(self.current_buffer)
            
            # Call the callback function if provided
            if self.callback_function:
                self.callback_function(processed_audio, self.sample_rate)
            
            # Clear the buffer
            self.current_buffer = np.array([])
            
        except Exception as e:
            print(f"Error processing utterance: {e}")
    
    def record_audio_chunk(self, duration: float = 5.0) -> Optional[np.ndarray]:
        """Record a single audio chunk of specified duration"""
        try:
            print(f"Recording for {duration} seconds...")
            audio_data = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=self.channels,
                device=self.device_index,
                dtype=np.float32
            )
            sd.wait()  # Wait until recording is finished
            
            # Convert to mono if stereo
            if len(audio_data.shape) > 1:
                audio_data = np.mean(audio_data, axis=1)
            else:
                audio_data = audio_data.flatten()
            
            return self.preprocess_audio(audio_data)
            
        except Exception as e:
            print(f"Error recording audio chunk: {e}")
            return None
    
    def save_audio(self, audio_data: np.ndarray, filename: str) -> bool:
        """Save audio data to file"""
        try:
            sf.write(filename, audio_data, self.sample_rate)
            print(f"Audio saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving audio: {e}")
            return False
    
    def load_audio_file(self, filename: str) -> Optional[np.ndarray]:
        """Load audio from file"""
        try:
            audio_data, sample_rate = librosa.load(
                filename, 
                sr=self.sample_rate, 
                mono=True
            )
            return self.preprocess_audio(audio_data)
        except Exception as e:
            print(f"Error loading audio file: {e}")
            return None
    
    def get_audio_info(self) -> dict:
        """Get current audio configuration info"""
        return {
            'sample_rate': self.sample_rate,
            'channels': self.channels,
            'chunk_size': self.chunk_size,
            'device_index': self.device_index,
            'is_recording': self.is_recording,
            'buffer_length': len(self.current_buffer) / self.sample_rate if len(self.current_buffer) > 0 else 0
        } 