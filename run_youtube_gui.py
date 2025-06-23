#!/usr/bin/env python3
"""
🎬 WisprClone Pro - YouTube Edition Launcher
Ultra-modern GUI perfect for content creation and demonstrations
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from typing import Optional, Dict, Any
import threading
import time
from pathlib import Path
import math

from wisprclone.core.config import Config
from wisprclone.core.transcriber import WhisperTranscriber
from wisprclone.core.audio_processor import AudioProcessor
from wisprclone.utils.output_handler import OutputHandler
from wisprclone.utils.hotkey_manager import HotkeyManager


# Ultra-modern dark theme for YouTube
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class YouTubeWisprCloneGUI:
    """🎬 YouTube-Ready WisprClone with Ultra-Modern UI ✨"""
    
    def __init__(self):
        self.config = Config()
        self.transcriber = None
        self.audio_processor = None
        self.output_handler = None
        self.hotkey_manager = None
        
        self.is_recording = False
        self.is_initialized = False
        self.animation_counter = 0
        
        # Create stunning main window
        self.root = ctk.CTk()
        self.root.title("🎤 WisprClone Pro - YouTube Edition")
        self.root.geometry("1300x850")
        self.root.minsize(1100, 700)
        self.root.configure(fg_color="#0d1117")
        
        self.setup_youtube_ui()
        threading.Thread(target=self.initialize_components, daemon=True).start()
        self.start_animations()
    
    def setup_youtube_ui(self):
        """Setup YouTube-perfect UI"""
        # Main container
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Header with branding
        self.create_header()
        
        # Content area
        self.create_content_area()
        
        # Status bar
        self.create_status_bar()
    
    def create_header(self):
        """Professional header for YouTube"""
        header = ctk.CTkFrame(
            self.main_frame,
            height=90,
            fg_color="#161b22",
            corner_radius=20,
            border_width=1,
            border_color="#30363d"
        )
        header.pack(fill="x", pady=(0, 20))
        header.pack_propagate(False)
        
        # Logo section
        logo_frame = ctk.CTkFrame(header, fg_color="transparent")
        logo_frame.pack(side="left", fill="y", padx=30, pady=15)
        
        title = ctk.CTkLabel(
            logo_frame,
            text="🎤 WisprClone Pro",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#58a6ff"
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            logo_frame,
            text="Professional AI Speech Recognition • YouTube Edition",
            font=ctk.CTkFont(size=12),
            text_color="#7d8590"
        )
        subtitle.pack(anchor="w", pady=(2, 0))
        
        # Status indicators
        status_frame = ctk.CTkFrame(header, fg_color="transparent")
        status_frame.pack(side="right", fill="y", padx=30, pady=15)
        
        self.ai_indicator = ctk.CTkLabel(
            status_frame,
            text="🤖 AI: Loading...",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#f85149"
        )
        self.ai_indicator.pack(anchor="e")
        
        self.mic_indicator = ctk.CTkLabel(
            status_frame,
            text="🎙️ Microphone: Ready",
            font=ctk.CTkFont(size=11),
            text_color="#3fb950"
        )
        self.mic_indicator.pack(anchor="e", pady=(3, 0))
    
    def create_content_area(self):
        """Main content with modern layout"""
        content = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        content.pack(fill="both", expand=True)
        
        # Left panel - Controls
        self.create_control_panel(content)
        
        # Right panel - Output
        self.create_output_panel(content)
    
    def create_control_panel(self, parent):
        """Modern control panel"""
        panel = ctk.CTkFrame(
            parent,
            width=380,
            fg_color="#161b22",
            corner_radius=20,
            border_width=1,
            border_color="#30363d"
        )
        panel.pack(side="left", fill="y", padx=(0, 15))
        panel.pack_propagate(False)
        
        # Recording section
        self.create_recording_section(panel)
        
        # Settings section
        self.create_settings_section(panel)
        
        # Quick actions
        self.create_actions_section(panel)
    
    def create_recording_section(self, parent):
        """Recording controls with animations"""
        section = ctk.CTkFrame(parent, fg_color="transparent")
        section.pack(fill="x", padx=20, pady=20)
        
        # Section title
        ctk.CTkLabel(
            section,
            text="🎙️ Recording Studio",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#f0f6fc"
        ).pack(anchor="w", pady=(0, 15))
        
        # Main record button
        self.record_btn = ctk.CTkButton(
            section,
            text="🎤 Start Recording",
            command=self.toggle_recording,
            height=60,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#238636",
            hover_color="#2ea043",
            corner_radius=15,
            border_width=2,
            border_color="#3fb950"
        )
        self.record_btn.pack(fill="x", pady=(0, 15))
        
        # Status indicator
        self.status_frame = ctk.CTkFrame(
            section,
            height=45,
            fg_color="#21262d",
            corner_radius=10
        )
        self.status_frame.pack(fill="x", pady=(0, 15))
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="🔴 Ready to Record",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#8b949e"
        )
        self.status_label.pack(pady=12)
        
        # Quick record
        ctk.CTkButton(
            section,
            text="⚡ Quick Record (5s)",
            command=self.quick_record,
            height=40,
            font=ctk.CTkFont(size=13),
            fg_color="#8b5cf6",
            hover_color="#7c3aed",
            corner_radius=10
        ).pack(fill="x")
    
    def create_settings_section(self, parent):
        """AI model settings"""
        section = ctk.CTkFrame(parent, fg_color="transparent")
        section.pack(fill="x", padx=20, pady=(10, 20))
        
        ctk.CTkLabel(
            section,
            text="🤖 AI Configuration",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#f0f6fc"
        ).pack(anchor="w", pady=(0, 10))
        
        # Model settings
        model_frame = ctk.CTkFrame(section, fg_color="#21262d", corner_radius=10)
        model_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            model_frame,
            text="Model Size:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#7d8590"
        ).pack(anchor="w", padx=15, pady=(12, 5))
        
        self.model_var = ctk.StringVar(value=self.config.whisper.model_size)
        self.model_selector = ctk.CTkOptionMenu(
            model_frame,
            values=["tiny", "base", "small", "medium", "large"],
            command=self.change_model,
            variable=self.model_var,
            height=35,
            font=ctk.CTkFont(size=12),
            fg_color="#30363d",
            button_color="#484f58",
            corner_radius=8
        )
        self.model_selector.pack(fill="x", padx=15, pady=(0, 15))
    
    def create_actions_section(self, parent):
        """Quick action buttons"""
        section = ctk.CTkFrame(parent, fg_color="transparent")
        section.pack(fill="x", padx=20, pady=(10, 20))
        
        ctk.CTkLabel(
            section,
            text="⚡ Quick Actions",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#f0f6fc"
        ).pack(anchor="w", pady=(0, 10))
        
        # Action buttons grid
        grid = ctk.CTkFrame(section, fg_color="transparent")
        grid.pack(fill="x")
        
        # Row 1
        row1 = ctk.CTkFrame(grid, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 8))
        
        self.clipboard_btn = ctk.CTkButton(
            row1,
            text="📋 Clipboard",
            command=self.toggle_clipboard,
            height=35,
            width=115,
            font=ctk.CTkFont(size=11),
            fg_color="#1f6feb",
            corner_radius=8
        )
        self.clipboard_btn.pack(side="left", padx=(0, 8))
        
        self.typing_btn = ctk.CTkButton(
            row1,
            text="⌨️ Auto-type",
            command=self.toggle_typing,
            height=35,
            width=115,
            font=ctk.CTkFont(size=11),
            fg_color="#238636",
            corner_radius=8
        )
        self.typing_btn.pack(side="left")
        
        # Row 2
        row2 = ctk.CTkFrame(grid, fg_color="transparent")
        row2.pack(fill="x", pady=(0, 8))
        
        ctk.CTkButton(
            row2,
            text="📁 Open File",
            command=self.open_file,
            height=35,
            width=115,
            font=ctk.CTkFont(size=11),
            fg_color="#fb8500",
            corner_radius=8
        ).pack(side="left", padx=(0, 8))
        
        ctk.CTkButton(
            row2,
            text="💾 Export",
            command=self.export_session,
            height=35,
            width=115,
            font=ctk.CTkFont(size=11),
            fg_color="#6f42c1",
            corner_radius=8
        ).pack(side="left")
        
        # Clear button
        ctk.CTkButton(
            grid,
            text="🗑️ Clear Output",
            command=self.clear_output,
            height=35,
            font=ctk.CTkFont(size=11),
            fg_color="#da3633",
            corner_radius=8
        ).pack(fill="x")
    
    def create_output_panel(self, parent):
        """Modern output display"""
        panel = ctk.CTkFrame(
            parent,
            fg_color="#161b22",
            corner_radius=20,
            border_width=1,
            border_color="#30363d"
        )
        panel.pack(side="right", fill="both", expand=True)
        
        # Header
        header = ctk.CTkFrame(panel, height=55, fg_color="#21262d", corner_radius=12)
        header.pack(fill="x", padx=15, pady=(15, 10))
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header,
            text="📝 Live Transcription Output",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#f0f6fc"
        ).pack(side="left", padx=20, pady=15)
        
        self.stats_label = ctk.CTkLabel(
            header,
            text="Ready for transcription",
            font=ctk.CTkFont(size=11),
            text_color="#7d8590"
        )
        self.stats_label.pack(side="right", padx=20, pady=15)
        
        # Output text area
        self.output_text = ctk.CTkTextbox(
            panel,
            font=ctk.CTkFont(family="JetBrains Mono", size=14),
            fg_color="#0d1117",
            text_color="#e6edf3",
            corner_radius=12,
            border_width=1,
            border_color="#30363d",
            wrap="word"
        )
        self.output_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Welcome message
        welcome = """🎉 Welcome to WisprClone Pro - YouTube Edition!

