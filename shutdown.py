import subprocess
import sys
import time
from datetime import datetime

def shutdown_pc(delay_seconds=0, reason=""):
    """
    Shuts down the PC after a specified delay.
    """
    try:
        if delay_seconds > 0:
            print(f"PC will shut down in {delay_seconds} seconds...")
            print("Press Ctrl+C to cancel")
            time.sleep(delay_seconds)
        
        if sys.platform == "win32":
            subprocess.run(["shutdown", "/s", "/t", "0"], check=True)
        else:  # Linux/Mac
            subprocess.run(["shutdown", "-h", "now"], check=True)
        
        print("Shutting down...")
        
    except KeyboardInterrupt:
        print("\n✗ Shutdown cancelled!")
        sys.exit(0)
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)

def main():
    print("PC Shutdown Helper")
    print("-" * 40)
    
    try:
        delay = input("Enter delay in seconds (0 for immediate): ").strip()
        delay = int(delay) if delay else 0
        
        if delay < 0:
            print("✗ Delay cannot be negative!")
            sys.exit(1)
        
        reason = input("Optional reason for shutdown: ").strip()
        
        if delay > 0:
            confirm = input(f"Shutdown in {delay} seconds? (yes/no): ").strip().lower()
            if confirm != "yes":
                print("Cancelled.")
                sys.exit(0)
        
        shutdown_pc(delay, reason)
        
    except ValueError:
        print("✗ Please enter a valid number for delay!")
        sys.exit(1)

if __name__ == "__main__":
    main()