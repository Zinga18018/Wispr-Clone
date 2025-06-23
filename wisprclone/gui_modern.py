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


# Set appearance mode and modern color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ModernWisprCloneGUI:
    """Ultra-modern, sleek GUI for WisprClone - YouTube Ready! 🎥✨"""
    
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
        
        # Create main window with modern styling
        self.root = ctk.CTk()
        self.root.title("🎤 WisprClone Pro - AI Speech Recognition")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Set window icon and styling
        self.root.configure(fg_color=["#f0f0f0", "#0d1117"])
        
        # Setup modern UI
        self.setup_modern_ui()
        
        # Initialize components in background
        threading.Thread(target=self.initialize_components, daemon=True).start()
        
        # Start animation loop
        self.animation_loop()
    
    def setup_modern_ui(self):
        """Setup the ultra-modern user interface"""
        # Configure grid with proper weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Create main container with gradient effect
        self.main_container = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )
        self.main_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)
        
        # Create header section
        self.create_modern_header()
        
        # Create main content area
        self.create_main_content()
        
        # Create status section
        self.create_modern_status()
        
        # Add subtle animations and effects
        self.setup_animations()
    
    def create_modern_header(self):
        """Create stunning header with branding"""
        header_frame = ctk.CTkFrame(
            self.main_container,
            height=120,
            fg_color=["#ffffff", "#1a1d29"],
            corner_radius=20
        )
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Logo and branding
        logo_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        logo_frame.grid(row=0, column=0, sticky="w", padx=30, pady=20)
        
        # Main title with gradient effect
        title_label = ctk.CTkLabel(
            logo_frame,
            text="🎤 WisprClone Pro",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=["#1f6aa5", "#4a9eff"]
        )
        title_label.pack(anchor="w")
        
        subtitle_label = ctk.CTkLabel(
            logo_frame,
            text="Professional AI Speech Recognition",
            font=ctk.CTkFont(size=14),
            text_color=["#666666", "#888888"]
        )
        subtitle_label.pack(anchor="w", pady=(5, 0))
        
        # Status indicators
        status_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        status_frame.grid(row=0, column=1, sticky="e", padx=30, pady=20)
        
        self.model_status = ctk.CTkLabel(
            status_frame,
            text="🔄 Initializing...",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=["#ff6b35", "#ff8c42"]
        )
        self.model_status.pack(anchor="e")
        
        self.connection_status = ctk.CTkLabel(
            status_frame,
            text="⚡ Connected",
            font=ctk.CTkFont(size=11),
            text_color=["#28a745", "#34d058"]
        )
        self.connection_status.pack(anchor="e", pady=(5, 0))
    
    def create_main_content(self):
        """Create the main content area with modern design"""
        content_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="transparent"
        )
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure((0, 1), weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        
        # Control panel on the left
        self.create_control_panel(content_frame)
        
        # Output area on the right
        self.create_output_area(content_frame)
    
    def create_control_panel(self, parent):
        """Create modern control panel with glass morphism effect"""
        control_frame = ctk.CTkFrame(
            parent,
            width=400,
            fg_color=["#ffffff", "#1a1d29"],
            corner_radius=20
        )
        control_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 10))
        control_frame.grid_propagate(False)
        
        # Recording section with visual feedback
        self.create_recording_section(control_frame)
        
        # Quick actions
        self.create_quick_actions(control_frame)
        
        # Settings panel
        self.create_settings_section(control_frame)
    
    def create_recording_section(self, parent):
        """Create recording section with visual feedback"""
        record_frame = ctk.CTkFrame(parent, fg_color="transparent")
        record_frame.pack(fill="x", padx=20, pady=20)
        
        # Section title
        ctk.CTkLabel(
            record_frame,
            text="🎙️ Recording Control",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=["#333333", "#ffffff"]
        ).pack(anchor="w", pady=(0, 15))
        
        # Main record button with pulsing effect
        self.record_button = ctk.CTkButton(
            record_frame,
            text="🎤 Start Recording",
            command=self.toggle_recording,
            height=60,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=["#28a745", "#238636"],
            hover_color=["#218838", "#2ea043"],
            corner_radius=15
        )
        self.record_button.pack(fill="x", pady=(0, 10))
        
        # Recording status indicator
        self.recording_indicator = ctk.CTkFrame(
            record_frame,
            height=40,
            fg_color=["#f8f9fa", "#21262d"],
            corner_radius=10
        )
        self.recording_indicator.pack(fill="x", pady=(0, 15))
        
        self.recording_status_label = ctk.CTkLabel(
            self.recording_indicator,
            text="🔴 Ready to Record",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=["#666666", "#8b949e"]
        )
        self.recording_status_label.pack(pady=10)
        
        # Quick record button
        self.quick_record_button = ctk.CTkButton(
            record_frame,
            text="⚡ Quick Record (5s)",
            command=self.quick_record,
            height=40,
            font=ctk.CTkFont(size=13),
            fg_color=["#6f42c1", "#8b5cf6"],
            hover_color=["#5a32a3", "#7c3aed"],
            corner_radius=10
        )
        self.quick_record_button.pack(fill="x")
    
    def create_quick_actions(self, parent):
        """Create quick action buttons"""
        actions_frame = ctk.CTkFrame(parent, fg_color="transparent")
        actions_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkLabel(
            actions_frame,
            text="⚡ Quick Actions",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=["#333333", "#ffffff"]
        ).pack(anchor="w", pady=(0, 10))
        
        # Button grid
        button_grid = ctk.CTkFrame(actions_frame, fg_color="transparent")
        button_grid.pack(fill="x")
        button_grid.grid_columnconfigure((0, 1), weight=1)
        
        # File operations
        self.file_button = ctk.CTkButton(
            button_grid,
            text="📁 Open File",
            command=self.open_file,
            height=35,
            font=ctk.CTkFont(size=12),
            fg_color=["#17a2b8", "#0ea5e9"],
            corner_radius=8
        )
        self.file_button.grid(row=0, column=0, sticky="ew", padx=(0, 5), pady=2)
        
        self.export_button = ctk.CTkButton(
            button_grid,
            text="💾 Export",
            command=self.export_session,
            height=35,
            font=ctk.CTkFont(size=12),
            fg_color=["#fd7e14", "#f59e0b"],
            corner_radius=8
        )
        self.export_button.grid(row=0, column=1, sticky="ew", padx=(5, 0), pady=2)
        
        # Output controls
        self.clipboard_button = ctk.CTkButton(
            button_grid,
            text="📋 Clipboard",
            command=self.toggle_clipboard,
            height=35,
            font=ctk.CTkFont(size=12),
            fg_color=["#6c757d", "#6b7280"],
            corner_radius=8
        )
        self.clipboard_button.grid(row=1, column=0, sticky="ew", padx=(0, 5), pady=2)
        
        self.typing_button = ctk.CTkButton(
            button_grid,
            text="⌨️ Typing",
            command=self.toggle_typing,
            height=35,
            font=ctk.CTkFont(size=12),
            fg_color=["#dc3545", "#ef4444"],
            corner_radius=8
        )
        self.typing_button.grid(row=1, column=1, sticky="ew", padx=(5, 0), pady=2)
        
        self.clear_button = ctk.CTkButton(
            button_grid,
            text="🗑️ Clear",
            command=self.clear_output,
            height=35,
            font=ctk.CTkFont(size=12),
            fg_color=["#6c757d", "#374151"],
            corner_radius=8
        )
        self.clear_button.grid(row=2, column=0, columnspan=2, sticky="ew", pady=2)
    
    def create_settings_section(self, parent):
        """Create settings section"""
        settings_frame = ctk.CTkFrame(parent, fg_color="transparent")
        settings_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkLabel(
            settings_frame,
            text="⚙️ Settings",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=["#333333", "#ffffff"]
        ).pack(anchor="w", pady=(0, 10))
        
        # Model selection
        model_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        model_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            model_frame,
            text="Model:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=["#666666", "#8b949e"]
        ).pack(anchor="w")
        
        self.model_selector = ctk.CTkOptionMenu(
            model_frame,
            values=["tiny", "base", "small", "medium", "large"],
            command=self.change_model,
            height=35,
            font=ctk.CTkFont(size=12),
            corner_radius=8
        )
        self.model_selector.pack(fill="x", pady=(5, 0))
        self.model_selector.set(self.config.whisper.model_size)
    
    def create_output_area(self, parent):
        """Create modern output area with syntax highlighting"""
        output_container = ctk.CTkFrame(
            parent,
            fg_color=["#ffffff", "#0d1117"],
            corner_radius=20
        )
        output_container.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=(10, 0))
        output_container.grid_columnconfigure(0, weight=1)
        output_container.grid_rowconfigure(1, weight=1)
        
        # Output header with stats
        output_header = ctk.CTkFrame(
            output_container,
            height=60,
            fg_color=["#f8f9fa", "#161b22"],
            corner_radius=15
        )
        output_header.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 10))
        output_header.grid_propagate(False)
        output_header.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            output_header,
            text="📝 Live Transcription",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=["#333333", "#f0f6fc"]
        ).grid(row=0, column=0, sticky="w", padx=20, pady=15)
        
        self.stats_label = ctk.CTkLabel(
            output_header,
            text="Ready",
            font=ctk.CTkFont(size=12),
            text_color=["#666666", "#8b949e"]
        )
        self.stats_label.grid(row=0, column=1, sticky="e", padx=20, pady=15)
        
        # Output text area with modern styling
        self.output_text = ctk.CTkTextbox(
            output_container,
            font=ctk.CTkFont(family="Consolas", size=14),
            fg_color=["#ffffff", "#0d1117"],
            text_color=["#333333", "#e6edf3"],
            corner_radius=15,
            border_width=0
        )
        self.output_text.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        
        # Welcome message
        welcome_text = """🎉 Welcome to WisprClone Pro!

Your professional AI-powered speech recognition system is ready.

✨ Features:
• Real-time speech transcription
• Multiple language support  
• High accuracy AI models
• Professional output formatting
• YouTube-ready interface

🎙️ Click "Start Recording" to begin transcribing your speech!

"""
        self.output_text.insert("1.0", welcome_text)
    
    def create_modern_status(self):
        """Create modern status bar"""
        status_frame = ctk.CTkFrame(
            self.main_container,
            height=50,
            fg_color=["#f8f9fa", "#21262d"],
            corner_radius=15
        )
        status_frame.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        status_frame.grid_propagate(False)
        status_frame.grid_columnconfigure(1, weight=1)
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="🟢 System Ready",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=["#28a745", "#2ea043"]
        )
        self.status_label.grid(row=0, column=0, sticky="w", padx=20, pady=15)
        
        # Version info
        version_label = ctk.CTkLabel(
            status_frame,
            text="WisprClone Pro v1.0 | OpenAI Whisper",
            font=ctk.CTkFont(size=10),
            text_color=["#666666", "#8b949e"]
        )
        version_label.grid(row=0, column=1, sticky="e", padx=20, pady=15)
    
    def setup_animations(self):
        """Setup subtle animations and effects"""
        pass
    
    def animation_loop(self):
        """Main animation loop for visual effects"""
        try:
            if self.is_recording:
                # Pulsing effect for recording button
                self.recording_animation += 0.1
                alpha = (math.sin(self.recording_animation) + 1) / 2
                
                # Update recording indicator
                if hasattr(self, 'recording_status_label'):
                    self.recording_status_label.configure(
                        text="🔴 Recording..." if alpha > 0.5 else "⚫ Recording..."
                    )
            
            # Schedule next animation frame
            self.root.after(100, self.animation_loop)
            
        except Exception as e:
            # Fail silently for animations
            self.root.after(1000, self.animation_loop)
    
    # Core functionality methods (same as original but with modern UI updates)
    def initialize_components(self):
        """Initialize all components"""
        try:
            # Update status
            self.root.after(0, lambda: self.update_status("🔄 Loading AI model...", "#ff6b35"))
            
            # Initialize transcriber
            self.transcriber = WhisperTranscriber(self.config)
            self.transcriber.load_model(self.config.whisper.model_size)
            
            # Initialize audio processor
            self.audio_processor = AudioProcessor(self.config)
            
            # Initialize output handler
            self.output_handler = OutputHandler(self.config)
            
            # Initialize hotkey manager
            try:
                self.hotkey_manager = HotkeyManager(self.config)
                self.hotkey_manager.register_hotkey("toggle_recording", self.toggle_recording)
                self.hotkey_manager.register_hotkey("stop_recording", self.stop_recording)
                self.hotkey_manager.register_hotkey("toggle_typing", self.toggle_typing)
                self.hotkey_manager.register_hotkey("clear_output", self.clear_output)
            except Exception as e:
                print(f"Hotkey registration failed: {e}")
            
            self.is_initialized = True
            self.root.after(0, self.update_ui_after_init)
            
        except Exception as e:
            self.root.after(0, lambda: self.update_status(f"❌ Initialization failed: {str(e)}", "#dc3545"))
    
    def update_ui_after_init(self):
        """Update UI after initialization"""
        model_info = self.transcriber.get_model_info()
        model_text = f"✅ {model_info.get('model_size', 'unknown').title()} Model Ready"
        self.model_status.configure(text=model_text, text_color=["#28a745", "#2ea043"])
        self.update_status("🟢 System Ready - Start Recording!", "#28a745")
        
        # Update button states
        self.update_button_states()
    
    def update_status(self, message: str, color: str = None):
        """Update status with color"""
        if hasattr(self, 'status_label'):
            self.status_label.configure(text=message)
            if color:
                self.status_label.configure(text_color=color)
    
    def update_button_states(self):
        """Update button appearances based on state"""
        if self.config.output.output_to_clipboard:
            self.clipboard_button.configure(fg_color=["#28a745", "#2ea043"])
        
        if self.config.output.typing_enabled:
            self.typing_button.configure(fg_color=["#28a745", "#2ea043"])
    
    # Include all the core methods from the original GUI
    def toggle_recording(self):
        """Toggle recording with visual feedback"""
        if not self.is_initialized:
            messagebox.showwarning("Warning", "System is still initializing. Please wait.")
            return
        
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()
    
    def start_recording(self):
        """Start recording with modern visual feedback"""
        if self.is_recording:
            return
        
        self.is_recording = True
        self.record_button.configure(
            text="⏹️ Stop Recording",
            fg_color=["#dc3545", "#ef4444"],
            hover_color=["#c82333", "#dc2626"]
        )
        
        # Start transcription callback
        def transcription_callback(result):
            self.root.after(0, lambda: self.handle_transcription_result(result))
        
        def audio_callback(audio_data, sample_rate):
            if self.transcriber:
                self.transcriber.queue_audio_for_transcription(audio_data, sample_rate)
        
        # Start transcription and recording
        self.transcriber.start_real_time_transcription(transcription_callback)
        self.audio_processor.start_recording(audio_callback)
        
        self.update_status("🎙️ Recording in progress...", "#dc3545")
    
    def stop_recording(self):
        """Stop recording"""
        if not self.is_recording:
            return
        
        self.is_recording = False
        self.record_button.configure(
            text="🎤 Start Recording",
            fg_color=["#28a745", "#238636"],
            hover_color=["#218838", "#2ea043"]
        )
        
        if self.audio_processor:
            self.audio_processor.stop_recording()
        
        if self.transcriber:
            self.transcriber.stop_real_time_transcription()
        
        self.update_status("✅ Recording stopped", "#28a745")
    
    def handle_transcription_result(self, result: Dict[str, Any]):
        """Handle transcription with modern formatting"""
        if "error" in result:
            # Don't show filtered results as errors in UI
            if "rejected" in result["error"].lower() or "too short" in result["error"].lower():
                return
            
            self.append_output(f"❌ {result['error']}\n", "error")
            return
        
        text = result.get("text", "").strip()
        if not text:
            return
        
        # Modern formatting
        timestamp = time.strftime('%H:%M:%S')
        language = result.get("language", "unknown").upper()
        confidence = result.get("confidence", 0.0)
        processing_time = result.get("processing_time", 0.0)
        
        # Beautiful output formatting
        output = f"""╭─ [{timestamp}] {language} ─ ✨{confidence:.0%} ─ ⚡{processing_time:.2f}s ─╮
│ {text}
╰─────────────────────────────────────────────────────╯

"""
        self.append_output(output)
        
        # Update statistics
        if self.transcriber:
            stats = self.transcriber.get_statistics()
            stats_text = f"📊 {stats.get('total_transcriptions', 0)} transcriptions │ ⚡ {stats.get('average_processing_time', 0):.2f}s avg"
            self.stats_label.configure(text=stats_text)
        
        # Handle output
        if self.output_handler:
            self.output_handler.handle_transcription(result)
    
    def append_output(self, text: str, tag: str = "normal"):
        """Append text with modern styling"""
        self.output_text.insert("end", text)
        self.output_text.see("end")
    
    # Include other methods from original GUI...
    def toggle_clipboard(self):
        """Toggle clipboard with visual feedback"""
        self.config.output.output_to_clipboard = not self.config.output.output_to_clipboard
        self.config.save()
        
        if self.output_handler:
            self.output_handler.update_typing_config()
        
        status = "enabled" if self.config.output.output_to_clipboard else "disabled"
        self.update_status(f"📋 Clipboard {status}", "#17a2b8")
        
        # Update button appearance
        if self.config.output.output_to_clipboard:
            self.clipboard_button.configure(fg_color=["#28a745", "#2ea043"])
        else:
            self.clipboard_button.configure(fg_color=["#6c757d", "#6b7280"])
    
    def toggle_typing(self):
        """Toggle typing with visual feedback"""
        self.config.output.typing_enabled = not self.config.output.typing_enabled
        self.config.save()
        
        if self.output_handler:
            self.output_handler.update_typing_config()
        
        status = "enabled" if self.config.output.typing_enabled else "disabled"
        self.update_status(f"⌨️ Auto-typing {status}", "#6f42c1")
        
        # Update button appearance
        if self.config.output.typing_enabled:
            self.typing_button.configure(fg_color=["#28a745", "#2ea043"])
        else:
            self.typing_button.configure(fg_color=["#dc3545", "#ef4444"])
    
    def clear_output(self):
        """Clear output with confirmation"""
        self.output_text.delete("1.0", "end")
        if self.output_handler:
            self.output_handler.clear_session_log()
        self.update_status("🗑️ Output cleared", "#6c757d")
    
    def change_model(self, new_model):
        """Change AI model"""
        self.config.whisper.model_size = new_model
        self.config.save()
        
        self.update_status("🔄 Loading new model...", "#ff6b35")
        
        def reload_model():
            try:
                self.transcriber.load_model(new_model)
                self.root.after(0, lambda: self.update_status(f"✅ {new_model.title()} model loaded", "#28a745"))
            except Exception as e:
                self.root.after(0, lambda: self.update_status(f"❌ Model loading failed", "#dc3545"))
        
        threading.Thread(target=reload_model, daemon=True).start()
    
    def quick_record(self):
        """Quick 5-second recording"""
        if not self.is_initialized:
            messagebox.showwarning("Warning", "System is still initializing.")
            return
        
        self.update_status("⚡ Quick recording...", "#6f42c1")
        
        def record_thread():
            try:
                audio_data = self.audio_processor.record_audio_chunk(5.0)
                if audio_data is None:
                    self.root.after(0, lambda: messagebox.showerror("Error", "Recording failed"))
                    return
                
                result = self.transcriber.transcribe_audio(audio_data, self.config.audio.sample_rate)
                self.root.after(0, lambda: self.handle_transcription_result(result))
                self.root.after(0, lambda: self.update_status("✅ Quick recording completed", "#28a745"))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Recording failed: {str(e)}"))
        
        threading.Thread(target=record_thread, daemon=True).start()
    
    def open_file(self):
        """Open and transcribe audio file"""
        if not self.is_initialized:
            messagebox.showwarning("Warning", "System still initializing.")
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
                self.root.after(0, lambda: self.update_status(f"🎵 Processing {Path(file_path).name}...", "#17a2b8"))
                result = self.transcriber.transcribe_file(file_path)
                self.root.after(0, lambda: self.handle_transcription_result(result))
                self.root.after(0, lambda: self.update_status("✅ File processed", "#28a745"))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"File processing failed: {str(e)}"))
        
        threading.Thread(target=transcribe_thread, daemon=True).start()
    
    def export_session(self):
        """Export session log"""
        if not self.output_handler or not self.output_handler.session_log:
            messagebox.showinfo("Info", "No session data to export")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Export Session",
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt"),
                ("JSON Files", "*.json"), 
                ("CSV Files", "*.csv")
            ]
        )
        
        if file_path:
            ext = Path(file_path).suffix.lower()
            format_type = {"json": "json", ".csv": "csv"}.get(ext, "txt")
            
            if self.output_handler.export_session_log(file_path, format_type):
                messagebox.showinfo("Success", f"Session exported to {file_path}")
    
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
            print(f"Cleanup error: {e}")
            self.root.destroy()
    
    def run(self):
        """Run the modern GUI"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()


def main():
    """Main entry point for modern GUI"""
    try:
        app = ModernWisprCloneGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"Failed to start WisprClone: {str(e)}")


if __name__ == "__main__":
    main() 