Your professional AI speech recognition system is ready for content creation.

✨ YouTube-Perfect Features:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Ultra-modern, sleek interface optimized for video recording
• Real-time speech transcription with high accuracy
• Multiple language support with auto-detection
• Professional output formatting perfect for demonstrations
• Advanced noise filtering to reduce false positives
• Customizable AI models for different accuracy levels
• Auto-typing feature for live demonstrations
• Export capabilities for content creation workflows

🎬 Perfect for YouTube Content:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Software tutorials and demonstrations
• Live coding sessions with voice commentary
• Educational content with speech-to-text
• Accessibility features for viewers
• Professional presentation recordings
• Podcast and interview transcriptions

🚀 Ready to create amazing content? Click "Start Recording" to begin!

"""
        self.output_text.insert("0.0", welcome)
    
    def create_status_bar(self):
        """Professional status bar"""
        status = ctk.CTkFrame(
            self.main_frame,
            height=45,
            fg_color="#161b22",
            corner_radius=15,
            border_width=1,
            border_color="#30363d"
        )
        status.pack(fill="x", pady=(15, 0))
        status.pack_propagate(False)
        
        self.main_status = ctk.CTkLabel(
            status,
            text="🟢 System Ready for YouTube Content Creation",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#3fb950"
        )
        self.main_status.pack(side="left", padx=20, pady=12)
        
        version_label = ctk.CTkLabel(
            status,
            text="WisprClone Pro v1.0 • YouTube Edition • Powered by OpenAI Whisper",
            font=ctk.CTkFont(size=10),
            text_color="#484f58"
        )
        version_label.pack(side="right", padx=20, pady=12)
    
    def start_animations(self):
        """Start interface animations"""
        self.animate_ui()
    
    def animate_ui(self):
        """Animate UI elements"""
        try:
            if self.is_recording:
                self.animation_counter += 0.2
                pulse = (math.sin(self.animation_counter) + 1) / 2
                
                if pulse > 0.6:
                    self.status_label.configure(
                        text="🔴 LIVE RECORDING",
                        text_color="#f85149"
                    )
                else:
                    self.status_label.configure(
                        text="⚪ LIVE RECORDING",
                        text_color="#f85149"
                    )
            
            self.root.after(200, self.animate_ui)
        except:
            self.root.after(1000, self.animate_ui)
    
    # Core functionality
    def initialize_components(self):
        """Initialize all components"""
        try:
            self.update_status("🔄 Loading AI Model...", "#fb8500")
            
            self.transcriber = WhisperTranscriber(self.config)
            self.transcriber.load_model(self.config.whisper.model_size)
            
            self.audio_processor = AudioProcessor(self.config)
            self.output_handler = OutputHandler(self.config)
            
            try:
                self.hotkey_manager = HotkeyManager(self.config)
                self.hotkey_manager.register_hotkey("toggle_recording", self.toggle_recording)
                self.hotkey_manager.register_hotkey("stop_recording", self.stop_recording)
                self.hotkey_manager.register_hotkey("toggle_typing", self.toggle_typing)
                self.hotkey_manager.register_hotkey("clear_output", self.clear_output)
            except Exception as e:
                print(f"Hotkey setup failed: {e}")
            
            self.is_initialized = True
            self.root.after(0, self.finish_initialization)
            
        except Exception as e:
            self.root.after(0, lambda: self.update_status(f"❌ Initialization failed: {str(e)}", "#f85149"))
    
    def finish_initialization(self):
        """Complete initialization"""
        model_info = self.transcriber.get_model_info()
        model_size = model_info.get('model_size', 'unknown').title()
        
        self.ai_indicator.configure(
            text=f"🤖 AI: {model_size} Model Ready",
            text_color="#3fb950"
        )
        
        self.update_status("🟢 All Systems Ready - Perfect for YouTube Recording!", "#3fb950")
        self.update_button_states()
    
    def update_status(self, message, color="#f0f6fc"):
        """Update main status"""
        if hasattr(self, 'main_status'):
            self.main_status.configure(text=message, text_color=color)
    
    def update_button_states(self):
        """Update button states"""
        if self.config.output.output_to_clipboard:
            self.clipboard_btn.configure(fg_color="#3fb950")
        
        if self.config.output.typing_enabled:
            self.typing_btn.configure(fg_color="#3fb950")
    
    def toggle_recording(self):
        """Toggle recording state"""
        if not self.is_initialized:
            messagebox.showwarning("Not Ready", "System still initializing...")
            return
        
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()
    
    def start_recording(self):
        """Start recording session"""
        self.is_recording = True
        
        self.record_btn.configure(
            text="⏹️ Stop Recording",
            fg_color="#f85149",
            hover_color="#da3633",
            border_color="#f85149"
        )
        
        def transcription_callback(result):
            self.root.after(0, lambda: self.handle_transcription(result))
        
        def audio_callback(audio_data, sample_rate):
            if self.transcriber:
                self.transcriber.queue_audio_for_transcription(audio_data, sample_rate)
        
        self.transcriber.start_real_time_transcription(transcription_callback)
        self.audio_processor.start_recording(audio_callback)
        
        self.update_status("🎙️ Recording Active - Creating Content!", "#f85149")
    
    def stop_recording(self):
        """Stop recording session"""
        self.is_recording = False
        
        self.record_btn.configure(
            text="🎤 Start Recording",
            fg_color="#238636",
            hover_color="#2ea043",
            border_color="#3fb950"
        )
        
        self.status_label.configure(
            text="🔴 Ready to Record",
            text_color="#8b949e"
        )
        
        if self.audio_processor:
            self.audio_processor.stop_recording()
        if self.transcriber:
            self.transcriber.stop_real_time_transcription()
        
        self.update_status("✅ Recording Complete - Ready for Next Session!", "#3fb950")
    
    def handle_transcription(self, result):
        """Handle transcription results"""
        if "error" in result:
            # Skip filtered results silently
            if any(word in result["error"].lower() for word in ["rejected", "too short", "repetitive"]):
                return
            return
        
        text = result.get("text", "").strip()
        if not text:
            return
        
        # Format for YouTube presentation
        timestamp = time.strftime('%H:%M:%S')
        language = result.get("language", "unknown").upper()
        confidence = result.get("confidence", 0.0) * 100
        processing_time = result.get("processing_time", 0.0)
        
        formatted_output = f"""
