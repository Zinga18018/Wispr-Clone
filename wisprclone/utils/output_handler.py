import os
import time
import pyperclip
from pathlib import Path
from typing import Dict, Any, Optional
from ..core.config import Config


class OutputHandler:
    """Handle different output formats for transcribed text"""
    
    def __init__(self, config: Config):
        self.config = config
        self.output_file = None
        self.session_log = []
        
        # Initialize output file if enabled
        if config.output.output_to_file:
            self._initialize_output_file()
    
    def _initialize_output_file(self) -> None:
        """Initialize output file for transcription logging"""
        try:
            output_path = Path(self.config.output.output_file_path)
            
            # Create directory if it doesn't exist
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Open file in append mode
            self.output_file = open(output_path, 'a', encoding='utf-8')
            
            # Write session header
            self.output_file.write(f"\n--- WisprClone Session Started: {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
            self.output_file.flush()
            
            print(f"Output file initialized: {output_path}")
            
        except Exception as e:
            print(f"Error initializing output file: {e}")
            self.output_file = None
    
    def handle_transcription(self, result: Dict[str, Any]) -> None:
        """Process and output transcription result"""
        if "error" in result:
            self._handle_error(result)
            return
        
        text = result.get("text", "").strip()
        if not text:
            return
        
        # Add to session log
        log_entry = {
            "timestamp": time.time(),
            "text": text,
            "language": result.get("language", "unknown"),
            "confidence": result.get("confidence", 0.0),
            "processing_time": result.get("processing_time", 0.0)
        }
        self.session_log.append(log_entry)
        
        # Output to different targets
        if self.config.output.output_to_console:
            self._output_to_console(text, result)
        
        if self.config.output.output_to_clipboard:
            self._output_to_clipboard(text)
        
        if self.config.output.output_to_file and self.output_file:
            self._output_to_file(text, result)
        
        if self.config.output.typing_enabled:
            from .typing_simulator import TypingSimulator
            typing_sim = TypingSimulator(self.config)
            typing_sim.type_text(text)
    
    def _handle_error(self, result: Dict[str, Any]) -> None:
        """Handle transcription errors"""
        error_msg = result.get("error", "Unknown error")
        print(f"Transcription Error: {error_msg}")
        
        if self.output_file:
            self.output_file.write(f"ERROR: {error_msg} [{time.strftime('%H:%M:%S')}]\n")
            self.output_file.flush()
    
    def _output_to_console(self, text: str, result: Dict[str, Any]) -> None:
        """Output transcription to console"""
        timestamp = time.strftime('%H:%M:%S')
        language = result.get("language", "unknown")
        confidence = result.get("confidence", 0.0)
        processing_time = result.get("processing_time", 0.0)
        
        print(f"\n[{timestamp}] ({language}, {confidence:.2f}, {processing_time:.2f}s)")
        print(f"📝 {text}")
        print("-" * 50)
    
    def _output_to_clipboard(self, text: str) -> None:
        """Copy transcription to clipboard"""
        try:
            # Get existing clipboard content
            try:
                existing_content = pyperclip.paste()
            except:
                existing_content = ""
            
            # Append new text (or replace if empty)
            if existing_content and not existing_content.endswith('\n'):
                new_content = existing_content + " " + text
            else:
                new_content = existing_content + text
            
            pyperclip.copy(new_content)
            print(f"📋 Copied to clipboard: {text[:50]}{'...' if len(text) > 50 else ''}")
            
        except Exception as e:
            print(f"Error copying to clipboard: {e}")
    
    def _output_to_file(self, text: str, result: Dict[str, Any]) -> None:
        """Write transcription to file"""
        try:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            language = result.get("language", "unknown")
            confidence = result.get("confidence", 0.0)
            
            # Write formatted entry
            self.output_file.write(f"[{timestamp}] ({language}, {confidence:.2f}) {text}\n")
            self.output_file.flush()
            
        except Exception as e:
            print(f"Error writing to file: {e}")
    
    def export_session_log(self, export_path: str, format: str = "txt") -> bool:
        """Export session log to file"""
        try:
            export_file_path = Path(export_path)
            export_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            if format.lower() == "json":
                import json
                with open(export_file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.session_log, f, indent=2, ensure_ascii=False)
            
            elif format.lower() == "csv":
                import csv
                with open(export_file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Timestamp", "Text", "Language", "Confidence", "Processing Time"])
                    for entry in self.session_log:
                        writer.writerow([
                            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(entry["timestamp"])),
                            entry["text"],
                            entry["language"],
                            entry["confidence"],
                            entry["processing_time"]
                        ])
            
            else:  # txt format
                with open(export_file_path, 'w', encoding='utf-8') as f:
                    f.write(f"WisprClone Session Log\n")
                    f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Total Entries: {len(self.session_log)}\n")
                    f.write("=" * 50 + "\n\n")
                    
                    for entry in self.session_log:
                        timestamp_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(entry["timestamp"]))
                        f.write(f"[{timestamp_str}] ({entry['language']}, {entry['confidence']:.2f})\n")
                        f.write(f"{entry['text']}\n\n")
            
            print(f"Session log exported to: {export_file_path}")
            return True
            
        except Exception as e:
            print(f"Error exporting session log: {e}")
            return False
    
    def get_session_statistics(self) -> Dict[str, Any]:
        """Get statistics about current session"""
        if not self.session_log:
            return {}
        
        total_entries = len(self.session_log)
        total_words = sum(len(entry["text"].split()) for entry in self.session_log)
        total_chars = sum(len(entry["text"]) for entry in self.session_log)
        
        # Calculate averages
        avg_confidence = sum(entry["confidence"] for entry in self.session_log) / total_entries
        avg_processing_time = sum(entry["processing_time"] for entry in self.session_log) / total_entries
        
        # Language distribution
        languages = {}
        for entry in self.session_log:
            lang = entry["language"]
            languages[lang] = languages.get(lang, 0) + 1
        
        # Session duration
        if total_entries > 1:
            session_duration = self.session_log[-1]["timestamp"] - self.session_log[0]["timestamp"]
        else:
            session_duration = 0
        
        return {
            "total_entries": total_entries,
            "total_words": total_words,
            "total_characters": total_chars,
            "average_confidence": avg_confidence,
            "average_processing_time": avg_processing_time,
            "session_duration": session_duration,
            "languages": languages,
            "words_per_minute": (total_words / (session_duration / 60)) if session_duration > 0 else 0
        }
    
    def clear_session_log(self) -> None:
        """Clear current session log"""
        self.session_log.clear()
        print("Session log cleared")
    
    def close(self) -> None:
        """Close output handler and cleanup"""
        if self.output_file:
            try:
                self.output_file.write(f"\n--- WisprClone Session Ended: {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
                self.output_file.close()
                print("Output file closed")
            except Exception as e:
                print(f"Error closing output file: {e}")
        
        self.output_file = None
    
    def __del__(self):
        """Destructor to ensure file is closed"""
        self.close() 