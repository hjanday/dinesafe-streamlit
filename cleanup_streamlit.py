#!/usr/bin/env python3
"""
simple cleanup script for local development only
this wont work on streamlit cloud but helps with local testing
"""

import subprocess
import os
import sys

def kill_streamlit_processes():
    """kill any running streamlit processes on your local machine"""
    print("Cleaning up streamlit processes...")
    
    try:
        if os.name == 'nt':  # windows
            # kill streamlit processes
            result = subprocess.run(['taskkill', '/f', '/im', 'streamlit.exe'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("Killed streamlit processes")
            else:
                print("No streamlit processes found")
                
        else:  # mac/linux
            result = subprocess.run(['pkill', '-f', 'streamlit'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("Killed streamlit processes")
            else:
                print("No streamlit processes found")
                
    except Exception as e:
        print(f"Error during cleanup: {e}")

def check_port_usage(port=8501):
    """check if a port is being used"""
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            print(f"Port {port} is available")
            return True
    except OSError:
        print(f"Port {port} is in use")
        return False

if __name__ == "__main__":
    print("Streamlit Cleanup Tool")
    print("=" * 25)
    
    kill_streamlit_processes()
    
    print("\nChecking port availability...")
    check_port_usage(8501)
    
    print("\nCleanup done! You can run your dashboard now.")
