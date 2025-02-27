#!/usr/bin/env python3
import os
import json
import getpass
from pathlib import Path
import base64
import hashlib

# ANSI escape sequences for colors
RESET = "\033[0m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"

class ConfigManager:
    def __init__(self, debug=False):
        self.debug = debug
        
        # Set up config directory in user's home folder
        self.config_dir = os.path.join(Path.home(), '.router-reboot')
        self.config_file = os.path.join(self.config_dir, 'config.json')
        
        # Ensure config directory exists
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
    
    def debug_print(self, message):
        """Print debug messages only if debug mode is enabled."""
        if self.debug:
            print(f"{CYAN}[DEBUG]{RESET} {message}")
    
    def encode_password(self, password):
        """Simple encoding to avoid plain text storage (not secure for sensitive data)"""
        return base64.b64encode(password.encode()).decode()
    
    def decode_password(self, encoded):
        """Decode the encoded password"""
        try:
            return base64.b64decode(encoded.encode()).decode()
        except:
            return ""
    
    def load_config(self):
        """Load configuration from file or create with defaults"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    
                # If we have an encoded password, decode it
                if config.get('password_encoded', False):
                    config['password'] = self.decode_password(config['password'])
                
                # Always ensure we use the fixed URL regardless of what's saved
                config['url'] = 'http://192.168.29.1/platform.cgi'
                
                self.debug_print(f"Loaded config: {config}")
                return config
            except Exception as e:
                self.debug_print(f"Error loading config: {e}")
                return self.get_default_config()
        else:
            return self.get_default_config()
    
    def get_default_config(self):
        """Return default configuration"""
        return {
            'url': 'http://192.168.29.1/platform.cgi',  # Fixed URL
            'username': '',
            'password': '',
            'configured': False
        }
    
    def save_config(self, config):
        """Save configuration to file"""
        # Make a copy to avoid modifying the original
        config_to_save = config.copy()
        
        # Encode password before saving
        if config_to_save.get('password'):
            config_to_save['password'] = self.encode_password(config_to_save['password'])
            config_to_save['password_encoded'] = True
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config_to_save, f)
            self.debug_print(f"Config saved to {self.config_file}")
            return True
        except Exception as e:
            self.debug_print(f"Error saving config: {e}")
            return False
    
    def prompt_for_credentials(self, config=None):
        """Interactive prompt for router credentials"""
        if config is None:
            config = self.get_default_config()
        
        print(f"\n{CYAN}Router Reboot - Initial Setup{RESET}")
        print(f"{YELLOW}Please enter your router credentials:{RESET}\n")
        
        # Fixed URL - not configurable
        print(f"Router URL: http://192.168.29.1/platform.cgi (fixed)")
        
        # Get username with default
        default_username = config.get('username', 'admin')
        username = input(f"Username [{default_username}]: ").strip()
        if not username:
            username = default_username
        
        # Get password (hide input)
        password = getpass.getpass("Password: ")
        
        # Update config
        config['url'] = 'http://192.168.29.1/platform.cgi'  # Fixed URL
        config['username'] = username
        if password:
            config['password'] = password
        config['configured'] = True
        
        # Save config
        if self.save_config(config):
            print(f"\n{GREEN}Configuration saved successfully!{RESET}\n")
        else:
            print(f"\n{RED}Failed to save configuration!{RESET}\n")
        
        return config
