"""
Notification Listener Module
Handles system notifications via DBus
"""

import threading
from gi.repository import GLib

try:
    import dbus
    from dbus.mainloop.glib import DBusGMainLoop
    HAS_DBUS = True
except ImportError:
    HAS_DBUS = False


class NotificationListener:
    """Listens to system notifications via DBus and forwards them to mascot"""
    
    # Apps to ignore (add your own noise apps here)
    IGNORED_APPS = [
        'workpulse', 'workpulse-mascot',  # Don't show our own notifications
        'spotify', 'vlc',  # Media players
        'chrome', 'firefox',  # Browsers (too noisy)
    ]
    
    # Apps to prioritize (always show these)
    PRIORITY_APPS = [
        'slack', 'teams', 'discord', 'telegram', 'signal',  # Messaging
        'thunderbird', 'evolution', 'geary',  # Email
        'git', 'github',  # Git notifications
        'jenkins', 'gitlab', 'jira', 'clickup',  # Work tools
    ]
    
    def __init__(self, callback):
        self.callback = callback  # Function to call with notification
        self.enabled = True
        self.show_all = False  # If True, show all notifications
        self.listener_thread = None
        self.running = False
        
    def start(self):
        """Start listening for notifications in background thread"""
        if not HAS_DBUS:
            return False
        
        self.running = True
        self.listener_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listener_thread.start()
        return True
    
    def stop(self):
        self.running = False
        
    def set_enabled(self, enabled):
        self.enabled = enabled
        
    def set_show_all(self, show_all):
        self.show_all = show_all
    
    def _listen_loop(self):
        """Background thread to listen for DBus notifications"""
        try:
            DBusGMainLoop(set_as_default=True)
            bus = dbus.SessionBus()
            
            # Connect to notification signals
            bus.add_match_string(
                "interface='org.freedesktop.Notifications',"
                "member='Notify',"
                "eavesdrop='true'"
            )
            bus.add_message_filter(self._on_notification)
            
            # Run the loop
            loop = GLib.MainLoop()
            while self.running:
                GLib.MainContext.default().iteration(True)
                
        except Exception as e:
            print(f"Notification listener error: {e}")
    
    def _on_notification(self, bus, message):
        """Handle incoming notification"""
        try:
            if not self.enabled:
                return
                
            args = message.get_args_list()
            if len(args) >= 4:
                app_name = str(args[0]).lower()
                summary = str(args[3])
                body = str(args[4]) if len(args) > 4 else ""
                
                # Check if we should show this notification
                if self._should_show(app_name):
                    # Truncate for display
                    display_text = summary[:30]
                    if body:
                        display_text += f": {body[:20]}"
                    if len(display_text) > 50:
                        display_text = display_text[:47] + "..."
                    
                    # Add app icon
                    if 'slack' in app_name:
                        display_text = f"💬 {display_text}"
                    elif 'teams' in app_name:
                        display_text = f"👥 {display_text}"
                    elif 'mail' in app_name or 'thunder' in app_name:
                        display_text = f"📧 {display_text}"
                    elif 'git' in app_name:
                        display_text = f"🔀 {display_text}"
                    else:
                        display_text = f"🔔 {display_text}"
                    
                    # Call back to main thread
                    GLib.idle_add(self.callback, display_text, app_name)
                    
        except Exception:
            pass
    
    def _should_show(self, app_name):
        """Determine if notification should be shown"""
        if self.show_all:
            return app_name not in [a.lower() for a in self.IGNORED_APPS]
        
        # Only show priority apps by default
        for priority_app in self.PRIORITY_APPS:
            if priority_app in app_name:
                return True
        return False
