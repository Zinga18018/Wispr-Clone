#!/usr/bin/env python3
"""
🎬 WisprClone Pro - YouTube Edition
Ultra-modern, sleek GUI perfect for YouTube content creation and demonstrations
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import messagebox, filedialog
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


# Ultra-modern dark theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class YouTubeWisprCloneGUI:
    """🎬 Professional YouTube-Ready WisprClone Interface ✨"""
    
    def __init__(self):
        self.config = Config()
        self.transcriber = None
        self.audio_processor = None
        self.output_handler = None
        self.hotkey_manager = None
        
        self.is_recording = False
        self.is_initialized = False
        self.animation_frame = 0
        
        # Create main window with professional styling
        self.root = ctk.CTk()
        self.root.title("🎤 WisprClone Pro - YouTube Edition")
        self.root.geometry("1300x850")
        self.root.minsize(1100, 700)
        self.root.configure(fg_color="#0a0a0a")
        
        self.setup_professional_ui()
        threading.Thread(target=self.initialize_system, daemon=True).start()
        self.start_visual_effects()
    
    def setup_professional_ui(self):
        """Setup professional YouTube-ready interface"""
        # Main container
        self.main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.create_professional_header()
        self.create_main_workspace()
        self.create_status_footer()
    
    def create_professional_header(self):
        """Create professional header perfect for YouTube recordings"""
        header = ctk.CTkFrame(
            self.main_container,
            height=85,
            fg_color="#1a1a1a",
            corner_radius=15,
            border_width=1,
            border_color="#333333"
        )
        header.pack(fill="x", pady=(0, 20))
        header.pack_propagate(False)
        
        # Brand section
        brand_frame = ctk.CTkFrame(header, fg_color="transparent")
        brand_frame.pack(side="left", fill="y", padx=25, pady=15)
        
        main_title = ctk.CTkLabel(
            brand_frame,
            text="🎤 WisprClone Pro",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#00D4FF"
        )
        main_title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            brand_frame,
            text="Professional AI Speech Recognition • YouTube Edition",
            font=ctk.CTkFont(size=11),
            text_color="#888888"
        )
        subtitle.pack(anchor="w", pady=(2, 0))
        
        # System status
        status_frame = ctk.CTkFrame(header, fg_color="transparent")
        status_frame.pack(side="right", fill="y", padx=25, pady=15)
        
        self.system_status = ctk.CTkLabel(
            status_frame,
            text="🤖 AI: Loading...",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#FF6B35"
        )
        self.system_status.pack(anchor="e")
        
        self.audio_status = ctk.CTkLabel(
            status_frame,
            text="🎙️ Audio: Ready",
            font=ctk.CTkFont(size=10),
            text_color="#00FF88"
        )
        self.audio_status.pack(anchor="e", pady=(3, 0))
    
    def create_main_workspace(self):
        """Create main workspace with modern layout"""
        workspace = ctk.CTkFrame(self.main_container, fg_color="transparent")
        workspace.pack(fill="both", expand=True)
        
        # Control panel (left side)
        self.create_control_panel(workspace)
        
        # Output area (right side)
        self.create_output_area(workspace)
    
    def create_control_panel(self, parent):
        """Create sleek control panel"""
        control_panel = ctk.CTkFrame(
            parent,
            width=370,
            fg_color="#1a1a1a",
            corner_radius=15,
            border_width=1,
            border_color="#333333"
        )
        control_panel.pack(side="left", fill="y", padx=(0, 15))
        control_panel.pack_propagate(False)
        
        # Recording controls
        self.create_recording_controls(control_panel)
        
        # AI settings
        self.create_ai_controls(control_panel)
        
        # Action buttons
        self.create_action_buttons(control_panel)
    
    def create_recording_controls(self, parent):
        """Create modern recording controls"""
        recording_section = ctk.CTkFrame(parent, fg_color="transparent")
        recording_section.pack(fill="x", padx=20, pady=20)
        
        # Section header
        ctk.CTkLabel(
            recording_section,
            text="🎙️ Recording Studio",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color="#FFFFFF"
        ).pack(anchor="w", pady=(0, 15))
        
        # Main record button with glow effect
        self.record_button = ctk.CTkButton(
            recording_section,
            text="🎤 Start Recording",
            command=self.toggle_recording,
            height=55,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#FF3366",
            hover_color="#FF1155",
            corner_radius=12
        )
        self.record_button.pack(fill="x", pady=(0, 15))
        
        # Recording status indicator
        self.recording_status_frame = ctk.CTkFrame(
            recording_section,
            height=40,
            fg_color="#2a2a2a",
            corner_radius=8
        )
        self.recording_status_frame.pack(fill="x", pady=(0, 15))
        
        self.recording_status_label = ctk.CTkLabel(
            self.recording_status_frame,
            text="🔴 Ready to Record",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#CCCCCC"
        )
        self.recording_status_label.pack(pady=10)
        
        # Quick record button
        ctk.CTkButton(
            recording_section,
            text="⚡ Quick Record (5s)",
            command=self.quick_record,
            height=35,
            font=ctk.CTkFont(size=12),
            fg_color="#8B5CF6",
            hover_color="#7C3AED",
            corner_radius=8
        ).pack(fill="x")
    
    def create_ai_controls(self, parent):
        """Create AI model controls"""
        ai_section = ctk.CTkFrame(parent, fg_color="transparent")
        ai_section.pack(fill="x", padx=20, pady=(10, 20))
        
        ctk.CTkLabel(
            ai_section,
            text="🤖 AI Configuration",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#FFFFFF"
        ).pack(anchor="w", pady=(0, 10))
        
        # Model selection
        model_frame = ctk.CTkFrame(ai_section, fg_color="#2a2a2a", corner_radius=8)
        model_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            model_frame,
            text="Model:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#AAAAAA"
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        self.model_selector = ctk.CTkOptionMenu(
            model_frame,
            values=["tiny", "base", "small", "medium", "large"],
            command=self.change_model,
            height=30,
            font=ctk.CTkFont(size=11),
            fg_color="#3a3a3a",
            corner_radius=6
        )
        self.model_selector.pack(fill="x", padx=15, pady=(0, 15))
        self.model_selector.set(self.config.whisper.model_size)
    
    def create_action_buttons(self, parent):
        """Create quick action buttons"""
        actions_section = ctk.CTkFrame(parent, fg_color="transparent")
        actions_section.pack(fill="x", padx=20, pady=(10, 20))
        
        ctk.CTkLabel(
            actions_section,
            text="⚡ Quick Actions",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#FFFFFF"
        ).pack(anchor="w", pady=(0, 10))
        
        # Button grid
        button_grid = ctk.CTkFrame(actions_section, fg_color="transparent")
        button_grid.pack(fill="x")
        
        # Row 1
        row1 = ctk.CTkFrame(button_grid, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 8))
        
        self.clipboard_button = ctk.CTkButton(
            row1,
            text="📋 Clipboard",
            command=self.toggle_clipboard,
            height=32,
            width=110,
            font=ctk.CTkFont(size=10),
            fg_color="#17A2B8",
            corner_radius=6
        )
        self.clipboard_button.pack(side="left", padx=(0, 8))
        
        self.typing_button = ctk.CTkButton(
            row1,
            text="⌨️ Auto-type",
            command=self.toggle_typing,
            height=32,
            width=110,
            font=ctk.CTkFont(size=10),
            fg_color="#28A745",
            corner_radius=6
        )
        self.typing_button.pack(side="left")
        
        # Row 2
        row2 = ctk.CTkFrame(button_grid, fg_color="transparent")
        row2.pack(fill="x", pady=(0, 8))
        
        ctk.CTkButton(
            row2,
            text="📁 File",
            command=self.open_file,
            height=32,
            width=110,
            font=ctk.CTkFont(size=10),
            fg_color="#FD7E14",
            corner_radius=6
        ).pack(side="left", padx=(0, 8))
        
        ctk.CTkButton(
            row2,
            text="💾 Export",
            command=self.export_session,
            height=32,
            width=110,
            font=ctk.CTkFont(size=10),
            fg_color="#6C757D",
            corner_radius=6
        ).pack(side="left")
        
        # Clear button
        ctk.CTkButton(
            button_grid,
            text="🗑️ Clear Output",
            command=self.clear_output,
            height=32,
            font=ctk.CTkFont(size=10),
            fg_color="#DC3545",
            corner_radius=6
        ).pack(fill="x")
    
    def create_output_area(self, parent):
        """Create professional output area"""
        output_panel = ctk.CTkFrame(
            parent,
            fg_color="#1a1a1a",
            corner_radius=15,
            border_width=1,
            border_color="#333333"
        )
        output_panel.pack(side="right", fill="both", expand=True)
        
        # Output header
        output_header = ctk.CTkFrame(
            output_panel,
            height=50,
            fg_color="#2a2a2a",
            corner_radius=10
        )
        output_header.pack(fill="x", padx=15, pady=(15, 10))
        output_header.pack_propagate(False)
        
        ctk.CTkLabel(
            output_header,
            text="📝 Live Transcription",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFFFFF"
        ).pack(side="left", padx=20, pady=12)
        
        self.statistics_label = ctk.CTkLabel(
            output_header,
            text="Ready for transcription",
            font=ctk.CTkFont(size=10),
            text_color="#AAAAAA"
        )
        self.statistics_label.pack(side="right", padx=20, pady=12)
        
        # Main output text area
        self.output_textbox = ctk.CTkTextbox(
            output_panel,
            font=ctk.CTkFont(family="Consolas", size=13),
            fg_color="#0a0a0a",
            text_color="#E6E6E6",
            corner_radius=10,
            border_width=1,
            border_color="#333333",
            wrap="word"
        )
        self.output_textbox.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Welcome message
        welcome_text = """🎉 Welcome to WisprClone Pro - YouTube Edition!

