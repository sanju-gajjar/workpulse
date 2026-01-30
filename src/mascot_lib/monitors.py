"""
Activity Monitors Module
Handles Git activity and meeting call detection
"""

import os
import time
import random
import subprocess


class GitActivityMonitor:
    """Monitors git activity by checking recent git commands"""
    
    GIT_CELEBRATION_MESSAGES = [
        "Nice commit! 🎉",
        "Code pushed! 🚀",
        "Git magic! ✨",
        "Version controlled! 📦",
        "Changes saved! 💾",
        "Great progress! 🌟",
        "Keep committing! 💪",
    ]
    
    GIT_PULL_MESSAGES = [
        "Synced up! 🔄",
        "Got latest! 📥",
        "Updated! ✅",
    ]
    
    def __init__(self):
        self.last_check_time = time.time()
        self.last_git_activity = None
        self.git_log_file = os.path.expanduser("~/.local/share/workpulse/git_activity.log")
        self.check_interval = 30  # seconds
        
    def check_recent_git_activity(self):
        """Check if any git command was run recently"""
        try:
            # Check bash/zsh history for recent git commands
            history_files = [
                os.path.expanduser("~/.bash_history"),
                os.path.expanduser("~/.zsh_history"),
            ]
            
            current_time = time.time()
            
            for hist_file in history_files:
                if os.path.exists(hist_file):
                    # Check if file was modified in last 60 seconds
                    mtime = os.path.getmtime(hist_file)
                    if current_time - mtime < 60:
                        # Read last few lines
                        with open(hist_file, 'r', errors='ignore') as f:
                            lines = f.readlines()[-10:]
                        
                        for line in reversed(lines):
                            line = line.strip().lower()
                            # Check for git commands
                            if 'git commit' in line or 'git push' in line:
                                if self.last_git_activity != 'commit':
                                    self.last_git_activity = 'commit'
                                    return ('commit', random.choice(self.GIT_CELEBRATION_MESSAGES))
                            elif 'git pull' in line or 'git fetch' in line:
                                if self.last_git_activity != 'pull':
                                    self.last_git_activity = 'pull'
                                    return ('pull', random.choice(self.GIT_PULL_MESSAGES))
            
            # Reset after some time
            if current_time - self.last_check_time > 120:
                self.last_git_activity = None
                
        except Exception:
            pass
        
        return None
    
    def get_celebration_message(self, activity_type):
        if activity_type == 'commit':
            return random.choice(self.GIT_CELEBRATION_MESSAGES)
        elif activity_type == 'pull':
            return random.choice(self.GIT_PULL_MESSAGES)
        return None


class MeetingDetector:
    """Detects active meeting calls (Zoom, Google Meet, Teams)"""
    
    def __init__(self):
        self.in_meeting = False
        self.meeting_app = None
        self.enabled = True
    
    def check_meeting_call(self):
        """
        Check for active meeting windows
        Returns: (is_in_meeting, app_name) or None
        """
        if not self.enabled:
            return None
        
        try:
            # Get all window titles
            result = subprocess.run(
                ['wmctrl', '-l'],
                capture_output=True,
                text=True,
                timeout=2
            )
            
            if result.returncode != 0:
                return None
            
            windows = result.stdout.lower()
            detected_app = None
            
            # Check for Zoom meeting
            if 'zoom meeting' in windows or 'zoom workplace' in windows:
                detected_app = 'Zoom'
            
            # Check for Google Meet
            elif 'meet.google.com' in windows or '- google meet' in windows:
                detected_app = 'Google Meet'
            
            # Check for Microsoft Teams
            elif 'microsoft teams' in windows and ('| call' in windows or '| meeting' in windows):
                detected_app = 'Teams'
            
            # Return state change if detected
            current_in_meeting = detected_app is not None
            
            if current_in_meeting != self.in_meeting:
                self.in_meeting = current_in_meeting
                self.meeting_app = detected_app
                return (current_in_meeting, detected_app)
            
            return None
            
        except subprocess.TimeoutExpired:
            pass
        except FileNotFoundError:
            # wmctrl not installed, disable feature
            self.enabled = False
        except Exception:
            pass
        
        return None
