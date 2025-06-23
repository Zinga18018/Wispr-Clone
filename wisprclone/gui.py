import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk
from typing import Optional, Dict, Any
import threading
import time
from pathlib import Path

from .core.config import Config
from .core.transcriber import WhisperTranscriber
from .core.audio_processor import AudioProcessor
from .utils.output_handler import OutputHandler
from .utils.hotkey_manager import HotkeyManager


# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class WisprCloneGUI:
    """Modern GUI for WisprClone using CustomTkinter"""
    
    def __init__(self):
        # Initialize configuration
        self.config = Config()
        
        # Initialize components
        self.transcriber = None
        self.audio_processor = None
        self.output_handler = None
        self.hotkey_manager = None
        
        # GUI state
        self.is_recording = False
        self.is_initialized = False
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("WisprClone - AI Speech Recognition")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Setup UI
        self.setup_ui()
        
        # Setup components in background
        threading.Thread(target=self.initialize_components, daemon=True).start()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Configure grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)
        
        # Create header
        self.create_header()
        
        # Create control panel
        self.create_control_panel()
        
        # Create output area
        self.create_output_area()
        
        # Create status bar
        self.create_status_bar()
        
        # Create settings panel
        self.create_settings_panel()
    
    def create_header(self):
        """Create the header section"""
        header_frame = ctk.CTkFrame(self.main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(10, 5))
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="🎤 WisprClone",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side="left", padx=20, pady=10)
        
        # Model info
        self.model_info_label = ctk.CTkLabel(
            header_frame,
            text="Initializing...",
            font=ctk.CTkFont(size=12)
        )
        self.model_info_label.pack(side="right", padx=20, pady=10)
    
    def create_control_panel(self):
        """Create the control panel"""
        control_frame = ctk.CTkFrame(self.main_frame)
        control_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        control_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Recording controls
        record_frame = ctk.CTkFrame(control_frame)
        record_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        ctk.CTkLabel(record_frame, text="Recording", font=ctk.CTkFont(weight="bold")).pack(pady=(10, 5))
        
        self.record_button = ctk.CTkButton(
            record_frame,
            text="🎤 Start Recording",
            command=self.toggle_recording,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.record_button.pack(pady=5, padx=10, fill="x")
        
        self.quick_record_button = ctk.CTkButton(
            record_frame,
            text="⚡ Quick Record (5s)",
            command=self.quick_record,
            height=30
        )
        self.quick_record_button.pack(pady=5, padx=10, fill="x")
        
        # File controls
        file_frame = ctk.CTkFrame(control_frame)
        file_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        ctk.CTkLabel(file_frame, text="Files", font=ctk.CTkFont(weight="bold")).pack(pady=(10, 5))
        
        self.file_button = ctk.CTkButton(
            file_frame,
            text="📁 Open Audio File",
            command=self.open_file,
            height=30
        )
        self.file_button.pack(pady=5, padx=10, fill="x")
        
        self.export_button = ctk.CTkButton(
            file_frame,
            text="💾 Export Session",
            command=self.export_session,
            height=30
        )
        self.export_button.pack(pady=5, padx=10, fill="x")
        
        # Output controls
        output_frame = ctk.CTkFrame(control_frame)
        output_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        
        ctk.CTkLabel(output_frame, text="Output", font=ctk.CTkFont(weight="bold")).pack(pady=(10, 5))
        
        self.clipboard_button = ctk.CTkButton(
            output_frame,
            text="📋 Copy to Clipboard",
            command=self.toggle_clipboard,
            height=30
        )
        self.clipboard_button.pack(pady=5, padx=10, fill="x")
        
        self.typing_button = ctk.CTkButton(
            output_frame,
            text="⌨️ Toggle Typing",
            command=self.toggle_typing,
            height=30
        )
        self.typing_button.pack(pady=5, padx=10, fill="x")
        
        self.clear_button = ctk.CTkButton(
            output_frame,
            text="🗑️ Clear Output",
            command=self.clear_output,
            height=30
        )
        self.clear_button.pack(pady=5, padx=10, fill="x")
    
    def create_output_area(self):
        """Create the output text area"""
        output_frame = ctk.CTkFrame(self.main_frame)
        output_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
        output_frame.grid_columnconfigure(0, weight=1)
        output_frame.grid_rowconfigure(1, weight=1)
        
        # Output header
        output_header = ctk.CTkFrame(output_frame)
        output_header.grid(row=0, column=0, sticky="ew", padx=5, pady=(5, 0))
        
        ctk.CTkLabel(
            output_header,
            text="📝 Transcription Output",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left", padx=10, pady=5)
        
        self.stats_label = ctk.CTkLabel(
            output_header,
            text="Ready",
            font=ctk.CTkFont(size=12)
        )
        self.stats_label.pack(side="right", padx=10, pady=5)
        
        # Text output
        self.output_text = ctk.CTkTextbox(
            output_frame,
            font=ctk.CTkFont(size=12),
            wrap="word"
        )
        self.output_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    
    def create_status_bar(self):
        """Create the status bar"""
        self.status_frame = ctk.CTkFrame(self.main_frame, height=30)
        self.status_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=(5, 10))
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Initializing WisprClone...",
            font=ctk.CTkFont(size=11)
        )
        self.status_label.pack(side="left", padx=10, pady=5)
        
        self.audio_indicator = ctk.CTkLabel(
            self.status_frame,
            text="🔇 Audio: Off",
            font=ctk.CTkFont(size=11)
        )
        self.audio_indicator.pack(side="right", padx=10, pady=5)
    
    def create_settings_panel(self):
        """Create settings panel as a separate window"""
        self.settings_window = None
    
    def initialize_components(self):
        """Initialize WisprClone components in background"""
        try:
            # Update status
            self.root.after(0, lambda: self.update_status("Loading Whisper model..."))
            
            # Initialize transcriber
            self.transcriber = WhisperTranscriber(self.config)
            if not self.transcriber.model:
                raise Exception("Failed to load Whisper model")
            
            self.root.after(0, lambda: self.update_status("Initializing audio system..."))
            
            # Initialize audio processor
            self.audio_processor = AudioProcessor(self.config)
            
            # Initialize output handler
            self.output_handler = OutputHandler(self.config)
            
            # Initialize hotkey manager
            self.hotkey_manager = HotkeyManager(self.config)
            
            # Setup hotkeys
            hotkey_callbacks = {
                "toggle_recording": self.toggle_recording,
                "stop_recording": self.stop_recording,
                "toggle_typing": self.toggle_typing,
                "clear_output": self.clear_output
            }
            self.hotkey_manager.setup_default_hotkeys(hotkey_callbacks)
            
            self.is_initialized = True
            
            # Update UI
            self.root.after(0, self.update_ui_after_init)
            
        except Exception as e:
            error_msg = f"Initialization failed: {str(e)}"
            self.root.after(0, lambda: self.update_status(error_msg))
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
    
    def update_ui_after_init(self):
        """Update UI after successful initialization"""
        # Update model info
        model_info = self.transcriber.get_model_info()
        model_text = f"Model: {model_info.get('model_size', 'Unknown')} | Device: {model_info.get('device', 'Unknown')}"
        self.model_info_label.configure(text=model_text)
        
        # Update status
        self.update_status("Ready - Press 🎤 to start recording")
        
        # Enable buttons
        self.record_button.configure(state="normal")
        self.quick_record_button.configure(state="normal")
        self.file_button.configure(state="normal")
    
    def update_status(self, message: str):
        """Update status bar message"""
        self.status_label.configure(text=message)
    
    def toggle_recording(self):
        """Toggle recording on/off"""
        if not self.is_initialized:
            messagebox.showwarning("Warning", "System is still initializing. Please wait.")
            return
        
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()
    
    def start_recording(self):
        """Start real-time recording"""
        try:
            # Setup callbacks
            def transcription_callback(result):
                self.root.after(0, lambda: self.handle_transcription_result(result))
            
            def audio_callback(audio_data, sample_rate):
                self.transcriber.queue_audio_for_transcription(audio_data, sample_rate)
            
            # Start transcription and recording
            self.transcriber.start_real_time_transcription(transcription_callback)
            self.audio_processor.start_recording(audio_callback)
            
            self.is_recording = True
            
            # Update UI
            self.record_button.configure(text="⏹️ Stop Recording", fg_color="red")
            self.audio_indicator.configure(text="🎤 Audio: Recording")
            self.update_status("Recording... Speak now!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start recording: {str(e)}")
    
    def stop_recording(self):
        """Stop recording"""
        try:
            if self.audio_processor:
                self.audio_processor.stop_recording()
            
            if self.transcriber:
                self.transcriber.stop_real_time_transcription()
            
            self.is_recording = False
            
            # Update UI
            self.record_button.configure(text="🎤 Start Recording", fg_color=None)
            self.audio_indicator.configure(text="🔇 Audio: Off")
            self.update_status("Recording stopped")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop recording: {str(e)}")
    
    def quick_record(self):
        """Quick 5-second recording"""
        if not self.is_initialized:
            messagebox.showwarning("Warning", "System is still initializing. Please wait.")
            return
        
        def record_thread():
            try:
                self.root.after(0, lambda: self.update_status("Quick recording in 3 seconds..."))
                time.sleep(1)
                self.root.after(0, lambda: self.update_status("Quick recording in 2 seconds..."))
                time.sleep(1)
                self.root.after(0, lambda: self.update_status("Quick recording in 1 second..."))
                time.sleep(1)
                self.root.after(0, lambda: self.update_status("Recording for 5 seconds..."))
                
                # Record audio
                audio_data = self.audio_processor.record_audio_chunk(5.0)
                
                if audio_data is None:
                    self.root.after(0, lambda: messagebox.showerror("Error", "Failed to record audio"))
                    return
                
                self.root.after(0, lambda: self.update_status("Processing..."))
                
                # Transcribe
                result = self.transcriber.transcribe_audio(audio_data, self.config.audio.sample_rate)
                
                # Handle result
                self.root.after(0, lambda: self.handle_transcription_result(result))
                self.root.after(0, lambda: self.update_status("Quick recording completed"))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Quick recording failed: {str(e)}"))
                self.root.after(0, lambda: self.update_status("Ready"))
        
        threading.Thread(target=record_thread, daemon=True).start()
    
    def open_file(self):
        """Open and transcribe an audio file"""
        if not self.is_initialized:
            messagebox.showwarning("Warning", "System is still initializing. Please wait.")
            return
        
        file_path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[
                ("Audio Files", "*.wav *.mp3 *.m4a *.ogg *.flac"),
                ("All Files", "*.*")
            ]
        )
        
        if not file_path:
            return
        
        def transcribe_thread():
            try:
                self.root.after(0, lambda: self.update_status(f"Transcribing {Path(file_path).name}..."))
                
                # Transcribe file
                result = self.transcriber.transcribe_file(file_path)
                
                # Handle result
                self.root.after(0, lambda: self.handle_transcription_result(result))
                self.root.after(0, lambda: self.update_status("File transcription completed"))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"File transcription failed: {str(e)}"))
                self.root.after(0, lambda: self.update_status("Ready"))
        
        threading.Thread(target=transcribe_thread, daemon=True).start()
    
    def handle_transcription_result(self, result: Dict[str, Any]):
        """Handle transcription result and update UI"""
        if "error" in result:
            self.append_output(f"❌ Error: {result['error']}\n", "error")
            return
        
        text = result.get("text", "").strip()
        if not text:
            return
        
        # Format output
        timestamp = time.strftime('%H:%M:%S')
        language = result.get("language", "unknown")
        confidence = result.get("confidence", 0.0)
        processing_time = result.get("processing_time", 0.0)
        
        output = f"[{timestamp}] ({language}, {confidence:.2f}, {processing_time:.2f}s)\n{text}\n\n"
        self.append_output(output)
        
        # Update statistics
        if self.transcriber:
            stats = self.transcriber.get_statistics()
            stats_text = f"Transcriptions: {stats.get('total_transcriptions', 0)} | Avg: {stats.get('average_processing_time', 0):.2f}s | RTF: {stats.get('real_time_factor', 0):.2f}x"
            self.stats_label.configure(text=stats_text)
        
        # Handle output
        if self.output_handler:
            self.output_handler.handle_transcription(result)
    
    def append_output(self, text: str, tag: str = "normal"):
        """Append text to output area"""
        self.output_text.insert("end", text)
        self.output_text.see("end")
    
    def toggle_clipboard(self):
        """Toggle clipboard output"""
        self.config.output.output_to_clipboard = not self.config.output.output_to_clipboard
        self.config.save()
        
        status = "enabled" if self.config.output.output_to_clipboard else "disabled"
        self.update_status(f"Clipboard output {status}")
        
        # Update button appearance
        if self.config.output.output_to_clipboard:
            self.clipboard_button.configure(fg_color="green")
        else:
            self.clipboard_button.configure(fg_color=None)
    
    def toggle_typing(self):
        """Toggle typing simulation"""
        self.config.output.typing_enabled = not self.config.output.typing_enabled
        self.config.save()
        
        status = "enabled" if self.config.output.typing_enabled else "disabled"
        self.update_status(f"Typing simulation {status}")
        
        # Update button appearance
        if self.config.output.typing_enabled:
            self.typing_button.configure(fg_color="green")
        else:
            self.typing_button.configure(fg_color=None)
    
    def clear_output(self):
        """Clear output text"""
        self.output_text.delete("1.0", "end")
        if self.output_handler:
            self.output_handler.clear_session_log()
        self.update_status("Output cleared")
    
    def export_session(self):
        """Export session log"""
        if not self.output_handler or not self.output_handler.session_log:
            messagebox.showinfo("Info", "No session data to export")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Export Session Log",
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt"),
                ("JSON Files", "*.json"),
                ("CSV Files", "*.csv"),
                ("All Files", "*.*")
            ]
        )
        
        if not file_path:
            return
        
        try:
            # Determine format from extension
            ext = Path(file_path).suffix.lower()
            if ext == ".json":
                format_type = "json"
            elif ext == ".csv":
                format_type = "csv"
            else:
                format_type = "txt"
            
            success = self.output_handler.export_session_log(file_path, format_type)
            
            if success:
                messagebox.showinfo("Success", f"Session exported to {file_path}")
            else:
                messagebox.showerror("Error", "Failed to export session")
                
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def on_closing(self):
        """Handle window closing"""
        try:
            if self.is_recording:
                self.stop_recording()
            
            if self.hotkey_manager:
                self.hotkey_manager.cleanup()
            
            if self.output_handler:
                self.output_handler.close()
            
            self.root.destroy()
            
        except Exception as e:
            print(f"Error during cleanup: {e}")
            self.root.destroy()
    
    def run(self):
        """Run the GUI application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()


def main():
    """Main GUI entry point"""
    try:
        app = WisprCloneGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"Failed to start WisprClone GUI: {str(e)}")


if __name__ == "__main__":
    main() 