Your professional AI speech recognition system is ready for content creation.

✨ YouTube-Ready Features:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Ultra-modern interface perfect for video recording
• Real-time speech transcription with high accuracy
• Advanced noise filtering to reduce false positives
• Multiple AI model sizes for different needs
• Professional output formatting
• Auto-typing for live demonstrations
• Export capabilities for content workflows

🎬 Perfect for YouTube Content:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Software tutorials and demonstrations
• Live coding with voice commentary
• Educational content with accessibility
• Professional presentation recordings
• Podcast and interview transcriptions

🚀 Ready to create amazing content? Click "Start Recording" to begin!
"""
        self.output_textbox.insert("0.0", welcome_text)
    
    def create_status_footer(self):
        """Create professional status footer"""
        footer = ctk.CTkFrame(
            self.main_container,
            height=40,
            fg_color="#1a1a1a",
            corner_radius=10,
            border_width=1,
            border_color="#333333"
        )
        footer.pack(fill="x", pady=(15, 0))
        footer.pack_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            footer,
            text="🟢 System Ready for Content Creation",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#00FF88"
        )
        self.status_label.pack(side="left", padx=20, pady=10)
        
        version_label = ctk.CTkLabel(
            footer,
            text="WisprClone Pro v1.0 • YouTube Edition • OpenAI Whisper",
            font=ctk.CTkFont(size=9),
            text_color="#666666"
        )
        version_label.pack(side="right", padx=20, pady=10)
    
    def start_visual_effects(self):
        """Start visual effects and animations"""
        self.animate_interface()
    
    def animate_interface(self):
        """Animate interface elements"""
        try:
            if self.is_recording:
                self.animation_frame += 0.15
                pulse = (math.sin(self.animation_frame) + 1) / 2
                
                if pulse > 0.5:
                    self.recording_status_label.configure(
                        text="🔴 RECORDING LIVE",
                        text_color="#FF3366"
                    )
                else:
                    self.recording_status_label.configure(
                        text="⚪ RECORDING LIVE",
                        text_color="#FF6699"
                    )
            
            self.root.after(200, self.animate_interface)
        except:
            self.root.after(1000, self.animate_interface)
    
    # Core functionality methods
    def initialize_system(self):
        """Initialize all system components"""
        try:
            self.update_main_status("🔄 Loading AI Model...", "#FF6B35")
            
            # Initialize transcriber
            self.transcriber = WhisperTranscriber(self.config)
            self.transcriber.load_model(self.config.whisper.model_size)
            
            # Initialize audio processor
            self.audio_processor = AudioProcessor(self.config)
            
            # Initialize output handler
            self.output_handler = OutputHandler(self.config)
            
            # Initialize hotkeys
            try:
                self.hotkey_manager = HotkeyManager(self.config)
                self.hotkey_manager.register_hotkey("toggle_recording", self.toggle_recording)
                self.hotkey_manager.register_hotkey("stop_recording", self.stop_recording)
                self.hotkey_manager.register_hotkey("toggle_typing", self.toggle_typing)
                self.hotkey_manager.register_hotkey("clear_output", self.clear_output)
            except Exception as e:
                print(f"Hotkey setup failed: {e}")
            
            self.is_initialized = True
            self.root.after(0, self.complete_initialization)
            
        except Exception as e:
            self.root.after(0, lambda: self.update_main_status(f"❌ Initialization failed: {str(e)}", "#FF3366"))
    
    def complete_initialization(self):
        """Complete system initialization"""
        model_info = self.transcriber.get_model_info()
        model_size = model_info.get('model_size', 'unknown').title()
        
        self.system_status.configure(
            text=f"🤖 AI: {model_size} Ready",
            text_color="#00FF88"
        )
        
        self.update_main_status("🟢 All Systems Ready - Perfect for YouTube!", "#00FF88")
        self.update_button_appearances()
    
    def update_main_status(self, message, color="#FFFFFF"):
        """Update main status message"""
        if hasattr(self, 'status_label'):
            self.status_label.configure(text=message, text_color=color)
    
    def update_button_appearances(self):
        """Update button visual states"""
        if self.config.output.output_to_clipboard:
            self.clipboard_button.configure(fg_color="#00FF88")
        
        if self.config.output.typing_enabled:
            self.typing_button.configure(fg_color="#00FF88")
    
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
        
        self.record_button.configure(
            text="⏹️ Stop Recording",
            fg_color="#FF0033",
            hover_color="#DD0022"
        )
        
        def transcription_callback(result):
            self.root.after(0, lambda: self.process_transcription(result))
        
        def audio_callback(audio_data, sample_rate):
            if self.transcriber:
                self.transcriber.queue_audio_for_transcription(audio_data, sample_rate)
        
        self.transcriber.start_real_time_transcription(transcription_callback)
        self.audio_processor.start_recording(audio_callback)
        
        self.update_main_status("🎙️ Recording Active - Creating Content!", "#FF3366")
    
    def stop_recording(self):
        """Stop recording session"""
        self.is_recording = False
        
        self.record_button.configure(
            text="🎤 Start Recording",
            fg_color="#FF3366",
            hover_color="#FF1155"
        )
        
        self.recording_status_label.configure(
            text="🔴 Ready to Record",
            text_color="#CCCCCC"
        )
        
        if self.audio_processor:
            self.audio_processor.stop_recording()
        if self.transcriber:
            self.transcriber.stop_real_time_transcription()
        
        self.update_main_status("✅ Recording Complete - Ready for Next Session!", "#00FF88")
    
    def process_transcription(self, result):
        """Process transcription results with professional formatting"""
        if "error" in result:
            # Silently skip filtered results
            error_msg = result["error"].lower()
            if any(keyword in error_msg for keyword in ["rejected", "too short", "repetitive"]):
                return
            return
        
        text = result.get("text", "").strip()
        if not text:
            return
        
        # Professional YouTube formatting
        timestamp = time.strftime('%H:%M:%S')
        language = result.get("language", "unknown").upper()
        confidence = result.get("confidence", 0.0) * 100
        processing_time = result.get("processing_time", 0.0)
        
        formatted_output = f"""
