#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

import json
import os
import sys
from pathlib import Path
from datetime import datetime

def get_session_log_dir(session_id):
    """
    Get the session-specific log directory.
    Creates it if it doesn't exist.
    """
    # Get project root from hook location
    hook_path = Path(__file__).resolve()
    project_root = hook_path.parent.parent.parent
    
    session_dir = project_root / 'logs' / 'sessions' / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    
    # Update last-activity timestamp
    activity_file = session_dir / 'last-activity'
    activity_file.write_text(datetime.now().isoformat())
    
    return session_dir

def main():
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)
        
        # Get session ID from input data
        session_id = input_data.get('session_id', 'unknown')
        
        # Get session-specific log directory
        session_log_dir = get_session_log_dir(session_id)
        log_path = session_log_dir / 'post_tool_use.json'
        
        # Read existing log data or initialize empty list
        if log_path.exists():
            with open(log_path, 'r') as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []
        
        # Append new data
        log_data.append(input_data)
        
        # Write back to file with formatting
        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        sys.exit(0)
        
    except json.JSONDecodeError:
        # Handle JSON decode errors gracefully
        sys.exit(0)
    except Exception:
        # Exit cleanly on any other error
        sys.exit(0)

if __name__ == '__main__':
    main()