┌─ 🎬 [{timestamp}] {language} ─ ✨ {confidence:.0f}% ─ ⚡ {processing_time:.2f}s ───────────────────────┐
│                                                                                           │
│  "{text}"
│                                                                                           │
└───────────────────────────────────────────────────────────────────────────────────────┘

"""
        
        self.output_text.insert("end", formatted_output)
        self.output_text.see("end")
        
        # Update stats
        if self.transcriber:
            stats = self.transcriber.get_statistics()
            total = stats.get('total_transcriptions', 0)
            avg_time = stats.get('average_processing_time', 0)
            self.stats_label.configure(text=f"📊 {total} transcriptions • ⚡ {avg_time:.2f}s avg")
        
        if self.output_handler:
            self.output_handler.handle_transcription(result)
    
    def toggle_clipboard(self):
        """Toggle clipboard output"""
        self.config.output.output_to_clipboard = not self.config.output.output_to_clipboard
        self.config.save()
        
        color = "#3fb950" if self.config.output.output_to_clipboard else "#1f6feb"
        self.clipboard_btn.configure(fg_color=color)
        
        status = "ON" if self.config.output.output_to_clipboard else "OFF"
        self.update_status(f"📋 Clipboard Output: {status}", color)
    
    def toggle_typing(self):
        """Toggle auto-typing"""
        self.config.output.typing_enabled = not self.config.output.typing_enabled
        self.config.save()
        
        if self.output_handler:
            self.output_handler.update_typing_config()
        
        color = "#3fb950" if self.config.output.typing_enabled else "#238636"
        self.typing_btn.configure(fg_color=color)
        
        status = "ON" if self.config.output.typing_enabled else "OFF"
        self.update_status(f"⌨️ Auto-typing: {status}", color)
    
    def clear_output(self):
        """Clear output area"""
        self.output_text.delete("0.0", "end")
        if self.output_handler:
            self.output_handler.clear_session_log()
        self.update_status("🗑️ Output Cleared - Fresh Start!", "#7d8590")
    
    def change_model(self, new_model):
        """Change AI model"""
        self.config.whisper.model_size = new_model
        self.config.save()
        
        self.update_status(f"🔄 Loading {new_model.title()} Model...", "#fb8500")
        
        def reload():
            try:
                self.transcriber.load_model(new_model)
                self.root.after(0, lambda: self.update_status(f"✅ {new_model.title()} Model Ready!", "#3fb950"))
                self.root.after(0, lambda: self.ai_indicator.configure(
                    text=f"🤖 AI: {new_model.title()} Model Ready",
                    text_color="#3fb950"
                ))
            except Exception as e:
                self.root.after(0, lambda: self.update_status("❌ Model Loading Failed", "#f85149"))
        
        threading.Thread(target=reload, daemon=True).start()
    
    def quick_record(self):
        """Quick 5-second recording"""
        if not self.is_initialized:
            messagebox.showwarning("Not Ready", "System still initializing...")
            return
        
        self.update_status("⚡ Quick Recording Session...", "#8b5cf6")
        
        def record():
            try:
                audio_data = self.audio_processor.record_audio_chunk(5.0)
                if audio_data is None:
                    self.root.after(0, lambda: messagebox.showerror("Error", "Recording failed"))
                    return
                
                result = self.transcriber.transcribe_audio(audio_data, self.config.audio.sample_rate)
                self.root.after(0, lambda: self.handle_transcription(result))
                self.root.after(0, lambda: self.update_status("✅ Quick Recording Complete!", "#3fb950"))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Recording failed: {str(e)}"))
        
        threading.Thread(target=record, daemon=True).start()
    
    def open_file(self):
        """Open audio file for transcription"""
        if not self.is_initialized:
            messagebox.showwarning("Not Ready", "System still initializing...")
            return
        
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[
                ("Audio Files", "*.wav *.mp3 *.m4a *.ogg *.flac *.aac"),
                ("All Files", "*.*")
            ]
        )
        
        if not file_path:
            return
        
        def process():
            try:
                filename = Path(file_path).name
                self.root.after(0, lambda: self.update_status(f"🎵 Processing {filename}...", "#fb8500"))
                
                result = self.transcriber.transcribe_file(file_path)
                self.root.after(0, lambda: self.handle_transcription(result))
                self.root.after(0, lambda: self.update_status("✅ File Processing Complete!", "#3fb950"))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Processing failed: {str(e)}"))
        
        threading.Thread(target=process, daemon=True).start()
    
    def export_session(self):
        """Export transcription session"""
        if not self.output_handler or not self.output_handler.session_log:
            messagebox.showinfo("No Data", "No transcription data to export")
            return
        
        from tkinter import filedialog
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
            try:
                ext = Path(file_path).suffix.lower()
                format_type = {"json": "json", ".csv": "csv"}.get(ext, "txt")
                
                if self.output_handler.export_session_log(file_path, format_type):
                    messagebox.showinfo("Success", f"Session exported to:\n{file_path}")
                    self.update_status("💾 Export Successful!", "#3fb950")
                
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def on_closing(self):
        """Handle application close"""
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


if __name__ == "__main__":
    try:
        print("🎬 Launching WisprClone Pro - YouTube Edition...")
        app = YouTubeWisprCloneGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Launch Error", f"Failed to start: {str(e)}") 