import threading
from typing import Dict, Callable, Optional
try:
    import keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False
    print("Warning: keyboard module not available. Hotkeys will be disabled.")

from ..core.config import Config


class HotkeyManager:
    """Manage global hotkeys for WisprClone"""
    
    def __init__(self, config: Config):
        self.config = config
        self.hotkeys = {}
        self.callbacks = {}
        self.enabled = KEYBOARD_AVAILABLE
        
        if not KEYBOARD_AVAILABLE:
            print("Hotkey management is disabled due to missing keyboard module")
    
    def register_hotkey(self, name: str, hotkey_combo: str, callback: Callable) -> bool:
        """Register a global hotkey"""
        if not self.enabled:
            print(f"Cannot register hotkey '{name}': keyboard module not available")
            return False
        
        try:
            # Remove existing hotkey if it exists
            if name in self.hotkeys:
                self.unregister_hotkey(name)
            
            # Register new hotkey
            keyboard.add_hotkey(hotkey_combo, callback)
            self.hotkeys[name] = hotkey_combo
            self.callbacks[name] = callback
            
            print(f"Hotkey registered: {name} -> {hotkey_combo}")
            return True
            
        except Exception as e:
            print(f"Error registering hotkey '{name}': {e}")
            return False
    
    def unregister_hotkey(self, name: str) -> bool:
        """Unregister a hotkey"""
        if not self.enabled:
            return False
        
        try:
            if name in self.hotkeys:
                hotkey_combo = self.hotkeys[name]
                keyboard.remove_hotkey(hotkey_combo)
                del self.hotkeys[name]
                del self.callbacks[name]
                print(f"Hotkey unregistered: {name}")
                return True
            else:
                print(f"Hotkey '{name}' not found")
                return False
                
        except Exception as e:
            print(f"Error unregistering hotkey '{name}': {e}")
            return False
    
    def setup_default_hotkeys(self, callbacks: Dict[str, Callable]) -> None:
        """Setup default hotkeys from config"""
        if not self.enabled:
            return
        
        default_hotkeys = {
            "toggle_recording": self.config.hotkeys.toggle_recording,
            "stop_recording": self.config.hotkeys.stop_recording,
            "toggle_typing": self.config.hotkeys.toggle_typing,
            "clear_output": self.config.hotkeys.clear_output
        }
        
        for name, hotkey_combo in default_hotkeys.items():
            if name in callbacks:
                self.register_hotkey(name, hotkey_combo, callbacks[name])
    
    def update_hotkey(self, name: str, new_hotkey_combo: str) -> bool:
        """Update an existing hotkey combination"""
        if not self.enabled:
            return False
        
        if name not in self.callbacks:
            print(f"Hotkey '{name}' not found")
            return False
        
        callback = self.callbacks[name]
        
        # Unregister old hotkey
        self.unregister_hotkey(name)
        
        # Register with new combination
        success = self.register_hotkey(name, new_hotkey_combo, callback)
        
        if success:
            # Update config
            if hasattr(self.config.hotkeys, name):
                setattr(self.config.hotkeys, name, new_hotkey_combo)
                self.config.save()
        
        return success
    
    def get_registered_hotkeys(self) -> Dict[str, str]:
        """Get list of currently registered hotkeys"""
        return self.hotkeys.copy()
    
    def is_hotkey_available(self, hotkey_combo: str) -> bool:
        """Check if a hotkey combination is available (not already registered)"""
        return hotkey_combo not in self.hotkeys.values()
    
    def validate_hotkey_combo(self, hotkey_combo: str) -> bool:
        """Validate if a hotkey combination is valid"""
        if not self.enabled:
            return False
        
        try:
            # Try to parse the hotkey combination
            # This is a simple validation - keyboard module will validate properly
            parts = hotkey_combo.lower().split('+')
            
            # Check for valid modifier keys
            valid_modifiers = ['ctrl', 'alt', 'shift', 'win', 'cmd']
            valid_keys = [
                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12',
                'space', 'enter', 'tab', 'escape', 'backspace', 'delete', 'insert',
                'home', 'end', 'page up', 'page down', 'up', 'down', 'left', 'right',
                '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
            ]
            
            # Must have at least one key
            if len(parts) == 0:
                return False
            
            # Last part should be the main key
            main_key = parts[-1].strip()
            if main_key not in valid_keys:
                return False
            
            # Check modifiers
            for part in parts[:-1]:
                modifier = part.strip()
                if modifier not in valid_modifiers:
                    return False
            
            return True
            
        except Exception as e:
            print(f"Error validating hotkey combo '{hotkey_combo}': {e}")
            return False
    
    def test_hotkey(self, hotkey_combo: str, test_callback: Optional[Callable] = None) -> bool:
        """Test a hotkey combination"""
        if not self.enabled:
            return False
        
        if not self.validate_hotkey_combo(hotkey_combo):
            print(f"Invalid hotkey combination: {hotkey_combo}")
            return False
        
        try:
            def test_func():
                print(f"Test hotkey triggered: {hotkey_combo}")
                if test_callback:
                    test_callback()
            
            # Register temporary hotkey
            test_name = f"_test_{hotkey_combo}"
            success = self.register_hotkey(test_name, hotkey_combo, test_func)
            
            if success:
                print(f"Test hotkey registered. Press {hotkey_combo} to test...")
                # Note: In a real application, you might want to automatically
                # unregister the test hotkey after some time
                
            return success
            
        except Exception as e:
            print(f"Error testing hotkey: {e}")
            return False
    
    def disable_all_hotkeys(self) -> None:
        """Disable all registered hotkeys"""
        if not self.enabled:
            return
        
        hotkey_names = list(self.hotkeys.keys())
        for name in hotkey_names:
            self.unregister_hotkey(name)
        
        print("All hotkeys disabled")
    
    def enable_hotkeys(self) -> bool:
        """Enable hotkey functionality"""
        if not KEYBOARD_AVAILABLE:
            print("Cannot enable hotkeys: keyboard module not available")
            return False
        
        self.enabled = True
        print("Hotkeys enabled")
        return True
    
    def disable_hotkeys(self) -> None:
        """Disable hotkey functionality"""
        self.disable_all_hotkeys()
        self.enabled = False
        print("Hotkeys disabled")
    
    def get_hotkey_info(self) -> Dict:
        """Get information about hotkey system"""
        return {
            "enabled": self.enabled,
            "keyboard_available": KEYBOARD_AVAILABLE,
            "registered_hotkeys": len(self.hotkeys),
            "hotkeys": self.get_registered_hotkeys()
        }
    
    def cleanup(self) -> None:
        """Clean up hotkey manager"""
        if self.enabled:
            self.disable_all_hotkeys()
        print("Hotkey manager cleaned up")
    
    def __del__(self):
        """Destructor to cleanup hotkeys"""
        try:
            self.cleanup()
        except:
            pass 