┌─ 🎬 [{timestamp}] {language} ─ ✨ {confidence:.0f}% ─ ⚡ {processing_time:.2f}s ──────────────────────┐
│                                                                                         │
│  "{text}"
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────┘

"""
        
        self.output_textbox.insert("end", formatted_output)
        self.output_textbox.see("end")
        
        # Update statistics
        if self.transcriber:
            stats = self.transcriber.get_statistics()
            total = stats.get('total_transcriptions', 0)
            avg_time = stats.get('average_processing_time', 0)
            self.statistics_label.configure(text=f"📊 {total} transcriptions • ⚡ {avg_time:.2f}s avg")
        
        # Handle output processing
        if self.output_handler:
            self.output_handler.handle_transcription(result)
    
    def toggle_clipboard(self):
        """Toggle clipboard output"""
        self.config.output.output_to_clipboard = not self.config.output.output_to_clipboard
        self.config.save()
        
        color = "#00FF88" if self.config.output.output_to_clipboard else "#17A2B8"
        self.clipboard_button.configure(fg_color=color)
        
        status = "ON" if self.config.output.output_to_clipboard else "OFF"
        self.update_main_status(f"📋 Clipboard: {status}", color)
    
    def toggle_typing(self):
        """Toggle auto-typing feature"""
        self.config.output.typing_enabled = not self.config.output.typing_enabled
        self.config.save()
        
        if self.output_handler:
            self.output_handler.update_typing_config()
        
        color = "#00FF88" if self.config.output.typing_enabled else "#28A745"
        self.typing_button.configure(fg_color=color)
        
        status = "ON" if self.config.output.typing_enabled else "OFF"
        self.update_main_status(f"⌨️ Auto-typing: {status}", color)
    
    def clear_output(self):
        """Clear output display"""
        self.output_textbox.delete("0.0", "end")
        if self.output_handler:
            self.output_handler.clear_session_log()
        self.update_main_status("🗑️ Output Cleared - Fresh Start!", "#6C757D")
    
    def change_model(self, new_model):
        """Change AI model"""
        self.config.whisper.model_size = new_model
        self.config.save()
        
        self.update_main_status(f"🔄 Loading {new_model.title()} Model...", "#FF6B35")
        
        def reload_model():
            try:
                self.transcriber.load_model(new_model)
                self.root.after(0, lambda: self.update_main_status(f"✅ {new_model.title()} Model Ready!", "#00FF88"))
                self.root.after(0, lambda: self.system_status.configure(
                    text=f"🤖 AI: {new_model.title()} Ready",
                    text_color="#00FF88"
                ))
            except Exception as e:
                self.root.after(0, lambda: self.update_main_status("❌ Model Loading Failed", "#FF3366"))
        
        threading.Thread(target=reload_model, daemon=True).start()
    
    def quick_record(self):
        """Quick 5-second recording"""
        if not self.is_initialized:
            messagebox.showwarning("Not Ready", "System still initializing...")
            return
        
        self.update_main_status("⚡ Quick Recording Session...", "#8B5CF6")
        
        def record_audio():
            try:
                audio_data = self.audio_processor.record_audio_chunk(5.0)
                if audio_data is None:
                    self.root.after(0, lambda: messagebox.showerror("Error", "Recording failed"))
                    return
                
                result = self.transcriber.transcribe_audio(audio_data, self.config.audio.sample_rate)
                self.root.after(0, lambda: self.process_transcription(result))
                self.root.after(0, lambda: self.update_main_status("✅ Quick Recording Complete!", "#00FF88"))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Recording failed: {str(e)}"))
        
        threading.Thread(target=record_audio, daemon=True).start()
    
    def open_file(self):
        """Open audio file for transcription"""
        if not self.is_initialized:
            messagebox.showwarning("Not Ready", "System still initializing...")
            return
        
        file_path = filedialog.askopenfilename(
            title="Select Audio File",
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
                self.root.after(0, lambda: self.update_main_status(f"🎵 Processing {filename}...", "#FD7E14"))
                
                result = self.transcriber.transcribe_file(file_path)
                self.root.after(0, lambda: self.process_transcription(result))
                self.root.after(0, lambda: self.update_main_status("✅ File Processing Complete!", "#00FF88"))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Processing failed: {str(e)}"))
        
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
                ("CSV Files", "*.csv")
            ]
        )
        
        if file_path:
            try:
                ext = Path(file_path).suffix.lower()
                format_type = "json" if ext == ".json" else "csv" if ext == ".csv" else "txt"
                
                if self.output_handler.export_session_log(file_path, format_type):
                    messagebox.showinfo("Success", f"Session exported successfully!\n\nFile: {file_path}")
                    self.update_main_status("💾 Export Successful!", "#00FF88")
                
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def on_application_close(self):
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
        """Launch the YouTube-ready GUI"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_application_close)
        self.root.mainloop()


def main():
    """Main entry point"""
    try:
        print("🎬 Launching WisprClone Pro - YouTube Edition...")
        app = YouTubeWisprCloneGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Launch Error", f"Failed to start WisprClone: {str(e)}")


if __name__ == "__main__":
    main() 