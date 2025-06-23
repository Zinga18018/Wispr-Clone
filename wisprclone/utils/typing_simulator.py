import time
import threading
from typing import Optional
try:
    import keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False
    print("Warning: keyboard module not available. Typing simulation will be disabled.")

from ..core.config import Config


class TypingSimulator:
    """Simulate keyboard typing for transcribed text"""
    
    def __init__(self, config: Config):
        self.config = config
        self.is_typing = False
        self.typing_thread = None
        self.typing_queue = []
        self.enabled = KEYBOARD_AVAILABLE and config.output.typing_enabled
        
        if not KEYBOARD_AVAILABLE:
            print("Typing simulation is disabled due to missing keyboard module")
    
    def type_text(self, text: str, delay: Optional[float] = None) -> None:
        """Type text character by character"""
        if not self.enabled:
            return
        
        # Use provided delay or config delay
        typing_delay = delay if delay is not None else self.config.output.typing_delay
        
        # Add to typing queue
        self.typing_queue.append((text, typing_delay))
        
        # Start typing thread if not already running
        if not self.is_typing:
            self._start_typing_thread()
    
    def _start_typing_thread(self) -> None:
        """Start the typing thread"""
        if self.typing_thread and self.typing_thread.is_alive():
            return
        
        self.is_typing = True
        self.typing_thread = threading.Thread(target=self._typing_worker)
        self.typing_thread.daemon = True
        self.typing_thread.start()
    
    def _typing_worker(self) -> None:
        """Worker thread for typing simulation"""
        while self.is_typing and self.typing_queue:
            try:
                text, delay = self.typing_queue.pop(0)
                self._simulate_typing(text, delay)
            except Exception as e:
                print(f"Error in typing simulation: {e}")
        
        self.is_typing = False
    
    def _simulate_typing(self, text: str, delay: float) -> None:
        """Simulate typing with realistic delays"""
        if not KEYBOARD_AVAILABLE:
            return
        
        try:
            # Add a small initial delay
            time.sleep(0.1)
            
            for char in text:
                if not self.enabled:
                    break
                
                # Handle special characters
                if char == '\n':
                    keyboard.press_and_release('enter')
                elif char == '\t':
                    keyboard.press_and_release('tab')
                elif char == ' ':
                    keyboard.press_and_release('space')
                else:
                    # Type regular character
                    keyboard.write(char)
                
                # Add typing delay with some randomization
                actual_delay = delay * (0.8 + 0.4 * hash(char) % 100 / 100)
                time.sleep(actual_delay)
            
            # Add space after the text
            keyboard.press_and_release('space')
            
        except Exception as e:
            print(f"Error simulating typing: {e}")
    
    def type_word_by_word(self, text: str, word_delay: float = 0.1) -> None:
        """Type text word by word instead of character by character"""
        if not self.enabled:
            return
        
        words = text.split()
        for i, word in enumerate(words):
            if not self.enabled:
                break
            
            try:
                keyboard.write(word)
                if i < len(words) - 1:  # Add space between words
                    keyboard.press_and_release('space')
                    time.sleep(word_delay)
            except Exception as e:
                print(f"Error typing word '{word}': {e}")
                break
    
    def enable_typing(self) -> bool:
        """Enable typing simulation"""
        if not KEYBOARD_AVAILABLE:
            print("Cannot enable typing: keyboard module not available")
            return False
        
        self.enabled = True
        self.config.output.typing_enabled = True
        self.config.save()
        print("Typing simulation enabled")
        return True
    
    def disable_typing(self) -> None:
        """Disable typing simulation"""
        self.enabled = False
        self.config.output.typing_enabled = False
        self.config.save()
        print("Typing simulation disabled")
    
    def toggle_typing(self) -> bool:
        """Toggle typing simulation on/off"""
        if self.enabled:
            self.disable_typing()
            return False
        else:
            return self.enable_typing()
    
    def clear_typing_queue(self) -> None:
        """Clear the typing queue"""
        self.typing_queue.clear()
        print("Typing queue cleared")
    
    def set_typing_speed(self, delay: float) -> None:
        """Set typing speed (delay between characters)"""
        if delay < 0:
            delay = 0
        elif delay > 1.0:
            delay = 1.0
        
        self.config.output.typing_delay = delay
        self.config.save()
        print(f"Typing delay set to {delay:.3f} seconds")
    
    def get_typing_stats(self) -> dict:
        """Get typing simulation statistics"""
        return {
            "enabled": self.enabled,
            "keyboard_available": KEYBOARD_AVAILABLE,
            "is_typing": self.is_typing,
            "queue_length": len(self.typing_queue),
            "typing_delay": self.config.output.typing_delay
        }
    
    def test_typing(self, test_text: str = "Hello, this is a typing test from WisprClone!") -> bool:
        """Test typing simulation"""
        if not self.enabled:
            print("Typing simulation is disabled")
            return False
        
        try:
            print(f"Testing typing in 3 seconds...")
            time.sleep(3)
            print("Typing test text...")
            self.type_text(test_text)
            return True
        except Exception as e:
            print(f"Typing test failed: {e}")
            return False
    
    def stop_typing(self) -> None:
        """Stop current typing operation"""
        self.enabled = False
        self.clear_typing_queue()
        
        if self.typing_thread and self.typing_thread.is_alive():
            self.is_typing = False
            self.typing_thread.join(timeout=1.0)
        
        print("Typing stopped")
    
    def __del__(self):
        """Destructor to cleanup typing thread"""
        self.stop_typing() 