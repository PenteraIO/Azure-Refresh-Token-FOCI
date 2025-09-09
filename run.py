#!/usr/bin/env python3
"""
Azure AD Refresh Token Utility - Launcher
Simple launcher script to run either CLI or web version.
"""

import sys
import os
import subprocess

def main():
    """Main launcher function."""
    print("=== Azure AD Refresh Token Utility ===\n")
    print("Choose an option:")
    print("1. CLI Version (Interactive)")
    print("2. Web Version (Browser Interface)")
    print("3. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            print("\nStarting CLI version...")
            try:
                subprocess.run([sys.executable, 'cli.py'], check=True)
            except KeyboardInterrupt:
                print("\nCLI interrupted by user.")
            except Exception as e:
                print(f"Error running CLI: {e}")
            break
            
        elif choice == '2':
            print("\nStarting web version...")
            print("The web interface will be available at: http://localhost:5001")
            print("Press Ctrl+C to stop the web server.")
            try:
                subprocess.run([sys.executable, 'web_app.py'], check=True)
            except KeyboardInterrupt:
                print("\nWeb server stopped.")
            except Exception as e:
                print(f"Error running web app: {e}")
            break
            
        elif choice == '3':
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main() 