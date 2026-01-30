"""
WorkPulse Mascot Library
Modular components for the animated mascot widget
"""

from .character import MascotTheme, MascotCharacter
from .notifications import NotificationListener
from .monitors import GitActivityMonitor, MeetingDetector
from .speech import SpeechBubble

__all__ = [
    'MascotTheme',
    'MascotCharacter',
    'NotificationListener',
    'GitActivityMonitor',
    'MeetingDetector',
    'SpeechBubble',
]
