import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk
from typing import Optional, Dict, Any
import threading
import time
from pathlib import Path
import math

from .core.config import Config
from .core.transcriber import WhisperTranscriber
from .core.audio_processor import AudioProcessor
from .utils.output_handler import OutputHandler
from .utils.hotkey_manager import HotkeyManager


# Ultra-modern theme for YouTube
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class YouTubeReadyGUI:
    """🎬 Ultra-Modern GUI Perfect for YouTube Content! ✨"""
    
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
        self.recording_animation = 0
        
        # Create stunning main window
        self.root = ctk.CTk()
        self.root.title("🎤 WisprClone Pro - YouTube Edition")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Professional styling
        self.root.configure(fg_color="#0a0a0a")
        
        # Setup the YouTube-ready interface
        self.setup_youtube_interface()
        
        # Initialize in background
        threading.Thread(target=self.initialize_components, daemon=True).start()
        
        # Start visual effects
        self.start_animations()
    
    def setup_youtube_interface(self):
        """Setup YouTube-ready interface with professional styling"""
        # Main container with modern layout
        self.main_container = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header section with branding
        self.create_professional_header()
        
        # Main content area
        self.create_content_area()
        
        # Status and info bar
        self.create_status_bar()
    
    def create_professional_header(self):
        """Create professional header perfect for YouTube"""
        header = ctk.CTkFrame(
            self.main_container,
            height=100,
            fg_color="#1a1a1a",
            corner_radius=15
        )
        header.pack(fill="x", pady=(0, 20))
        header.pack_propagate(False)
        
        # Left side - Logo and title
        left_frame = ctk.CTkFrame(header, fg_color="transparent")
        left_frame.pack(side="left", fill="y", padx=30, pady=20)
        
        title_label = ctk.CTkLabel(
            left_frame,
            text="🎤 WisprClone Pro",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#00D4FF"
        )
        title_label.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            left_frame,
            text="Professional AI Speech Recognition • YouTube Edition",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        subtitle.pack(anchor="w", pady=(2, 0))
        
        # Right side - Status indicators
        right_frame = ctk.CTkFrame(header, fg_color="transparent")
        right_frame.pack(side="right", fill="y", padx=30, pady=20)
        
        self.ai_status = ctk.CTkLabel(
            right_frame,
            text="🤖 AI: Loading...",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#FF6B35"
        )
        self.ai_status.pack(anchor="e")
        
        self.device_status = ctk.CTkLabel(
            right_frame,
            text="🎙️ Microphone: Ready",
            font=ctk.CTkFont(size=11),
            text_color="#00FF88"
        )
        self.device_status.pack(anchor="e", pady=(5, 0))
    
    def create_content_area(self):
        """Create main content area with modern design"""
        content_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="transparent"
        )
        content_frame.pack(fill="both", expand=True)
        
        # Left panel - Controls
        self.create_control_panel(content_frame)
        
        # Right panel - Output
        self.create_output_panel(content_frame)
    
    def create_control_panel(self, parent):
        """Create sleek control panel"""
        control_panel = ctk.CTkFrame(
            parent,
            width=400,
            fg_color="#1a1a1a",
            corner_radius=15
        )
        control_panel.pack(side="left", fill="y", padx=(0, 15))
        control_panel.pack_propagate(False)
        
        # Recording section
        self.create_recording_controls(control_panel)
        
        # AI Settings
        self.create_ai_settings(control_panel)
        
        # Quick actions
        self.create_quick_actions_panel(control_panel)
    
    def create_recording_controls(self, parent):
        """Create modern recording controls"""
        record_section = ctk.CTkFrame(parent, fg_color="transparent")
        record_section.pack(fill="x", padx=20, pady=20)
        
        # Section header
        header_label = ctk.CTkLabel(
            record_section,
            text="🎙️ Recording Studio",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FFFFFF"
        )
        header_label.pack(anchor="w", pady=(0, 15))
        
        # Main record button with glow effect
        self.main_record_btn = ctk.CTkButton(
            record_section,
            text="🎤 Start Recording",
            command=self.toggle_recording,
            height=55,
            width=300,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#FF3366",
            hover_color="#FF1155",
            corner_radius=12,
            border_width=2,
            border_color="#FF6699"
        )
        self.main_record_btn.pack(pady=(0, 15))
        
        # Recording indicator with animation
        self.record_indicator = ctk.CTkFrame(
            record_section,
            height=50,
            fg_color="#2a2a2a",
            corner_radius=10
        )
        self.record_indicator.pack(fill="x", pady=(0, 15))
        
        self.record_status = ctk.CTkLabel(
            self.record_indicator,
            text="🔴 Ready to Record",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#CCCCCC"
        )
        self.record_status.pack(pady=15)
        
        # Quick record button
        quick_btn = ctk.CTkButton(
            record_section,
            text="⚡ Quick Record (5s)",
            command=self.quick_record,
            height=40,
            font=ctk.CTkFont(size=13),
            fg_color="#8B5CF6",
            hover_color="#7C3AED",
            corner_radius=8
        )
        quick_btn.pack(fill="x")
    
    def create_ai_settings(self, parent):
        """Create AI model settings"""
        ai_section = ctk.CTkFrame(parent, fg_color="transparent")
        ai_section.pack(fill="x", padx=20, pady=(10, 20))
        
        ctk.CTkLabel(
            ai_section,
            text="🤖 AI Configuration",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFFFFF"
        ).pack(anchor="w", pady=(0, 10))
        
        # Model selector
        model_frame = ctk.CTkFrame(ai_section, fg_color="#2a2a2a", corner_radius=8)
        model_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            model_frame,
            text="Model Size:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#AAAAAA"
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        self.model_selector = ctk.CTkOptionMenu(
            model_frame,
            values=["tiny", "base", "small", "medium", "large"],
            command=self.change_model,
            height=35,
            font=ctk.CTkFont(size=12),
            fg_color="#3a3a3a",
            button_color="#4a4a4a",
            corner_radius=6
        )
        self.model_selector.pack(fill="x", padx=15, pady=(0, 15))
        self.model_selector.set(self.config.whisper.model_size)
        
        # Language selector
        lang_frame = ctk.CTkFrame(ai_section, fg_color="#2a2a2a", corner_radius=8)
        lang_frame.pack(fill="x")
        
        ctk.CTkLabel(
            lang_frame,
            text="Language:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#AAAAAA"
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        self.lang_selector = ctk.CTkOptionMenu(
            lang_frame,
            values=["Auto-detect", "English", "Spanish", "French", "German", "Chinese"],
            height=35,
            font=ctk.CTkFont(size=12),
            fg_color="#3a3a3a",
            button_color="#4a4a4a",
            corner_radius=6
        )
        self.lang_selector.pack(fill="x", padx=15, pady=(0, 15))
        self.lang_selector.set("Auto-detect")
    
    def create_quick_actions_panel(self, parent):
        """Create quick actions panel"""
        actions_section = ctk.CTkFrame(parent, fg_color="transparent")
        actions_section.pack(fill="x", padx=20, pady=(10, 20))
        
        ctk.CTkLabel(
            actions_section,
            text="⚡ Quick Actions",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFFFFF"
        ).pack(anchor="w", pady=(0, 10))
        
        # Action buttons grid
        buttons_frame = ctk.CTkFrame(actions_section, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        # Row 1
        row1 = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 8))
        
        self.clipboard_btn = ctk.CTkButton(
            row1,
            text="📋 Clipboard",
            command=self.toggle_clipboard,
            height=35,
            width=120,
            font=ctk.CTkFont(size=11),
            fg_color="#17A2B8",
            corner_radius=6
        )
        self.clipboard_btn.pack(side="left", padx=(0, 8))
        
        self.typing_btn = ctk.CTkButton(
            row1,
            text="⌨️ Auto-type",
            command=self.toggle_typing,
            height=35,
            width=120,
            font=ctk.CTkFont(size=11),
            fg_color="#28A745",
            corner_radius=6
        )
        self.typing_btn.pack(side="left")
        
        # Row 2
        row2 = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        row2.pack(fill="x", pady=(0, 8))
        
        file_btn = ctk.CTkButton(
            row2,
            text="📁 Open File",
            command=self.open_file,
            height=35,
            width=120,
            font=ctk.CTkFont(size=11),
            fg_color="#FD7E14",
            corner_radius=6
        )
        file_btn.pack(side="left", padx=(0, 8))
        
        export_btn = ctk.CTkButton(
            row2,
            text="💾 Export",
            command=self.export_session,
            height=35,
            width=120,
            font=ctk.CTkFont(size=11),
            fg_color="#6C757D",
            corner_radius=6
        )
        export_btn.pack(side="left")
        
        # Clear button
        clear_btn = ctk.CTkButton(
            buttons_frame,
            text="🗑️ Clear Output",
            command=self.clear_output,
            height=35,
            font=ctk.CTkFont(size=11),
            fg_color="#DC3545",
            corner_radius=6
        )
        clear_btn.pack(fill="x", pady=(0, 8))
    
    def create_output_panel(self, parent):
        """Create modern output panel"""
        output_panel = ctk.CTkFrame(
            parent,
            fg_color="#1a1a1a",
            corner_radius=15
        )
        output_panel.pack(side="right", fill="both", expand=True)
        
        # Output header
        output_header = ctk.CTkFrame(
            output_panel,
            height=60,
            fg_color="#2a2a2a",
            corner_radius=10
        )
        output_header.pack(fill="x", padx=15, pady=(15, 10))
        output_header.pack_propagate(False)
        
        # Header content
        header_left = ctk.CTkFrame(output_header, fg_color="transparent")
        header_left.pack(side="left", fill="y", padx=20)
        
        ctk.CTkLabel(
            header_left,
            text="📝 Live Transcription",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FFFFFF"
        ).pack(anchor="w", pady=15)
        
        header_right = ctk.CTkFrame(output_header, fg_color="transparent")
        header_right.pack(side="right", fill="y", padx=20)
        
        self.stats_display = ctk.CTkLabel(
            header_right,
            text="Ready for transcription",
            font=ctk.CTkFont(size=11),
            text_color="#AAAAAA"
        )
        self.stats_display.pack(anchor="e", pady=15)
        
        # Main output area
        self.output_display = ctk.CTkTextbox(
            output_panel,
            font=ctk.CTkFont(family="JetBrains Mono", size=14),
            fg_color="#0a0a0a",
            text_color="#E6E6E6",
            corner_radius=10,
            border_width=1,
            border_color="#333333",
            wrap="word"
        )
        self.output_display.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Welcome message
        welcome_message = """🎉 Welcome to WisprClone Pro - YouTube Edition!

Your professional AI-powered speech recognition system is ready for content creation.

✨ YouTube-Ready Features:
• Ultra-modern, sleek interface
• Real-time speech transcription
• Multiple language support
• Professional output formatting
• High-accuracy AI models
• Perfect for video content

🎬 Perfect for:
• Video tutorials
• Live streaming
• Podcast transcription
• Content creation
• Professional presentations

🎙️ Click "Start Recording" to begin your professional transcription experience!

Ready to create amazing content? Let's go! 🚀
"""
        self.output_display.insert("0.0", welcome_message)
    
    def create_status_bar(self):
        """Create professional status bar"""
        status_bar = ctk.CTkFrame(
            self.main_container,
            height=45,
            fg_color="#1a1a1a",
            corner_radius=10
        )
        status_bar.pack(fill="x", pady=(15, 0))
        status_bar.pack_propagate(False)
        
        # Status content
        status_left = ctk.CTkFrame(status_bar, fg_color="transparent")
        status_left.pack(side="left", fill="y", padx=20)
        
        self.main_status = ctk.CTkLabel(
            status_left,
            text="🟢 System Ready",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#00FF88"
        )
        self.main_status.pack(anchor="w", pady=12)
        
        status_right = ctk.CTkFrame(status_bar, fg_color="transparent")
        status_right.pack(side="right", fill="y", padx=20)
        
        version_info = ctk.CTkLabel(
            status_right,
            text="WisprClone Pro v1.0 • YouTube Edition • Powered by OpenAI Whisper",
            font=ctk.CTkFont(size=10),
            text_color="#666666"
        )
        version_info.pack(anchor="e", pady=12)
    
    def start_animations(self):
        """Start visual animations"""
        self.animate_interface()
    
    def animate_interface(self):
        """Animate interface elements"""
        try:
            if self.is_recording:
                # Pulsing animation for recording
                self.recording_animation += 0.15
                pulse = (math.sin(self.recording_animation) + 1) / 2
                
                # Animate recording status
                if pulse > 0.5:
                    self.record_status.configure(
                        text="🔴 RECORDING...",
                        text_color="#FF3366"
                    )
                else:
                    self.record_status.configure(
                        text="⚪ RECORDING...",
                        text_color="#FF6699"
                    )
            
            # Schedule next frame
            self.root.after(150, self.animate_interface)
            
        except Exception:
            # Graceful failure for animations
            self.root.after(1000, self.animate_interface)
    
    # Core functionality methods
    def initialize_components(self):
        """Initialize all components"""
        try:
            self.update_status("🔄 Initializing AI...", "#FF6B35")
            
            # Load AI model
            self.transcriber = WhisperTranscriber(self.config)
            self.transcriber.load_model(self.config.whisper.model_size)
            
            # Setup audio
            self.audio_processor = AudioProcessor(self.config)
            
            # Setup output
            self.output_handler = OutputHandler(self.config)
            
            # Setup hotkeys
            try:
                self.hotkey_manager = HotkeyManager(self.config)
                self.hotkey_manager.register_hotkey("toggle_recording", self.toggle_recording)
                self.hotkey_manager.register_hotkey("stop_recording", self.stop_recording)
                self.hotkey_manager.register_hotkey("toggle_typing", self.toggle_typing)
                self.hotkey_manager.register_hotkey("clear_output", self.clear_output)
            except Exception as e:
                print(f"Hotkey setup failed: {e}")
            
            self.is_initialized = True
            self.root.after(0, self.finalize_initialization)
            
        except Exception as e:
            self.root.after(0, lambda: self.update_status(f"❌ Init failed: {str(e)}", "#FF3366"))
    
    def finalize_initialization(self):
        """Finalize initialization with UI updates"""
        model_info = self.transcriber.get_model_info()
        model_name = model_info.get('model_size', 'unknown').title()
        
        self.ai_status.configure(
            text=f"🤖 AI: {model_name} Ready",
            text_color="#00FF88"
        )
        
        self.update_status("🟢 All Systems Ready - Perfect for YouTube!", "#00FF88")
        self.update_button_states()
    
    def update_status(self, message: str, color: str = "#FFFFFF"):
        """Update main status"""
        if hasattr(self, 'main_status'):
            self.main_status.configure(text=message, text_color=color)
    
    def update_button_states(self):
        """Update button appearances"""
        if self.config.output.output_to_clipboard:
            self.clipboard_btn.configure(fg_color="#00FF88")
        
        if self.config.output.typing_enabled:
            self.typing_btn.configure(fg_color="#00FF88")
    
    def toggle_recording(self):
        """Toggle recording with professional feedback"""
        if not self.is_initialized:
            messagebox.showwarning("Not Ready", "System still initializing...")
            return
        
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()
    
    def start_recording(self):
        """Start recording with visual effects"""
        self.is_recording = True
        
        # Update button
        self.main_record_btn.configure(
            text="⏹️ Stop Recording",
            fg_color="#FF0033",
            hover_color="#DD0022",
            border_color="#FF3366"
        )
        
        # Setup callbacks
        def transcription_callback(result):
            self.root.after(0, lambda: self.handle_transcription_result(result))
        
        def audio_callback(audio_data, sample_rate):
            if self.transcriber:
                self.transcriber.queue_audio_for_transcription(audio_data, sample_rate)
        
        # Start systems
        self.transcriber.start_real_time_transcription(transcription_callback)
        self.audio_processor.start_recording(audio_callback)
        
        self.update_status("🎙️ Recording in Progress - Creating Content!", "#FF3366")
    
    def stop_recording(self):
        """Stop recording"""
        self.is_recording = False
        
        # Reset button
        self.main_record_btn.configure(
            text="🎤 Start Recording",
            fg_color="#FF3366",
            hover_color="#FF1155",
            border_color="#FF6699"
        )
        
        # Reset status
        self.record_status.configure(
            text="🔴 Ready to Record",
            text_color="#CCCCCC"
        )
        
        # Stop systems
        if self.audio_processor:
            self.audio_processor.stop_recording()
        if self.transcriber:
            self.transcriber.stop_real_time_transcription()
        
        self.update_status("✅ Recording Complete - Ready for Next Take!", "#00FF88")
    
    def handle_transcription_result(self, result: Dict[str, Any]):
        """Handle transcription with YouTube-ready formatting"""
        if "error" in result:
            # Skip filtered results
            if any(keyword in result["error"].lower() for keyword in ["rejected", "too short", "repetitive"]):
                return
            return
        
        text = result.get("text", "").strip()
        if not text:
            return
        
        # YouTube-ready formatting
        timestamp = time.strftime('%H:%M:%S')
        language = result.get("language", "unknown").upper()
        confidence = result.get("confidence", 0.0)
        processing_time = result.get("processing_time", 0.0)
        
        # Professional output format
        formatted_output = f"""
┌─ 🎬 [{timestamp}] {language} ─ ✨ {confidence:.0%} Confidence ─ ⚡ {processing_time:.2f}s ─┐
│                                                                                    │
│  "{text}"
│                                                                                    │
└────────────────────────────────────────────────────────────────────────────────┘

"""
        
        self.output_display.insert("end", formatted_output)
        self.output_display.see("end")
        
        # Update stats
        if self.transcriber:
            stats = self.transcriber.get_statistics()
            total = stats.get('total_transcriptions', 0)
            avg_time = stats.get('average_processing_time', 0)
            self.stats_display.configure(
                text=f"📊 {total} transcriptions │ ⚡ {avg_time:.2f}s average"
            )
        
        # Handle output
        if self.output_handler:
            self.output_handler.handle_transcription(result)
    
    def toggle_clipboard(self):
        """Toggle clipboard output"""
        self.config.output.output_to_clipboard = not self.config.output.output_to_clipboard
        self.config.save()
        
        status = "ON" if self.config.output.output_to_clipboard else "OFF"
        color = "#00FF88" if self.config.output.output_to_clipboard else "#17A2B8"
        
        self.clipboard_btn.configure(fg_color=color)
        self.update_status(f"📋 Clipboard: {status}", color)
    
    def toggle_typing(self):
        """Toggle auto-typing"""
        self.config.output.typing_enabled = not self.config.output.typing_enabled
        self.config.save()
        
        if self.output_handler:
            self.output_handler.update_typing_config()
        
        status = "ON" if self.config.output.typing_enabled else "OFF"
        color = "#00FF88" if self.config.output.typing_enabled else "#28A745"
        
        self.typing_btn.configure(fg_color=color)
        self.update_status(f"⌨️ Auto-typing: {status}", color)
    
    def clear_output(self):
        """Clear output display"""
        self.output_display.delete("0.0", "end")
        if self.output_handler:
            self.output_handler.clear_session_log()
        self.update_status("🗑️ Output Cleared - Ready for Fresh Content!", "#6C757D")
    
    def change_model(self, new_model):
        """Change AI model"""
        self.config.whisper.model_size = new_model
        self.config.save()
        
        self.update_status(f"🔄 Loading {new_model.title()} model...", "#FF6B35")
        
        def reload_model():
            try:
                self.transcriber.load_model(new_model)
                self.root.after(0, lambda: self.update_status(f"✅ {new_model.title()} model ready!", "#00FF88"))
                self.root.after(0, lambda: self.ai_status.configure(
                    text=f"🤖 AI: {new_model.title()} Ready",
                    text_color="#00FF88"
                ))
            except Exception as e:
                self.root.after(0, lambda: self.update_status("❌ Model loading failed", "#FF3366"))
        
        threading.Thread(target=reload_model, daemon=True).start()
    
    def quick_record(self):
        """Quick 5-second recording"""
        if not self.is_initialized:
            messagebox.showwarning("Not Ready", "System still initializing...")
            return
        
        self.update_status("⚡ Quick Recording - Get Ready!", "#8B5CF6")
        
        def record_thread():
            try:
                audio_data = self.audio_processor.record_audio_chunk(5.0)
                if audio_data is None:
                    self.root.after(0, lambda: messagebox.showerror("Error", "Recording failed"))
                    return
                
                result = self.transcriber.transcribe_audio(audio_data, self.config.audio.sample_rate)
                self.root.after(0, lambda: self.handle_transcription_result(result))
                self.root.after(0, lambda: self.update_status("✅ Quick recording complete!", "#00FF88"))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Recording failed: {str(e)}"))
        
        threading.Thread(target=record_thread, daemon=True).start()
    
    def open_file(self):
        """Open and process audio file"""
        if not self.is_initialized:
            messagebox.showwarning("Not Ready", "System still initializing...")
            return
        
        file_path = filedialog.askopenfilename(
            title="Select Audio File for Transcription",
            filetypes=[
                ("Audio Files", "*.wav *.mp3 *.m4a *.ogg *.flac *.aac"),
                ("All Files", "*.*")
            ]
        )
        
        if not file_path:
            return
        
        def process_file():
            try:
                filename = Path(file_path).name
                self.root.after(0, lambda: self.update_status(f"🎵 Processing {filename}...", "#FD7E14"))
                
                result = self.transcriber.transcribe_file(file_path)
                self.root.after(0, lambda: self.handle_transcription_result(result))
                self.root.after(0, lambda: self.update_status("✅ File processing complete!", "#00FF88"))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"File processing failed: {str(e)}"))
                self.root.after(0, lambda: self.update_status("❌ File processing failed", "#FF3366"))
        
        threading.Thread(target=process_file, daemon=True).start()
    
    def export_session(self):
        """Export transcription session"""
        if not self.output_handler or not self.output_handler.session_log:
            messagebox.showinfo("No Data", "No transcription data to export")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Export Transcription Session",
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt"),
                ("JSON Files", "*.json"),
                ("CSV Files", "*.csv"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            try:
                ext = Path(file_path).suffix.lower()
                format_type = {"json": "json", ".csv": "csv"}.get(ext, "txt")
                
                if self.output_handler.export_session_log(file_path, format_type):
                    messagebox.showinfo("Success", f"Session exported successfully!\n\nFile: {file_path}")
                    self.update_status("💾 Session exported successfully!", "#00FF88")
                else:
                    messagebox.showerror("Error", "Export failed")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def on_closing(self):
        """Handle application closing"""
        try:
            if self.is_recording:
                self.stop_recording()
            
            if self.hotkey_manager:
                self.hotkey_manager.cleanup()
            
            if self.output_handler:
                self.output_handler.close()
            
            self.root.destroy()
            
        except Exception as e:
            print(f"Cleanup error: {e}")
            self.root.destroy()
    
    def run(self):
        """Run the YouTube-ready GUI"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()


def main():
    """Launch YouTube-ready WisprClone"""
    try:
        app = YouTubeReadyGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Launch Error", f"Failed to start WisprClone: {str(e)}")


if __name__ == "__main__":
    main() 