"""
Speech Bubble Module
Manages mascot's speech bubbles and contextual messages
"""

import time
import random


class SpeechBubble:
    """Manages speech bubbles and motivational messages"""
    
    # Greeting messages (morning, afternoon, evening awareness)
    GREETINGS = [
        "Hey {user}! 👋",
        "Hi there, {user}!",
        "Hello {user}! ✨",
        "What's up, {user}?",
        "Ready to rock, {user}?",
        "Good to see you, {user}!",
    ]
    
    MORNING_GREETINGS = [
        "Good morning, {user}! ☀️",
        "Rise and shine, {user}!",
        "New day, new wins! 🌅",
        "Let's make today count!",
        "Morning, {user}! ☕",
    ]
    
    AFTERNOON_GREETINGS = [
        "Hope your day's going well!",
        "Keep up the great work!",
        "You're doing amazing! 💪",
        "Halfway there, {user}!",
    ]
    
    EVENING_GREETINGS = [
        "Almost there, {user}!",
        "Great progress today! 🌙",
        "Wrapping up nicely!",
        "You did great today!",
    ]
    
    # Motivational quotes when working
    WORKING_QUOTES = [
        "You've got this! 💪",
        "Focus mode: ON 🎯",
        "Making progress!",
        "Deep work time! 🧠",
        "In the zone! ⚡",
        "Crushing it! 🚀",
        "Great focus, {user}!",
        "Keep going!",
        "One step at a time",
        "You're on fire! 🔥",
        "Steady progress 📈",
        "Nice flow! 🌊",
    ]
    
    # Idle/not tracking nudges
    IDLE_NUDGES = [
        "What are you working on?",
        "Ready to start something?",
        "I can help you track!",
        "Click me to begin! 👆",
        "Shall we log some time?",
        "Don't forget to track!",
        "I'm here when you're ready",
        "Any tasks to start?",
    ]
    
    # Break reminders
    BREAK_MESSAGES = [
        "Time for a stretch! 🧘",
        "Coffee break? ☕",
        "Rest those eyes! 👀",
        "Quick breather?",
        "Hydration check! 💧",
        "Stand up and stretch!",
    ]
    
    # Celebration messages
    CELEBRATION_MESSAGES = [
        "Awesome work today! 🎉",
        "You're amazing, {user}!",
        "Great job! ⭐",
        "Productivity champion! 🏆",
        "Nailed it! 💫",
    ]
    
    # Pause messages
    PAUSE_MESSAGES = [
        "Taking a break...",
        "Paused for now",
        "I'll be here! 😊",
        "Rest up!",
        "Catch you later!",
    ]
    
    # Random fun messages
    FUN_MESSAGES = [
        "Beep boop! 🤖",
        "*happy dance*",
        "You're the best!",
        "Let's do this!",
        "*waves*",
        "Thinking... 🤔",
        "Hmm... 💭",
    ]
    
    # Sleepy messages (when idle too long)
    SLEEPY_MESSAGES = [
        "*yawns* 😴",
        "Getting sleepy...",
        "Zzz...",
        "Wake me up?",
        "So quiet here...",
        "*snores softly*",
    ]
    
    # End of day messages
    EOD_MESSAGES = [
        "Time to wrap up, {user}! 📋",
        "Don't forget your standup!",
        "Export your logs! 📊",
        "End of day check! ✅",
        "Log your hours, {user}!",
    ]
    
    def __init__(self, user_name="friend"):
        self.user_name = user_name
        self.current_message = ""
        self.message_timer = 0
        self.message_duration = 100  # frames (~5 seconds)
        self.show_message = False
        self.last_message_time = 0
        self.message_cooldown = 120  # 2 minutes between random messages
        
    def set_user_name(self, name):
        self.user_name = name
        
    def get_time_based_greeting(self):
        hour = time.localtime().tm_hour
        if 5 <= hour < 12:
            pool = self.MORNING_GREETINGS + self.GREETINGS
        elif 12 <= hour < 17:
            pool = self.AFTERNOON_GREETINGS + self.GREETINGS
        else:
            pool = self.EVENING_GREETINGS + self.GREETINGS
        return random.choice(pool).format(user=self.user_name)
    
    def get_message(self, is_tracking, is_paused, hours_worked=0, just_started=False):
        """Get a context-appropriate message"""
        current_time = time.time()
        
        # Cooldown check
        if current_time - self.last_message_time < self.message_cooldown:
            return None
            
        # Random chance to show message (3% - very rare, non-intrusive)
        if random.random() > 0.03:
            return None
        
        self.last_message_time = current_time
        
        if just_started:
            return self.get_time_based_greeting()
        elif is_paused:
            return random.choice(self.PAUSE_MESSAGES).format(user=self.user_name)
        elif is_tracking:
            if hours_worked >= 6:
                return random.choice(self.CELEBRATION_MESSAGES).format(user=self.user_name)
            elif hours_worked >= 2 and random.random() < 0.3:
                return random.choice(self.BREAK_MESSAGES).format(user=self.user_name)
            else:
                return random.choice(self.WORKING_QUOTES).format(user=self.user_name)
        else:
            # Not tracking
            if random.random() < 0.4:
                return random.choice(self.IDLE_NUDGES).format(user=self.user_name)
            else:
                return random.choice(self.FUN_MESSAGES + self.GREETINGS).format(user=self.user_name)
    
    def force_message(self, category="greeting"):
        """Force show a message of specific category"""
        self.last_message_time = 0  # Reset cooldown
        if category == "greeting":
            return self.get_time_based_greeting()
        elif category == "working":
            return random.choice(self.WORKING_QUOTES).format(user=self.user_name)
        elif category == "break":
            return random.choice(self.BREAK_MESSAGES).format(user=self.user_name)
        elif category == "celebration":
            return random.choice(self.CELEBRATION_MESSAGES).format(user=self.user_name)
        elif category == "sleepy":
            return random.choice(self.SLEEPY_MESSAGES).format(user=self.user_name)
        elif category == "eod":
            return random.choice(self.EOD_MESSAGES).format(user=self.user_name)
        return random.choice(self.FUN_MESSAGES)
    
    def update(self, is_tracking, is_paused, hours_worked=0):
        """Update message state each frame"""
        if self.show_message:
            self.message_timer += 1
            if self.message_timer > self.message_duration:
                self.show_message = False
                self.current_message = ""
                self.message_timer = 0
        else:
            # Try to get a new message
            msg = self.get_message(is_tracking, is_paused, hours_worked)
            if msg:
                self.current_message = msg
                self.show_message = True
                self.message_timer = 0
                
    def set_message(self, msg):
        """Manually set a message to display"""
        self.current_message = msg
        self.show_message = True
        self.message_timer = 0
