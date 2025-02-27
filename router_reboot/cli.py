#!/usr/bin/env python3
import argparse
from .rebooter import RouterRebooter
from .config import ConfigManager

def main():
    """Command line entry point for the router reboot utility."""
    parser = argparse.ArgumentParser(description="Router Reboot Utility - Reboot your JioFiber router")
    
    parser.add_argument("--debug", 
                        action="store_true", 
                        help="Enable debug mode")
    
    parser.add_argument("--configure", 
                        action="store_true", 
                        help="Configure or reconfigure router credentials")
    
    args = parser.parse_args()
    
    # Initialize config manager
    config_manager = ConfigManager(debug=args.debug)
    
    # Load saved config
    config = config_manager.load_config()
    
    # If not configured or explicitly asked to configure
    if args.configure or not config.get('configured', False):
        config = config_manager.prompt_for_credentials(config)
    
    # Removed override logic for username and password
    
    # Initialize and run the router rebooter
    rebooter = RouterRebooter(
        base_url=config['url'],
        username=config['username'],
        password=config['password'], 
        debug=args.debug
    )
    rebooter.run()

if __name__ == "__main__":
    main()
