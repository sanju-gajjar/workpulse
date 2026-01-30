"""
Character Module
Defines mascot themes and character drawing logic
"""

import math
import random
import cairo


class MascotTheme:
    """Elephant mascot theme"""
    
    ELEPHANT = 'elephant'  # Cartoon elephant mascot
    
    THEMES = {
        'elephant': {
            'name': 'Ellie (Elephant)',
            'icon': '🐘',
            'body_idle': (0.65, 0.65, 0.70),
            'body_working': (0.55, 0.65, 0.75),
            'body_paused': (0.75, 0.70, 0.65),
        }
    }
    
    @classmethod
    def get_theme(cls, theme_name):
        return cls.THEMES.get(theme_name, cls.THEMES['elephant'])
    
    @classmethod
    def get_all_themes(cls):
        return list(cls.THEMES.keys())


class MascotCharacter:
    """Draws a cute cartoon elephant mascot with different poses/animations"""
    
    # Animation states
    IDLE = 'idle'
    THINKING = 'thinking'
    WORKING = 'working'
    RUNNING = 'running'
    JUMPING = 'jumping'
    WAVING = 'waving'
    SLEEPING = 'sleeping'
    CELEBRATING = 'celebrating'
    ANGRY = 'angry'
    CRYING = 'crying'
    SAD = 'sad'
    EXCITED = 'excited'
    CONFUSED = 'confused'
    SHOCKED = 'shocked'
    LAUGHING = 'laughing'
    TIRED = 'tired'
    DANCING = 'dancing'
    MEDITATING = 'meditating'
    
    def __init__(self, theme='elephant'):
        self.theme = 'elephant'
        self.state = self.IDLE
        self.frame = 0
        self.blink_timer = 0
        self.is_blinking = False
        self.state_timer = 0
        self.state_duration = 100
        self.bounce_offset = 0
        self.bounce_dir = 1
        self.is_sleepy = False
        self.trunk_swing = 0
        self.ear_flap = 0
        
    def set_theme(self, theme):
        self.theme = 'elephant'
        
    def set_sleepy(self, sleepy):
        """Set sleepy mode - mascot falls asleep when idle too long"""
        if sleepy and not self.is_sleepy:
            self.is_sleepy = True
            self.state = self.SLEEPING
            self.state_timer = 0
        elif not sleepy and self.is_sleepy:
            self.is_sleepy = False
            self.state = self.IDLE
        
    def next_frame(self):
        self.frame += 1
        self.state_timer += 1
        
        # Blinking
        self.blink_timer += 1
        if self.blink_timer > 60 and not self.is_blinking:
            if random.random() < 0.05:
                self.is_blinking = True
                self.blink_timer = 0
        if self.is_blinking and self.blink_timer > 5:
            self.is_blinking = False
            self.blink_timer = 0
        
        # Bounce effect
        self.bounce_offset += 0.15 * self.bounce_dir
        if abs(self.bounce_offset) > 2:
            self.bounce_dir *= -1
        
        # Trunk swing animation
        self.trunk_swing = math.sin(self.frame * 0.1) * 15
        
        # Ear flap animation
        self.ear_flap = abs(math.sin(self.frame * 0.15)) * 5
        
        # Random state change
        if self.state_timer > self.state_duration:
            self.change_random_state()
    
    def change_random_state(self, is_tracking=False, is_paused=False):
        self.state_timer = 0
        self.state_duration = random.randint(80, 200)
        
        if self.is_sleepy:
            self.state = self.SLEEPING
            return
        
        if is_paused:
            self.state = random.choice([
                self.SLEEPING, self.THINKING, self.IDLE, 
                self.TIRED, self.MEDITATING
            ])
        elif is_tracking:
            self.state = random.choice([
                self.WORKING, self.WORKING, self.WORKING,
                self.THINKING, self.RUNNING, self.CELEBRATING,
                self.EXCITED, self.DANCING
            ])
        else:
            self.state = random.choice([
                self.IDLE, self.IDLE, self.WAVING, 
                self.THINKING, self.JUMPING, self.CONFUSED,
                self.LAUGHING
            ])
    
    def draw(self, cr, cx, cy, size, is_tracking=False, is_paused=False):
        """Draw the elephant mascot at center (cx, cy) with given size"""
        
        # Apply bounce
        if self.is_sleepy:
            cy += self.bounce_offset * 0.3
        else:
            cy += self.bounce_offset
        
        # Scale factor
        s = size / 80
        
        # Jump animation
        jump_offset = 0
        if self.state == self.JUMPING:
            jump_offset = -abs(math.sin(self.frame * 0.2)) * 15 * s
        
        cy += jump_offset
        
        # Get theme colors
        theme = MascotTheme.get_theme(self.theme)
        if is_tracking and not is_paused:
            body_color = theme['body_working']
        elif is_paused:
            body_color = theme['body_paused']
        else:
            body_color = theme['body_idle']
        
        # Draw shadow
        cr.set_source_rgba(0, 0, 0, 0.15)
        cr.save()
        cr.translate(cx, cy + 35*s)
        cr.scale(40*s, 10*s)
        cr.arc(0, 0, 1, 0, 2*math.pi)
        cr.restore()
        cr.fill()
        
        # Draw elephant
        self._draw_elephant_body(cr, cx, cy, s, body_color)
        self._draw_elephant_ears(cr, cx, cy, s, body_color)
        self._draw_elephant_trunk(cr, cx, cy, s, body_color)
        self._draw_elephant_legs(cr, cx, cy, s, body_color)
        self._draw_elephant_face(cr, cx, cy, s)
        self._draw_elephant_tail(cr, cx, cy, s, body_color)
        self._draw_state_effects(cr, cx, cy, s)
    
    def _draw_elephant_body(self, cr, cx, cy, s, color):
        """Draw elephant body"""
        cr.set_source_rgb(*color)
        
        # Main body (large oval)
        cr.save()
        cr.translate(cx, cy)
        cr.scale(1.2, 1)
        cr.arc(0, 0, 25*s, 0, 2*math.pi)
        cr.restore()
        cr.fill()
        
        # Body highlight
        cr.set_source_rgba(1, 1, 1, 0.2)
        cr.arc(cx - 10*s, cy - 12*s, 10*s, 0, 2*math.pi)
        cr.fill()
    
    def _draw_elephant_ears(self, cr, cx, cy, s, color):
        """Draw big elephant ears"""
        ear_angle = self.ear_flap * 0.01
        
        # Left ear
        cr.set_source_rgb(*[c * 0.9 for c in color])
        cr.save()
        cr.translate(cx - 20*s, cy - 8*s)
        cr.rotate(-0.3 - ear_angle)
        cr.save()
        cr.scale(1, 1.3)
        cr.arc(0, 0, 18*s, 0, 2*math.pi)
        cr.restore()
        cr.fill()
        cr.restore()
        
        # Left ear inner (pink)
        cr.set_source_rgba(0.9, 0.6, 0.7, 0.6)
        cr.save()
        cr.translate(cx - 20*s, cy - 8*s)
        cr.rotate(-0.3 - ear_angle)
        cr.save()
        cr.scale(1, 1.3)
        cr.arc(0, 0, 12*s, 0, 2*math.pi)
        cr.restore()
        cr.fill()
        cr.restore()
        
        # Right ear
        cr.set_source_rgb(*[c * 0.9 for c in color])
        cr.save()
        cr.translate(cx + 20*s, cy - 8*s)
        cr.rotate(0.3 + ear_angle)
        cr.save()
        cr.scale(1, 1.3)
        cr.arc(0, 0, 18*s, 0, 2*math.pi)
        cr.restore()
        cr.fill()
        cr.restore()
        
        # Right ear inner (pink)
        cr.set_source_rgba(0.9, 0.6, 0.7, 0.6)
        cr.save()
        cr.translate(cx + 20*s, cy - 8*s)
        cr.rotate(0.3 + ear_angle)
        cr.save()
        cr.scale(1, 1.3)
        cr.arc(0, 0, 12*s, 0, 2*math.pi)
        cr.restore()
        cr.fill()
        cr.restore()
    
    def _draw_elephant_trunk(self, cr, cx, cy, s, color):
        """Draw elephant trunk with animation"""
        trunk_angle = self.trunk_swing * 0.01
        
        if self.state == self.WAVING:
            trunk_angle = -0.5 + math.sin(self.frame * 0.3) * 0.4
        elif self.state == self.WORKING:
            trunk_angle = 0.3
        elif self.state == self.DRINKING:
            trunk_angle = 0.5
        
        cr.set_source_rgb(*color)
        cr.set_line_width(10*s)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        
        # Trunk curve
        cr.move_to(cx, cy + 8*s)
        cr.curve_to(
            cx + math.sin(trunk_angle) * 10*s, cy + 18*s,
            cx + math.sin(trunk_angle) * 15*s, cy + 28*s,
            cx + math.sin(trunk_angle) * 20*s, cy + 35*s
        )
        cr.stroke()
        
        # Trunk tip
        trunk_tip_x = cx + math.sin(trunk_angle) * 20*s
        trunk_tip_y = cy + 35*s
        cr.set_source_rgb(*[c * 0.85 for c in color])
        cr.arc(trunk_tip_x, trunk_tip_y, 5*s, 0, 2*math.pi)
        cr.fill()
        
        # Trunk wrinkles
        cr.set_source_rgba(0, 0, 0, 0.1)
        cr.set_line_width(1*s)
        for i in range(3):
            y_pos = cy + 15*s + i * 7*s
            cr.move_to(cx - 4*s, y_pos)
            cr.line_to(cx + 4*s, y_pos)
            cr.stroke()
    
    def _draw_elephant_legs(self, cr, cx, cy, s, color):
        """Draw elephant legs"""
        leg_width = 10*s
        leg_height = 20*s
        
        # Calculate leg positions for running
        left_offset = 0
        right_offset = 0
        if self.state == self.RUNNING:
            left_offset = math.sin(self.frame * 0.3) * 5*s
            right_offset = -math.sin(self.frame * 0.3) * 5*s
        
        cr.set_source_rgb(*[c * 0.85 for c in color])
        
        # Front left leg
        cr.rectangle(cx - 18*s, cy + 15*s + left_offset, leg_width, leg_height)
        cr.fill()
        
        # Front right leg
        cr.rectangle(cx + 8*s, cy + 15*s + right_offset, leg_width, leg_height)
        cr.fill()
        
        # Back left leg (behind body)
        cr.set_source_rgb(*[c * 0.75 for c in color])
        cr.rectangle(cx - 12*s, cy + 15*s - left_offset, leg_width, leg_height)
        cr.fill()
        
        # Back right leg (behind body)
        cr.rectangle(cx + 2*s, cy + 15*s - right_offset, leg_width, leg_height)
        cr.fill()
        
        # Feet (toenails)
        cr.set_source_rgba(0, 0, 0, 0.3)
        for leg_x in [cx - 18*s, cx + 8*s, cx - 12*s, cx + 2*s]:
            for toe in range(3):
                cr.arc(leg_x + 2*s + toe * 3*s, cy + 36*s, 1.5*s, 0, 2*math.pi)
                cr.fill()
    
    def _draw_elephant_face(self, cr, cx, cy, s):
        """Draw elephant eyes and expression"""
        eye_y = cy - 8*s
        
        # Eyes
        if self.is_blinking or self.state == self.SLEEPING or self.state == self.TIRED:
            # Closed eyes
            cr.set_source_rgb(0.2, 0.2, 0.2)
            cr.set_line_width(2*s)
            cr.move_to(cx - 15*s, eye_y)
            cr.line_to(cx - 10*s, eye_y)
            cr.move_to(cx + 10*s, eye_y)
            cr.line_to(cx + 15*s, eye_y)
            cr.stroke()
        elif self.state == self.SHOCKED or self.state == self.EXCITED:
            # Wide eyes
            cr.set_source_rgb(1, 1, 1)
            cr.arc(cx - 12*s, eye_y, 5*s, 0, 2*math.pi)
            cr.arc(cx + 12*s, eye_y, 5*s, 0, 2*math.pi)
            cr.fill()
            cr.set_source_rgb(0.1, 0.1, 0.1)
            cr.arc(cx - 12*s, eye_y, 3*s, 0, 2*math.pi)
            cr.arc(cx + 12*s, eye_y, 3*s, 0, 2*math.pi)
            cr.fill()
        elif self.state == self.HAPPY or self.state == self.CELEBRATING:
            # Happy squinted eyes
            cr.set_source_rgb(0.2, 0.2, 0.2)
            cr.set_line_width(2*s)
            cr.arc(cx - 12*s, eye_y, 4*s, 0.3, math.pi - 0.3)
            cr.stroke()
            cr.arc(cx + 12*s, eye_y, 4*s, 0.3, math.pi - 0.3)
            cr.stroke()
        else:
            # Normal eyes
            cr.set_source_rgb(1, 1, 1)
            cr.arc(cx - 12*s, eye_y, 4*s, 0, 2*math.pi)
            cr.arc(cx + 12*s, eye_y, 4*s, 0, 2*math.pi)
            cr.fill()
            cr.set_source_rgb(0.1, 0.1, 0.1)
            cr.arc(cx - 12*s, eye_y, 2*s, 0, 2*math.pi)
            cr.arc(cx + 12*s, eye_y, 2*s, 0, 2*math.pi)
            cr.fill()
            # Eye shine
            cr.set_source_rgba(1, 1, 1, 0.8)
            cr.arc(cx - 11*s, eye_y - 1*s, 1*s, 0, 2*math.pi)
            cr.arc(cx + 13*s, eye_y - 1*s, 1*s, 0, 2*math.pi)
            cr.fill()
        
        # Tusks (small white)
        if self.state != self.SLEEPING:
            cr.set_source_rgb(1, 1, 0.95)
            # Left tusk
            cr.move_to(cx - 8*s, cy + 5*s)
            cr.curve_to(cx - 12*s, cy + 8*s, cx - 15*s, cy + 10*s, cx - 16*s, cy + 15*s)
            cr.line_to(cx - 14*s, cy + 15*s)
            cr.curve_to(cx - 13*s, cy + 10*s, cx - 10*s, cy + 8*s, cx - 7*s, cy + 5*s)
            cr.close_path()
            cr.fill()
            # Right tusk
            cr.move_to(cx + 8*s, cy + 5*s)
            cr.curve_to(cx + 12*s, cy + 8*s, cx + 15*s, cy + 10*s, cx + 16*s, cy + 15*s)
            cr.line_to(cx + 14*s, cy + 15*s)
            cr.curve_to(cx + 13*s, cy + 10*s, cx + 10*s, cy + 8*s, cx + 7*s, cy + 5*s)
            cr.close_path()
            cr.fill()
    
    def _draw_elephant_tail(self, cr, cx, cy, s, color):
        """Draw elephant tail"""
        tail_swing = math.sin(self.frame * 0.12) * 8*s
        
        cr.set_source_rgb(*[c * 0.85 for c in color])
        cr.set_line_width(3*s)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        
        # Tail curve
        cr.move_to(cx + 30*s, cy + 5*s)
        cr.curve_to(
            cx + 35*s + tail_swing, cy + 10*s,
            cx + 38*s + tail_swing, cy + 18*s,
            cx + 35*s + tail_swing, cy + 25*s
        )
        cr.stroke()
        
        # Tail tuft
        cr.set_source_rgb(*[c * 0.7 for c in color])
        tail_end_x = cx + 35*s + tail_swing
        tail_end_y = cy + 25*s
        for i in range(5):
            angle = (i - 2) * 0.2
            cr.move_to(tail_end_x, tail_end_y)
            cr.line_to(
                tail_end_x + math.sin(angle) * 4*s,
                tail_end_y + 6*s + abs(math.cos(angle)) * 2*s
            )
            cr.stroke()
    
    def _draw_state_effects(self, cr, cx, cy, s):
        """Draw extra effects based on state"""
        
        if self.state == self.THINKING or self.state == self.CONFUSED:
            # Thought bubble
            cr.set_source_rgba(0.3, 0.3, 0.3, 0.7)
            cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            cr.set_font_size(16*s)
            cr.move_to(cx + 25*s, cy - 30*s)
            cr.show_text("?")
        
        elif self.state == self.SLEEPING or self.state == self.TIRED:
            # Zzz
            cr.set_source_rgba(0.3, 0.3, 0.3, 0.6)
            cr.select_font_face("Sans", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_BOLD)
            offset = math.sin(self.frame * 0.1) * 3
            for i, (size, x_off, y_off) in enumerate([(10*s, 20*s, -25*s), (12*s, 28*s, -32*s), (14*s, 36*s, -40*s)]):
                cr.set_font_size(size)
                cr.move_to(cx + x_off, cy + y_off + offset)
                cr.show_text("z" if i < 2 else "Z")
        
        elif self.state == self.WORKING:
            # Computer/laptop
            cr.set_source_rgba(0.3, 0.3, 0.4, 0.8)
            cr.rectangle(cx - 15*s, cy + 20*s, 30*s, 5*s)
            cr.fill()
        
        elif self.state == self.CELEBRATING or self.state == self.EXCITED:
            # Sparkles
            cr.set_source_rgba(1, 0.85, 0.2, 0.8)
            for i in range(4):
                angle = self.frame * 0.1 + i * 1.57
                dist = 40*s
                px = cx + math.cos(angle) * dist
                py = cy - 20*s + math.sin(angle) * dist * 0.4
                cr.arc(px, py, 2*s, 0, 2*math.pi)
                cr.fill()
        
        elif self.state == self.DANCING:
            # Music notes
            cr.set_source_rgba(0.2, 0.2, 0.8, 0.7)
            cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            cr.set_font_size(14*s)
            note_offset = math.sin(self.frame * 0.2) * 5*s
            cr.move_to(cx - 30*s, cy - 30*s + note_offset)
            cr.show_text("♪")
            cr.move_to(cx + 25*s, cy - 25*s - note_offset)
            cr.show_text("♫")
        
        elif self.state == self.SHOCKED:
            # Exclamation
            cr.set_source_rgba(0.9, 0.1, 0.1, 0.9)
            cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            cr.set_font_size(18*s)
            cr.move_to(cx - 30*s, cy - 25*s)
            cr.show_text("!")


# Keep old THEME_CONFIGS structure for backward compatibility (empty now)
THEME_CONFIGS = {
    'blob': {
        'body_shape': 'ellipse',
        'body_size': (28, 25),  # width, height multipliers
        'body_highlight': {'x': -8, 'y': -10, 'size': 8},
        'ears': None,
        'tail': None,
        'special_accessories': [],
        'face_offset': 0,
    },
    'robot': {
        'body_shape': 'rounded_rect',
        'body_size': (25, 22),
        'body_highlight': {'x': -6, 'y': -8, 'size': 6},
        'ears': None,
        'tail': None,
        'special_accessories': ['antenna', 'buttons'],
        'face_offset': 0,
    },
    'cat': {
        'body_shape': 'ellipse',
        'body_size': (28, 25),
        'body_highlight': {'x': -8, 'y': -10, 'size': 8},
        'ears': {'type': 'pointed', 'size': 8},
        'tail': {'type': 'curved', 'length': 20},
        'special_accessories': ['whiskers'],
        'face_offset': 0,
    },
    'astronaut': {
        'body_shape': 'ellipse',
        'body_size': (28, 25),
        'body_highlight': {'x': -8, 'y': -10, 'size': 8},
        'ears': None,
        'tail': None,
        'special_accessories': ['helmet', 'jetpack'],
        'face_offset': 0,
    },
    'dragon': {
        'body_shape': 'ellipse',
        'body_size': (30, 26),
        'body_highlight': {'x': -9, 'y': -11, 'size': 9},
        'ears': {'type': 'pointed', 'size': 10},
        'tail': {'type': 'spiked', 'length': 25},
        'special_accessories': ['wings', 'horns'],
        'face_offset': 0,
    },
    'alien': {
        'body_shape': 'ellipse',
        'body_size': (26, 24),
        'body_highlight': {'x': -7, 'y': -9, 'size': 7},
        'ears': None,
        'tail': None,
        'special_accessories': ['antenna'],
        'face_offset': 0,
    },
    'ninja': {
        'body_shape': 'ellipse',
        'body_size': (27, 24),
        'body_highlight': {'x': -7, 'y': -9, 'size': 7},
        'ears': None,
        'tail': None,
        'special_accessories': ['mask', 'scarf'],
        'face_offset': 0,
    },
    'wizard': {
        'body_shape': 'ellipse',
        'body_size': (28, 25),
        'body_highlight': {'x': -8, 'y': -10, 'size': 8},
        'ears': {'type': 'pointed', 'size': 9},
        'tail': None,
        'special_accessories': ['hat', 'staff'],
        'face_offset': 0,
    },
    'penguin': {
        'body_shape': 'ellipse',
        'body_size': (24, 28),
        'body_highlight': {'x': -6, 'y': -12, 'size': 6},
        'ears': None,
        'tail': None,
        'special_accessories': ['flippers'],
        'face_offset': 0,
    },
    'bear': {
        'body_shape': 'ellipse',
        'body_size': (30, 26),
        'body_highlight': {'x': -9, 'y': -11, 'size': 9},
        'ears': {'type': 'round', 'size': 8},
        'tail': None,
        'special_accessories': [],
        'face_offset': 0,
    },
    'ghost': {
        'body_shape': 'ghost',
        'body_size': (28, 25),
        'body_highlight': None,
        'ears': None,
        'tail': None,
        'special_accessories': [],
        'face_offset': 0,
    },
    'pirate': {
        'body_shape': 'ellipse',
        'body_size': (28, 25),
        'body_highlight': {'x': -8, 'y': -10, 'size': 8},
        'ears': None,
        'tail': None,
        'special_accessories': ['hat', 'patch'],
        'face_offset': 0,
    },
    'ironman': {
        'body_shape': 'armored',
        'body_size': (28, 25),
        'body_highlight': None,
        'ears': None,
        'tail': None,
        'special_accessories': ['armor_plates', 'repulsors', 'thrusters'],
        'face_offset': 0,
    },
}


class MascotThemeBase:
    """Base class for mascot themes with shared drawing methods"""
    
    def __init__(self, config):
        self.config = config
    
    def draw_body(self, cr, cx, cy, s, color):
        """Draw the main body based on config"""
        shape = self.config.get('body_shape', 'ellipse')
        w, h = self.config['body_size']
        w *= s
        h *= s
        
        if shape == 'ellipse':
            cr.save()
            cr.translate(cx, cy)
            cr.scale(1, h/(w*math.pi/2))  # approximate ellipse
            cr.arc(0, 0, w/2, 0, 2*math.pi)
            cr.restore()
        elif shape == 'rounded_rect':
            self._draw_rounded_rect(cr, cx - w/2, cy - h/2, w, h, 5*s)
        elif shape == 'ghost':
            self._draw_ghost_shape(cr, cx, cy, w, h)
        elif shape == 'armored':
            self._draw_armored_body(cr, cx, cy, s, color)
        else:
            # default ellipse
            cr.arc(cx, cy, w/2, 0, 2*math.pi)
        
        cr.set_source_rgba(*color)
        cr.fill()
        
        # Highlight
        highlight = self.config.get('body_highlight')
        if highlight:
            cr.set_source_rgba(1, 1, 1, 0.3)
            cr.arc(cx + highlight['x']*s, cy + highlight['y']*s, highlight['size']*s, 0, 2*math.pi)
            cr.fill()
    
    def draw_face(self, cr, cx, cy, s):
        """Base face drawing - can be overridden"""
        # Eyes
        eye_y = cy - 5*s
        cr.set_source_rgba(0, 0, 0, 1)
        cr.arc(cx - 10*s, eye_y, 2*s, 0, 2*math.pi)
        cr.fill()
        cr.arc(cx + 10*s, eye_y, 2*s, 0, 2*math.pi)
        cr.fill()
        
        # Mouth
        cr.arc(cx, cy + 5*s, 3*s, 0, math.pi)
        cr.stroke()
    
    def draw_ears(self, cr, cx, cy, s):
        """Draw ears if configured"""
        ears = self.config.get('ears')
        if ears:
            if ears['type'] == 'pointed':
                # Cat-like ears
                cr.move_to(cx - 15*s, cy - 20*s)
                cr.line_to(cx - 10*s, cy - 30*s)
                cr.line_to(cx - 5*s, cy - 20*s)
                cr.close_path()
                cr.move_to(cx + 5*s, cy - 20*s)
                cr.line_to(cx + 10*s, cy - 30*s)
                cr.line_to(cx + 15*s, cy - 20*s)
                cr.close_path()
                cr.fill()
            elif ears['type'] == 'round':
                cr.arc(cx - 12*s, cy - 25*s, 6*s, 0, 2*math.pi)
                cr.fill()
                cr.arc(cx + 12*s, cy - 25*s, 6*s, 0, 2*math.pi)
                cr.fill()
    
    def draw_tail(self, cr, cx, cy, s):
        """Draw tail if configured"""
        tail = self.config.get('tail')
        if tail:
            if tail['type'] == 'curved':
                cr.move_to(cx, cy + 15*s)
                cr.curve_to(cx + 10*s, cy + 20*s, cx + 15*s, cy + 25*s, cx + tail['length']*s, cy + 15*s)
                cr.stroke()
            elif tail['type'] == 'spiked':
                # Dragon tail
                cr.move_to(cx, cy + 15*s)
                for i in range(5):
                    cr.line_to(cx + (i+1)*5*s, cy + 15*s + (i%2)*5*s)
                cr.stroke()
    
    def draw_special_accessories(self, cr, cx, cy, s, color):
        """Draw theme-specific accessories"""
        accessories = self.config.get('special_accessories', [])
        for acc in accessories:
            if acc == 'antenna':
                cr.set_source_rgba(0.5, 0.5, 0.5, 1)
                cr.move_to(cx, cy - 25*s)
                cr.line_to(cx, cy - 35*s)
                cr.stroke()
                cr.arc(cx, cy - 37*s, 2*s, 0, 2*math.pi)
                cr.fill()
            elif acc == 'buttons':
                cr.set_source_rgba(0.8, 0.8, 0.8, 1)
                cr.arc(cx - 8*s, cy, 3*s, 0, 2*math.pi)
                cr.fill()
                cr.arc(cx + 8*s, cy, 3*s, 0, 2*math.pi)
                cr.fill()
            elif acc == 'whiskers':
                cr.set_source_rgba(0, 0, 0, 0.8)
                cr.move_to(cx - 20*s, cy - 2*s)
                cr.line_to(cx - 30*s, cy - 2*s)
                cr.move_to(cx - 20*s, cy + 2*s)
                cr.line_to(cx - 30*s, cy + 2*s)
                cr.move_to(cx + 20*s, cy - 2*s)
                cr.line_to(cx + 30*s, cy - 2*s)
                cr.move_to(cx + 20*s, cy + 2*s)
                cr.line_to(cx + 30*s, cy + 2*s)
                cr.stroke()
            # Add more as needed
    
    def _draw_rounded_rect(self, cr, x, y, w, h, r):
        cr.move_to(x + r, y)
        cr.line_to(x + w - r, y)
        cr.curve_to(x + w, y, x + w, y + r, x + w, y + r)
        cr.line_to(x + w, y + h - r)
        cr.curve_to(x + w, y + h, x + w - r, y + h, x + w - r, y + h)
        cr.line_to(x + r, y + h)
        cr.curve_to(x, y + h, x, y + h - r, x, y + h - r)
        cr.line_to(x, y + r)
        cr.curve_to(x, y, x + r, y, x + r, y)
        cr.close_path()
    
    def _draw_ghost_shape(self, cr, cx, cy, w, h):
        # Ghost shape with wavy bottom
        cr.move_to(cx - w/2, cy - h/2)
        cr.line_to(cx + w/2, cy - h/2)
        cr.line_to(cx + w/2, cy + h/4)
        cr.curve_to(cx + w/3, cy + h/2, cx, cy + h/3, cx, cy + h/2)
        cr.curve_to(cx - w/3, cy + h/3, cx - w/2, cy + h/4, cx - w/2, cy + h/4)
        cr.close_path()
    
    def _draw_armored_body(self, cr, cx, cy, s, color):
        # Iron Man style armored body
        # Chest plate
        cr.set_source_rgba(0.6, 0.09, 0.09, 1)
        self._draw_rounded_rect(cr, cx - 22*s, cy - 8*s, 44*s, 16*s, 3*s)
        cr.fill()
        # Arc reactor
        cr.set_source_rgba(0.3, 0.8, 1.0, 1)
        cr.arc(cx, cy, 4*s, 0, 2*math.pi)
        cr.fill()


class BlobTheme(MascotThemeBase):
    pass  # Uses base implementation


class RobotTheme(MascotThemeBase):
    def draw_special_accessories(self, cr, cx, cy, s, color):
        super().draw_special_accessories(cr, cx, cy, s, color)
        # Additional robot details if needed


class CatTheme(MascotThemeBase):
    pass


class AstronautTheme(MascotThemeBase):
    def draw_special_accessories(self, cr, cx, cy, s, color):
        # Helmet
        cr.set_source_rgba(0.9, 0.9, 0.9, 1)
        cr.arc(cx, cy - 10*s, 18*s, math.pi, 2*math.pi)
        cr.fill()
        # Visor
        cr.set_source_rgba(0.1, 0.1, 0.1, 0.8)
        cr.arc(cx, cy - 10*s, 15*s, math.pi, 2*math.pi)
        cr.fill()


class DragonTheme(MascotThemeBase):
    def draw_special_accessories(self, cr, cx, cy, s, color):
        # Wings
        cr.set_source_rgba(*color)
        cr.move_to(cx - 20*s, cy - 5*s)
        cr.curve_to(cx - 30*s, cy - 15*s, cx - 25*s, cy + 5*s, cx - 15*s, cy)
        cr.close_path()
        cr.fill()
        cr.move_to(cx + 20*s, cy - 5*s)
        cr.curve_to(cx + 30*s, cy - 15*s, cx + 25*s, cy + 5*s, cx + 15*s, cy)
        cr.close_path()
        cr.fill()
        # Horns
        cr.set_source_rgba(0.8, 0.2, 0.3, 1)
        cr.move_to(cx - 8*s, cy - 25*s)
        cr.line_to(cx - 5*s, cy - 35*s)
        cr.line_to(cx - 3*s, cy - 25*s)
        cr.close_path()
        cr.fill()
        cr.move_to(cx + 3*s, cy - 25*s)
        cr.line_to(cx + 5*s, cy - 35*s)
        cr.line_to(cx + 8*s, cy - 25*s)
        cr.close_path()
        cr.fill()


class AlienTheme(MascotThemeBase):
    def draw_face(self, cr, cx, cy, s):
        # Alien eyes
        cr.set_source_rgba(0.3, 1.0, 0.5, 1)
        cr.arc(cx - 10*s, cy - 5*s, 3*s, 0, 2*math.pi)
        cr.fill()
        cr.arc(cx + 10*s, cy - 5*s, 3*s, 0, 2*math.pi)
        cr.fill()
        # Mouth
        cr.set_source_rgba(0, 0, 0, 1)
        cr.arc(cx, cy + 5*s, 2*s, 0, math.pi)
        cr.stroke()


class NinjaTheme(MascotThemeBase):
    def draw_special_accessories(self, cr, cx, cy, s, color):
        # Mask
        cr.set_source_rgba(0.1, 0.1, 0.1, 1)
        cr.arc(cx, cy - 5*s, 12*s, math.pi, 2*math.pi)
        cr.fill()


class WizardTheme(MascotThemeBase):
    def draw_special_accessories(self, cr, cx, cy, s, color):
        # Hat
        cr.set_source_rgba(0.4, 0.2, 0.7, 1)
        cr.move_to(cx - 15*s, cy - 20*s)
        cr.line_to(cx, cy - 40*s)
        cr.line_to(cx + 15*s, cy - 20*s)
        cr.close_path()
        cr.fill()
        # Staff
        cr.set_source_rgba(0.6, 0.4, 0.2, 1)
        cr.move_to(cx + 20*s, cy - 10*s)
        cr.line_to(cx + 20*s, cy + 20*s)
        cr.stroke()


class PenguinTheme(MascotThemeBase):
    def draw_special_accessories(self, cr, cx, cy, s, color):
        # Flippers
        cr.set_source_rgba(0.1, 0.1, 0.15, 1)
        cr.arc(cx - 25*s, cy, 8*s, math.pi/2, 3*math.pi/2)
        cr.fill()
        cr.arc(cx + 25*s, cy, 8*s, 3*math.pi/2, math.pi/2)
        cr.fill()


class BearTheme(MascotThemeBase):
    pass


class GhostTheme(MascotThemeBase):
    def draw_body(self, cr, cx, cy, s, color):
        cr.set_source_rgba(0.9, 0.9, 1.0, 0.8)
        w, h = self.config['body_size']
        self._draw_ghost_shape(cr, cx, cy, w*s, h*s)
        cr.fill()


class PirateTheme(MascotThemeBase):
    def draw_special_accessories(self, cr, cx, cy, s, color):
        # Hat
        cr.set_source_rgba(0.1, 0.1, 0.1, 1)
        cr.arc(cx, cy - 25*s, 12*s, math.pi, 2*math.pi)
        cr.fill()
        cr.move_to(cx - 12*s, cy - 25*s)
        cr.line_to(cx - 12*s, cy - 15*s)
        cr.line_to(cx + 12*s, cy - 15*s)
        cr.line_to(cx + 12*s, cy - 25*s)
        cr.fill()
        # Eye patch
        cr.set_source_rgba(0.05, 0.05, 0.05, 1)
        cr.arc(cx - 10*s, cy - 5*s, 4*s, 0, 2*math.pi)
        cr.fill()


class IronManTheme(MascotThemeBase):
    def draw_body(self, cr, cx, cy, s, color):
        self._draw_armored_body(cr, cx, cy, s, color)
    
    def draw_special_accessories(self, cr, cx, cy, s, color):
        # Repulsors
        cr.set_source_rgba(0.3, 0.8, 1.0, 1)
        cr.arc(cx - 15*s, cy, 3*s, 0, 2*math.pi)
        cr.fill()
        cr.arc(cx + 15*s, cy, 3*s, 0, 2*math.pi)
        cr.fill()
        # Thrusters
        cr.set_source_rgba(1.0, 0.5, 0.0, 1)
        cr.arc(cx - 10*s, cy + 15*s, 4*s, 0, 2*math.pi)
        cr.fill()
        cr.arc(cx + 10*s, cy + 15*s, 4*s, 0, 2*math.pi)
        cr.fill()


class MascotCharacter:
    """Draws a cute cartoon character with different poses/animations"""
    
    # Animation states
    IDLE = 'idle'
    THINKING = 'thinking'
    WORKING = 'working'
    RUNNING = 'running'
    JUMPING = 'jumping'
    WAVING = 'waving'
    SLEEPING = 'sleeping'
    CELEBRATING = 'celebrating'
    ANGRY = 'angry'
    CRYING = 'crying'
    SAD = 'sad'
    EXCITED = 'excited'
    CONFUSED = 'confused'
    SHOCKED = 'shocked'
    LAUGHING = 'laughing'
    TIRED = 'tired'
    DANCING = 'dancing'
    MEDITATING = 'meditating'
    FLYING = 'flying'
    LANDING = 'landing'
    CHARGING = 'charging'
    FIRING = 'firing'
    
    def __init__(self, theme='blob'):
        self.theme = theme
        self.theme_instance = self._create_theme_instance(theme)
        self.state = self.IDLE
        self.frame = 0
        self.blink_timer = 0
        self.is_blinking = False
        self.state_timer = 0
        self.state_duration = 100  # Frames before state change
        self.bounce_offset = 0
        self.bounce_dir = 1
        self.is_sleepy = False  # Sleepy mode when idle too long
        self.mask_open = False  # Iron Man mask state
        self.mask_animation = 0  # Mask animation progress (0-10)
        self.repulsor_charge = 0  # Repulsor charge level
        self.is_hovering = False  # Iron Man hovering state
        
    def _create_theme_instance(self, theme):
        config = THEME_CONFIGS.get(theme, THEME_CONFIGS['blob'])
        theme_classes = {
            'blob': BlobTheme,
            'robot': RobotTheme,
            'cat': CatTheme,
            'astronaut': AstronautTheme,
            'dragon': DragonTheme,
            'alien': AlienTheme,
            'ninja': NinjaTheme,
            'wizard': WizardTheme,
            'penguin': PenguinTheme,
            'bear': BearTheme,
            'ghost': GhostTheme,
            'pirate': PirateTheme,
            'ironman': IronManTheme,
        }
        cls = theme_classes.get(theme, BlobTheme)
        return cls(config)
        
    def set_theme(self, theme):
        self.theme = theme
        self.theme_instance = self._create_theme_instance(theme)
        
    def set_sleepy(self, sleepy):
        """Set sleepy mode - mascot falls asleep when idle too long"""
        if sleepy and not self.is_sleepy:
            self.is_sleepy = True
            self.state = self.SLEEPING
            self.state_timer = 0
        elif not sleepy and self.is_sleepy:
            self.is_sleepy = False
            self.state = self.IDLE
        
    def next_frame(self):
        self.frame += 1
        self.state_timer += 1
        
        # Blinking
        self.blink_timer += 1
        if self.blink_timer > 60 and not self.is_blinking:
            if random.random() < 0.05:
                self.is_blinking = True
                self.blink_timer = 0
        if self.is_blinking and self.blink_timer > 5:
            self.is_blinking = False
            self.blink_timer = 0
        
        # Bounce effect
        self.bounce_offset += 0.15 * self.bounce_dir
        if abs(self.bounce_offset) > 2:
            self.bounce_dir *= -1
        
        # Random state change
        if self.state_timer > self.state_duration:
            self.change_random_state()
    
    def change_random_state(self, is_tracking=False, is_paused=False):
        self.state_timer = 0
        self.state_duration = random.randint(80, 200)
        
        # If sleepy, stay sleeping
        if self.is_sleepy:
            self.state = self.SLEEPING
            return
        
        if is_paused:
            self.state = random.choice([
                self.SLEEPING, self.THINKING, self.IDLE, 
                self.TIRED, self.MEDITATING
            ])
        elif is_tracking:
            # When working, bias toward working animations
            self.state = random.choice([
                self.WORKING, self.WORKING, self.WORKING,
                self.THINKING, self.RUNNING, self.CELEBRATING,
                self.EXCITED, self.DANCING
            ])
        else:
            self.state = random.choice([
                self.IDLE, self.IDLE, self.WAVING, 
                self.THINKING, self.JUMPING, self.CONFUSED,
                self.LAUGHING
            ])
    
    def draw(self, cr, cx, cy, size, is_tracking=False, is_paused=False):
        """Draw the mascot at center (cx, cy) with given size"""
        
        # Apply bounce (less if sleepy)
        if self.is_sleepy:
            cy += self.bounce_offset * 0.3
        else:
            cy += self.bounce_offset
        
        # Scale factor
        s = size / 80  # Base design is 80px
        
        # Jump animation
        jump_offset = 0
        if self.state == self.JUMPING:
            jump_offset = -abs(math.sin(self.frame * 0.2)) * 15 * s
        
        cy += jump_offset
        
        # Get theme colors
        theme = MascotTheme.get_theme(self.theme)
        if is_tracking and not is_paused:
            body_color = theme['body_working']
        elif is_paused:
            body_color = theme['body_paused']
        else:
            body_color = theme['body_idle']
        
        # Draw shadow
        cr.set_source_rgba(0, 0, 0, 0.15)
        self._draw_ellipse(cr, cx - 20*s, cy + 35*s, 40*s, 10*s)
        cr.fill()
        
        # Draw body based on theme
        self.theme_instance.draw_body(cr, cx, cy, s, body_color)
        
        # Draw ears, tail
        self.theme_instance.draw_ears(cr, cx, cy, s)
        self.theme_instance.draw_tail(cr, cx, cy, s)
        
        # Draw face
        self.theme_instance.draw_face(cr, cx, cy, s)
        
        # Draw special accessories
        self.theme_instance.draw_special_accessories(cr, cx, cy, s, body_color)
        
        # Draw arms and legs BEFORE face for astronaut (so they're behind)
        if self.theme == 'astronaut':
            self._draw_astronaut_arms(cr, cx, cy, s)
            self._draw_astronaut_legs(cr, cx, cy, s)
        elif self.theme == 'ironman':
            self._draw_ironman_arms(cr, cx, cy, s)
            self._draw_ironman_legs(cr, cx, cy, s)
        
        # Draw face
        self.theme_instance.draw_face(cr, cx, cy, s)
        
        # Draw arms based on state (skip astronaut and ironman, already drawn)
        if self.theme not in ['astronaut', 'ironman']:
            self._draw_arms(cr, cx, cy, s, body_color)
        
        # Draw legs (skip astronaut and ironman, already drawn)
        if self.theme not in ['astronaut', 'ironman']:
            self._draw_legs(cr, cx, cy, s, body_color)
        
        # Draw jetpack flames AFTER legs (so they're visible)
        if self.theme == 'astronaut':
            self._draw_astronaut_jetpack_flames(cr, cx, cy, s)
        elif self.theme == 'ironman':
            self._draw_ironman_effects(cr, cx, cy, s)
        
        # Draw state-specific elements
        self._draw_state_effects(cr, cx, cy, s)
        
        # Draw theme-specific accessories
        self._draw_theme_accessories(cr, cx, cy, s)
    


    def _draw_astronaut_body(self, cr, cx, cy, s, color):
        """Draw astronaut-style body with detailed spacesuit"""
        # === SPACESUIT TORSO (segmented armor plating) ===
        # Upper chest plate
        cr.set_source_rgb(0.88, 0.90, 0.92)
        points = [
            (cx - 22*s, cy - 10*s),
            (cx - 18*s, cy - 22*s),
            (cx + 18*s, cy - 22*s),
            (cx + 22*s, cy - 10*s),
            (cx + 20*s, cy + 5*s),
            (cx - 20*s, cy + 5*s)
        ]
        cr.move_to(*points[0])
        for point in points[1:]:
            cr.line_to(*point)
        cr.close_path()
        cr.fill()
        
        # Lower torso segment (darker)
        cr.set_source_rgb(0.78, 0.82, 0.85)
        points_lower = [
            (cx - 20*s, cy + 5*s),
            (cx + 20*s, cy + 5*s),
            (cx + 18*s, cy + 20*s),
            (cx - 18*s, cy + 20*s)
        ]
        cr.move_to(*points_lower[0])
        for point in points_lower[1:]:
            cr.line_to(*point)
        cr.close_path()
        cr.fill()
        
        # Suit segments/panel lines
        cr.set_source_rgba(0.3, 0.35, 0.4, 0.4)
        cr.set_line_width(1.5*s)
        cr.move_to(cx - 18*s, cy - 5*s)
        cr.line_to(cx + 18*s, cy - 5*s)
        cr.stroke()
        cr.move_to(cx, cy - 20*s)
        cr.line_to(cx, cy + 18*s)
        cr.stroke()
        
        # === CHEST CONTROL PANEL ===
        cr.set_source_rgb(0.25, 0.28, 0.32)
        self._draw_rounded_rect_shape(cr, cx - 12*s, cy - 2*s, 24*s, 12*s, 2*s)
        cr.fill()
        
        # Control panel details (buttons and indicators)
        # Status lights
        for i, color_led in enumerate([(1, 0.2, 0.2), (0.2, 1, 0.3), (0.3, 0.5, 1)]):
            if self.frame % (30 + i*10) < 15:
                cr.set_source_rgb(*color_led)
            else:
                cr.set_source_rgba(*color_led, 0.3)
            cr.arc(cx - 8*s + i*8*s, cy + 2*s, 1.5*s, 0, 2*math.pi)
            cr.fill()
        
        # Digital display
        cr.set_source_rgb(0.1, 0.8, 0.9)
        cr.rectangle(cx - 9*s, cy + 6*s, 18*s, 3*s)
        cr.fill()
        
        # === BACKPACK LIFE SUPPORT ===
        # Main backpack housing
        cr.set_source_rgb(0.65, 0.68, 0.72)
        self._draw_rounded_rect_shape(cr, cx - 38*s, cy - 15*s, 15*s, 35*s, 3*s)
        cr.fill()
        
        # Oxygen tanks (dual cylinders)
        cr.set_source_rgb(0.85, 0.88, 0.90)
        # Left tank
        cr.rectangle(cx - 36*s, cy - 12*s, 5*s, 30*s)
        cr.fill()
        # Right tank
        cr.rectangle(cx - 29*s, cy - 12*s, 5*s, 30*s)
        cr.fill()
        
        # Tank pressure gauges
        cr.set_source_rgb(0.2, 0.2, 0.25)
        cr.arc(cx - 33.5*s, cy - 2*s, 3*s, 0, 2*math.pi)
        cr.arc(cx - 26.5*s, cy - 2*s, 3*s, 0, 2*math.pi)
        cr.stroke()
        
        # Gauge needles (animated)
        needle_angle = math.sin(self.frame * 0.05) * 0.3 + 0.5
        cr.set_source_rgb(1, 0.3, 0.3)
        cr.set_line_width(1*s)
        cr.move_to(cx - 33.5*s, cy - 2*s)
        cr.line_to(cx - 33.5*s + math.cos(needle_angle) * 2*s, 
                   cy - 2*s + math.sin(needle_angle) * 2*s)
        cr.stroke()
        cr.move_to(cx - 26.5*s, cy - 2*s)
        cr.line_to(cx - 26.5*s + math.cos(needle_angle + 0.2) * 2*s,
                   cy - 2*s + math.sin(needle_angle + 0.2) * 2*s)
        cr.stroke()
        
        # Life support tubes
        cr.set_source_rgb(0.3, 0.35, 0.4)
        cr.set_line_width(2*s)
        # From backpack to helmet
        cr.move_to(cx - 25*s, cy - 10*s)
        cr.curve_to(cx - 20*s, cy - 15*s, cx - 15*s, cy - 20*s, cx - 10*s, cy - 22*s)
        cr.stroke()
        
        # === HELMET (futuristic angular design) ===
        # Helmet main structure (angular, not round)
        cr.set_source_rgb(0.92, 0.94, 0.96)
        helmet_points = [
            (cx - 24*s, cy - 8*s),
            (cx - 20*s, cy - 28*s),
            (cx - 10*s, cy - 35*s),
            (cx + 10*s, cy - 35*s),
            (cx + 20*s, cy - 28*s),
            (cx + 24*s, cy - 8*s),
            (cx + 18*s, cy - 5*s),
            (cx - 18*s, cy - 5*s)
        ]
        cr.move_to(*helmet_points[0])
        for point in helmet_points[1:]:
            cr.line_to(*point)
        cr.close_path()
        cr.fill()
        
        # Helmet visor (angular glass with gradient effect)
        cr.set_source_rgba(0.15, 0.25, 0.45, 0.85)
        visor_points = [
            (cx - 18*s, cy - 10*s),
            (cx - 15*s, cy - 25*s),
            (cx + 15*s, cy - 25*s),
            (cx + 18*s, cy - 10*s),
            (cx + 12*s, cy - 8*s),
            (cx - 12*s, cy - 8*s)
        ]
        cr.move_to(*visor_points[0])
        for point in visor_points[1:]:
            cr.line_to(*point)
        cr.close_path()
        cr.fill()
        
        # Visor highlights (reflections)
        cr.set_source_rgba(0.6, 0.8, 1, 0.5)
        visor_highlight = [
            (cx - 12*s, cy - 12*s),
            (cx - 10*s, cy - 22*s),
            (cx + 2*s, cy - 24*s),
            (cx + 4*s, cy - 14*s)
        ]
        cr.move_to(*visor_highlight[0])
        for point in visor_highlight[1:]:
            cr.line_to(*point)
        cr.close_path()
        cr.fill()
        
        # Secondary reflection
        cr.set_source_rgba(1, 1, 1, 0.3)
        cr.arc(cx - 8*s, cy - 20*s, 4*s, 0, 2*math.pi)
        cr.fill()
        
        # Helmet lights (external)
        if self.frame % 50 < 25:
            cr.set_source_rgb(1, 1, 0.8)
        else:
            cr.set_source_rgb(0.8, 0.8, 0.6)
        cr.arc(cx - 20*s, cy - 15*s, 2*s, 0, 2*math.pi)
        cr.arc(cx + 20*s, cy - 15*s, 2*s, 0, 2*math.pi)
        cr.fill()
        
        # Helmet seal ring
        cr.set_source_rgb(0.5, 0.52, 0.55)
        cr.set_line_width(3*s)
        cr.move_to(cx - 18*s, cy - 5*s)
        cr.line_to(cx - 22*s, cy - 2*s)
        cr.line_to(cx + 22*s, cy - 2*s)
        cr.line_to(cx + 18*s, cy - 5*s)
        cr.stroke()
        
        # Helmet vent details
        cr.set_source_rgba(0.2, 0.2, 0.25, 0.6)
        cr.set_line_width(1*s)
        for i in range(4):
            y_vent = cy - 30*s + i * 2*s
            cr.move_to(cx - 8*s, y_vent)
            cr.line_to(cx + 8*s, y_vent)
            cr.stroke()
        
        # === SHOULDER PADS ===
        cr.set_source_rgb(0.82, 0.85, 0.88)
        # Left shoulder
        cr.save()
        cr.translate(cx - 22*s, cy - 12*s)
        cr.rotate(-0.3)
        self._draw_rounded_rect_shape(cr, -8*s, -4*s, 16*s, 8*s, 2*s)
        cr.fill()
        cr.restore()
        # Right shoulder
        cr.save()
        cr.translate(cx + 22*s, cy - 12*s)
        cr.rotate(0.3)
        self._draw_rounded_rect_shape(cr, -8*s, -4*s, 16*s, 8*s, 2*s)
        cr.fill()
        cr.restore()
        
        # Shoulder joint details
        cr.set_source_rgb(0.4, 0.42, 0.45)
        cr.arc(cx - 22*s, cy - 12*s, 3*s, 0, 2*math.pi)
        cr.arc(cx + 22*s, cy - 12*s, 3*s, 0, 2*math.pi)
        cr.fill()
        
        # === JETPACK / THRUSTER SYSTEM ===
        # Jetpack mounting (behind lower torso)
        cr.set_source_rgb(0.55, 0.58, 0.62)
        # Connection struts
        cr.rectangle(cx - 8*s, cy + 18*s, 3*s, 8*s)
        cr.rectangle(cx + 5*s, cy + 18*s, 3*s, 8*s)
        cr.fill()
        
        # Thruster nozzles
        cr.set_source_rgb(0.45, 0.48, 0.52)
        # Left nozzle
        cr.save()
        cr.translate(cx - 6.5*s, cy + 26*s)
        cr.move_to(-3*s, 0)
        cr.line_to(-4*s, 8*s)
        cr.line_to(1*s, 8*s)
        cr.line_to(0, 0)
        cr.close_path()
        cr.fill()
        cr.restore()
        # Right nozzle
        cr.save()
        cr.translate(cx + 6.5*s, cy + 26*s)
        cr.move_to(-3*s, 0)
        cr.line_to(-4*s, 8*s)
        cr.line_to(1*s, 8*s)
        cr.line_to(0, 0)
        cr.close_path()
        cr.fill()
        cr.restore()
        
        # Nozzle interior (dark)
        cr.set_source_rgb(0.15, 0.15, 0.18)
        cr.rectangle(cx - 9*s, cy + 34*s, 4*s, 2*s)
        cr.rectangle(cx + 5*s, cy + 34*s, 4*s, 2*s)
        cr.fill()
    
    def _draw_astronaut_jetpack_flames(self, cr, cx, cy, s):
        """Draw animated jetpack flames - called after legs so flames are visible"""
        # === THRUST FLAMES (animated) ===
        flame_intensity = abs(math.sin(self.frame * 0.3))
        flame_offset = math.sin(self.frame * 0.4) * 2*s
        
        # Left thruster flame
        for i in range(3):
            alpha = 0.7 - i * 0.2
            flame_length = (8 + i * 4) * s * (0.8 + flame_intensity * 0.4)
            
            # Orange inner flame
            cr.set_source_rgba(1, 0.6, 0.1, alpha)
            cr.save()
            cr.translate(cx - 7*s, cy + 36*s + flame_offset)
            cr.move_to(-2*s, 0)
            cr.curve_to(
                -3*s, flame_length * 0.4,
                -2*s, flame_length * 0.7,
                0, flame_length
            )
            cr.curve_to(
                2*s, flame_length * 0.7,
                3*s, flame_length * 0.4,
                2*s, 0
            )
            cr.close_path()
            cr.fill()
            cr.restore()
            
        # Yellow/white core
        cr.set_source_rgba(1, 1, 0.8, 0.9)
        cr.save()
        cr.translate(cx - 7*s, cy + 36*s + flame_offset)
        cr.move_to(-1*s, 0)
        cr.curve_to(-1*s, 3*s, -0.5*s, 4*s, 0, 5*s)
        cr.curve_to(0.5*s, 4*s, 1*s, 3*s, 1*s, 0)
        cr.close_path()
        cr.fill()
        cr.restore()
        
        # Right thruster flame
        for i in range(3):
            alpha = 0.7 - i * 0.2
            flame_length = (8 + i * 4) * s * (0.8 + flame_intensity * 0.4)
            
            # Orange inner flame
            cr.set_source_rgba(1, 0.6, 0.1, alpha)
            cr.save()
            cr.translate(cx + 7*s, cy + 36*s - flame_offset)
            cr.move_to(-2*s, 0)
            cr.curve_to(
                -3*s, flame_length * 0.4,
                -2*s, flame_length * 0.7,
                0, flame_length
            )
            cr.curve_to(
                2*s, flame_length * 0.7,
                3*s, flame_length * 0.4,
                2*s, 0
            )
            cr.close_path()
            cr.fill()
            cr.restore()
            
        # Yellow/white core
        cr.set_source_rgba(1, 1, 0.8, 0.9)
        cr.save()
        cr.translate(cx + 7*s, cy + 36*s - flame_offset)
        cr.move_to(-1*s, 0)
        cr.curve_to(-1*s, 3*s, -0.5*s, 4*s, 0, 5*s)
        cr.curve_to(0.5*s, 4*s, 1*s, 3*s, 1*s, 0)
        cr.close_path()
        cr.fill()
        cr.restore()
        
        # Sparkles/particles
        if self.frame % 10 < 5:
            cr.set_source_rgba(1, 0.8, 0.3, 0.6)
            for i in range(4):
                particle_offset = (self.frame + i * 7) % 20
                particle_x = cx + (i % 2 * 14 - 7) * s
                particle_y = cy + 38*s + particle_offset * s
                cr.arc(particle_x, particle_y, 1*s, 0, 2*math.pi)
                cr.fill()
    
    def _draw_dragon_body(self, cr, cx, cy, s, color):
        """Draw dragon-style body with scales and wings"""
        # Body
        cr.set_source_rgb(*color)
        self._draw_body(cr, cx, cy, s)
        
        # Scales pattern
        cr.set_source_rgba(0, 0, 0, 0.15)
        for i in range(3):
            for j in range(3):
                x_offset = (i - 1) * 10*s
                y_offset = (j - 1) * 10*s
                cr.arc(cx + x_offset, cy + y_offset, 4*s, 0, 2*math.pi)
                cr.fill()
        
        # Wings
        cr.set_source_rgba(*[c * 0.8 for c in color])
        # Left wing
        cr.move_to(cx - 25*s, cy)
        cr.curve_to(cx - 45*s, cy - 20*s, cx - 45*s, cy + 10*s, cx - 25*s, cy + 15*s)
        cr.close_path()
        cr.fill()
        # Right wing
        cr.move_to(cx + 25*s, cy)
        cr.curve_to(cx + 45*s, cy - 20*s, cx + 45*s, cy + 10*s, cx + 25*s, cy + 15*s)
        cr.close_path()
        cr.fill()
        
        # Spikes on back
        cr.set_source_rgba(*[c * 0.6 for c in color])
        for i in range(3):
            x = cx - 15*s + i * 15*s
            cr.move_to(x, cy - 25*s)
            cr.line_to(x - 5*s, cy - 35*s)
            cr.line_to(x + 5*s, cy - 25*s)
            cr.close_path()
            cr.fill()
    
    def _draw_alien_body(self, cr, cx, cy, s, color):
        """Draw alien-style body with antennae"""
        # Body (oval shaped)
        cr.set_source_rgb(*color)
        cr.save()
        cr.translate(cx, cy)
        cr.scale(1, 1.2)
        cr.arc(0, 0, 25*s, 0, 2*math.pi)
        cr.restore()
        cr.fill()
        
        # Antennae
        cr.set_source_rgba(*[c * 0.7 for c in color])
        cr.set_line_width(2*s)
        # Left antenna
        cr.move_to(cx - 15*s, cy - 25*s)
        cr.line_to(cx - 20*s, cy - 40*s)
        cr.stroke()
        # Right antenna
        cr.move_to(cx + 15*s, cy - 25*s)
        cr.line_to(cx + 20*s, cy - 40*s)
        cr.stroke()
        
        # Antenna balls (glowing)
        if self.frame % 30 < 15:
            cr.set_source_rgb(1, 1, 0.3)
        else:
            cr.set_source_rgb(0.5, 1, 0.5)
        cr.arc(cx - 20*s, cy - 42*s, 4*s, 0, 2*math.pi)
        cr.arc(cx + 20*s, cy - 42*s, 4*s, 0, 2*math.pi)
        cr.fill()
        
        # Spots
        cr.set_source_rgba(0, 0, 0, 0.2)
        cr.arc(cx - 10*s, cy - 5*s, 5*s, 0, 2*math.pi)
        cr.arc(cx + 8*s, cy + 10*s, 6*s, 0, 2*math.pi)
        cr.fill()
    
    def _draw_ninja_body(self, cr, cx, cy, s, color):
        """Draw ninja-style body with mask"""
        # Body
        cr.set_source_rgb(*color)
        self._draw_body(cr, cx, cy, s)
        
        # Ninja mask (covers lower face)
        cr.set_source_rgb(0.1, 0.1, 0.15)
        cr.arc(cx, cy + 8*s, 20*s, 0, math.pi)
        cr.fill()
        
        # Headband
        cr.set_source_rgb(0.8, 0.1, 0.1)
        cr.rectangle(cx - 28*s, cy - 20*s, 56*s, 6*s)
        cr.fill()
        
        # Headband knot
        cr.set_line_width(3*s)
        cr.move_to(cx + 25*s, cy - 17*s)
        cr.line_to(cx + 35*s, cy - 20*s)
        cr.line_to(cx + 30*s, cy - 10*s)
        cr.stroke()
    
    def _draw_wizard_body(self, cr, cx, cy, s, color):
        """Draw wizard-style body with robe and hat"""
        # Robe body
        cr.set_source_rgb(*color)
        cr.move_to(cx, cy - 28*s)
        cr.line_to(cx - 30*s, cy + 25*s)
        cr.line_to(cx + 30*s, cy + 25*s)
        cr.close_path()
        cr.fill()
        
        # Hat
        cr.set_source_rgb(*[c * 0.7 for c in color])
        # Hat cone
        cr.move_to(cx, cy - 50*s)
        cr.line_to(cx - 20*s, cy - 25*s)
        cr.line_to(cx + 20*s, cy - 25*s)
        cr.close_path()
        cr.fill()
        # Hat brim
        cr.move_to(cx - 25*s, cy - 25*s)
        cr.line_to(cx + 25*s, cy - 25*s)
        cr.line_to(cx + 25*s, cy - 22*s)
        cr.line_to(cx - 25*s, cy - 22*s)
        cr.close_path()
        cr.fill()
        
        # Stars on robe
        cr.set_source_rgb(1, 1, 0.3)
        for i in range(3):
            y = cy - 10*s + i * 10*s
            self._draw_star(cr, cx - 10*s, y, 3*s)
            self._draw_star(cr, cx + 10*s, y + 5*s, 3*s)
    
    def _draw_penguin_body(self, cr, cx, cy, s, color):
        """Draw penguin-style body"""
        # Black body
        cr.set_source_rgb(*color)
        cr.save()
        cr.translate(cx, cy)
        cr.scale(1, 1.1)
        cr.arc(0, 0, 28*s, 0, 2*math.pi)
        cr.restore()
        cr.fill()
        
        # White belly
        cr.set_source_rgb(1, 1, 1)
        cr.save()
        cr.translate(cx, cy + 5*s)
        cr.scale(0.6, 0.8)
        cr.arc(0, 0, 25*s, 0, 2*math.pi)
        cr.restore()
        cr.fill()
        
        # Flippers
        cr.set_source_rgb(*color)
        # Left flipper
        cr.save()
        cr.translate(cx - 25*s, cy)
        cr.rotate(-0.3)
        cr.move_to(0, 0)
        cr.curve_to(-10*s, 5*s, -15*s, 15*s, -5*s, 20*s)
        cr.close_path()
        cr.restore()
        cr.fill()
        # Right flipper
        cr.save()
        cr.translate(cx + 25*s, cy)
        cr.rotate(0.3)
        cr.move_to(0, 0)
        cr.curve_to(10*s, 5*s, 15*s, 15*s, 5*s, 20*s)
        cr.close_path()
        cr.restore()
        cr.fill()
        
        # Orange beak
        cr.set_source_rgb(1, 0.5, 0)
        cr.move_to(cx, cy + 5*s)
        cr.line_to(cx - 8*s, cy + 10*s)
        cr.line_to(cx + 8*s, cy + 10*s)
        cr.close_path()
        cr.fill()
    
    def _draw_bear_body(self, cr, cx, cy, s, color):
        """Draw bear-style body"""
        # Body
        cr.set_source_rgb(*color)
        self._draw_body(cr, cx, cy, s)
        
        # Ears
        cr.set_source_rgb(*color)
        cr.arc(cx - 20*s, cy - 25*s, 10*s, 0, 2*math.pi)
        cr.arc(cx + 20*s, cy - 25*s, 10*s, 0, 2*math.pi)
        cr.fill()
        
        # Inner ears
        cr.set_source_rgba(*[c * 0.7 for c in color])
        cr.arc(cx - 20*s, cy - 25*s, 6*s, 0, 2*math.pi)
        cr.arc(cx + 20*s, cy - 25*s, 6*s, 0, 2*math.pi)
        cr.fill()
        
        # Snout
        cr.set_source_rgba(*[min(c + 0.1, 1) for c in color])
        cr.arc(cx, cy + 10*s, 12*s, 0, 2*math.pi)
        cr.fill()
        
        # Nose
        cr.set_source_rgb(0.2, 0.2, 0.2)
        cr.arc(cx, cy + 8*s, 5*s, 0, 2*math.pi)
        cr.fill()
    
    def _draw_ghost_body(self, cr, cx, cy, s, color):
        """Draw ghost-style body with wavy bottom"""
        # Ghost body
        cr.set_source_rgb(*color)
        
        # Top part (rounded)
        cr.arc(cx, cy - 10*s, 25*s, math.pi, 0)
        
        # Wavy bottom
        points = []
        for i in range(7):
            angle = i * math.pi / 6
            wave_offset = math.sin(self.frame * 0.1 + angle * 2) * 3*s
            x = cx - 25*s + i * 8.5*s
            y = cy + 20*s + wave_offset
            points.append((x, y))
        
        for i, (x, y) in enumerate(points):
            if i == 0:
                cr.line_to(x, y)
            else:
                cr.curve_to(
                    points[i-1][0] + 4*s, points[i-1][1],
                    x - 4*s, y,
                    x, y
                )
        
        cr.close_path()
        cr.fill()
        
        # Transparency effect
        cr.set_source_rgba(*color, 0.3)
        cr.arc(cx, cy, 20*s, 0, 2*math.pi)
        cr.fill()
    
    def _draw_pirate_body(self, cr, cx, cy, s, color):
        """Draw pirate-style body with hat and eye patch"""
        # Body
        cr.set_source_rgb(*color)
        self._draw_body(cr, cx, cy, s)
        
        # Pirate hat
        cr.set_source_rgb(0.2, 0.2, 0.25)
        # Hat base
        cr.move_to(cx - 30*s, cy - 25*s)
        cr.line_to(cx + 30*s, cy - 25*s)
        cr.line_to(cx + 25*s, cy - 15*s)
        cr.line_to(cx - 25*s, cy - 15*s)
        cr.close_path()
        cr.fill()
        # Hat top
        cr.move_to(cx - 20*s, cy - 25*s)
        cr.line_to(cx, cy - 45*s)
        cr.line_to(cx + 20*s, cy - 25*s)
        cr.close_path()
        cr.fill()
        
        # Skull and crossbones on hat
        cr.set_source_rgb(1, 1, 1)
        cr.arc(cx, cy - 33*s, 4*s, 0, 2*math.pi)
        cr.fill()
        cr.set_line_width(2*s)
        cr.move_to(cx - 5*s, cy - 27*s)
        cr.line_to(cx + 5*s, cy - 27*s)
        cr.move_to(cx, cy - 32*s)
        cr.line_to(cx, cy - 22*s)
        cr.stroke()
        
        # Eye patch
        cr.set_source_rgb(0.1, 0.1, 0.1)
        cr.arc(cx + 10*s, cy - 5*s, 8*s, 0, 2*math.pi)
        cr.fill()
        # Eye patch string
        cr.set_line_width(2*s)
        cr.arc(cx, cy - 5*s, 28*s, -0.3, 0.3)
        cr.stroke()
    
    def _draw_star(self, cr, cx, cy, size):
        """Helper to draw a star shape"""
        cr.save()
        cr.translate(cx, cy)
        for i in range(5):
            angle = i * 2 * math.pi / 5 - math.pi / 2
            r = size if i % 2 == 0 else size / 2
            x = math.cos(angle) * r
            y = math.sin(angle) * r
            if i == 0:
                cr.move_to(x, y)
            else:
                cr.line_to(x, y)
        cr.close_path()
        cr.fill()
        cr.restore()
    
    def _draw_rounded_rect_shape(self, cr, x, y, w, h, r):
        """Draw a rounded rectangle path"""
        cr.move_to(x + r, y)
        cr.line_to(x + w - r, y)
        cr.arc(x + w - r, y + r, r, -math.pi/2, 0)
        cr.line_to(x + w, y + h - r)
        cr.arc(x + w - r, y + h - r, r, 0, math.pi/2)
        cr.line_to(x + r, y + h)
        cr.arc(x + r, y + h - r, r, math.pi/2, math.pi)
        cr.line_to(x, y + r)
        cr.arc(x + r, y + r, r, math.pi, 3*math.pi/2)
        cr.close_path()
    
    def _draw_theme_accessories(self, cr, cx, cy, s):
        """Draw theme-specific accessories"""
        if self.theme == 'cat':
            # Whiskers
            cr.set_source_rgba(0.3, 0.3, 0.3, 0.6)
            cr.set_line_width(1*s)
            # Left whiskers
            for i, angle in enumerate([-0.2, 0, 0.2]):
                cr.move_to(cx - 18*s, cy + 5*s + i*3*s)
                cr.line_to(cx - 35*s, cy + 3*s + i*3*s + angle*10*s)
                cr.stroke()
            # Right whiskers
            for i, angle in enumerate([-0.2, 0, 0.2]):
                cr.move_to(cx + 18*s, cy + 5*s + i*3*s)
                cr.line_to(cx + 35*s, cy + 3*s + i*3*s + angle*10*s)
                cr.stroke()
    
    def _draw_ellipse(self, cr, x, y, width, height):
        """Draw an ellipse centered at (x + width/2, y + height/2)"""
        cr.save()
        cr.translate(x + width/2, y + height/2)
        cr.scale(width/2, height/2)
        cr.arc(0, 0, 1, 0, 2*math.pi)
        cr.restore()
    
    def _draw_body(self, cr, cx, cy, s):
        """Draw the main body blob"""
        # Main body ellipse
        cr.save()
        cr.translate(cx, cy)
        cr.scale(1, 0.9)
        cr.arc(0, 0, 28*s, 0, 2*math.pi)
        cr.restore()
        cr.fill()
        
        # Highlight
        cr.set_source_rgba(1, 1, 1, 0.3)
        cr.arc(cx - 8*s, cy - 10*s, 8*s, 0, 2*math.pi)
        cr.fill()
    
    def _draw_face(self, cr, cx, cy, s):
        """Draw eyes and mouth with emotional expressions"""
        eye_y = cy - 5*s
        left_eye_x = cx - 10*s
        right_eye_x = cx + 10*s
        
        # Eyes based on emotion
        if self.is_blinking or self.state == self.SLEEPING or self.state == self.TIRED:
            # Closed eyes (lines)
            cr.set_source_rgb(0.2, 0.2, 0.2)
            cr.set_line_width(2*s)
            cr.move_to(left_eye_x - 5*s, eye_y)
            cr.line_to(left_eye_x + 5*s, eye_y)
            cr.move_to(right_eye_x - 5*s, eye_y)
            cr.line_to(right_eye_x + 5*s, eye_y)
            cr.stroke()
        elif self.state == self.CRYING:
            # Sad closed eyes with tears
            cr.set_source_rgb(0.2, 0.2, 0.2)
            cr.set_line_width(2*s)
            # Upward curved closed eyes
            cr.arc(left_eye_x, eye_y + 2*s, 5*s, math.pi, 0)
            cr.stroke()
            cr.arc(right_eye_x, eye_y + 2*s, 5*s, math.pi, 0)
            cr.stroke()
            # Tears
            cr.set_source_rgba(0.3, 0.5, 0.9, 0.7)
            tear_offset = (self.frame % 20) * 1*s
            cr.arc(left_eye_x, eye_y + 5*s + tear_offset, 2*s, 0, 2*math.pi)
            cr.arc(right_eye_x, eye_y + 5*s + tear_offset, 2*s, 0, 2*math.pi)
            cr.fill()
        elif self.state == self.SHOCKED or self.state == self.CONFUSED:
            # Wide open eyes
            cr.set_source_rgb(1, 1, 1)
            cr.arc(left_eye_x, eye_y, 9*s, 0, 2*math.pi)
            cr.arc(right_eye_x, eye_y, 9*s, 0, 2*math.pi)
            cr.fill()
            # Large pupils
            cr.set_source_rgb(0.1, 0.1, 0.1)
            pupil_size = 4*s if self.state == self.SHOCKED else 3*s
            cr.arc(left_eye_x, eye_y, pupil_size, 0, 2*math.pi)
            cr.arc(right_eye_x, eye_y, pupil_size, 0, 2*math.pi)
            cr.fill()
        elif self.state == self.ANGRY:
            # Angry eyes (angled)
            cr.set_source_rgb(1, 1, 1)
            cr.arc(left_eye_x, eye_y, 7*s, 0, 2*math.pi)
            cr.arc(right_eye_x, eye_y, 7*s, 0, 2*math.pi)
            cr.fill()
            # Pupils
            cr.set_source_rgb(0.8, 0.1, 0.1)
            cr.arc(left_eye_x, eye_y, 3*s, 0, 2*math.pi)
            cr.arc(right_eye_x, eye_y, 3*s, 0, 2*math.pi)
            cr.fill()
            # Angry eyebrows
            cr.set_source_rgb(0.2, 0.2, 0.2)
            cr.set_line_width(3*s)
            cr.move_to(left_eye_x - 8*s, eye_y - 10*s)
            cr.line_to(left_eye_x + 3*s, eye_y - 7*s)
            cr.move_to(right_eye_x - 3*s, eye_y - 7*s)
            cr.line_to(right_eye_x + 8*s, eye_y - 10*s)
            cr.stroke()
        elif self.state == self.LAUGHING or self.state == self.EXCITED:
            # Happy squinted eyes
            cr.set_source_rgb(0.2, 0.2, 0.2)
            cr.set_line_width(2*s)
            cr.arc(left_eye_x, eye_y, 6*s, 0.3, math.pi - 0.3)
            cr.stroke()
            cr.arc(right_eye_x, eye_y, 6*s, 0.3, math.pi - 0.3)
            cr.stroke()
        elif self.state == self.SAD:
            # Sad droopy eyes
            cr.set_source_rgb(1, 1, 1)
            cr.arc(left_eye_x, eye_y, 7*s, 0, 2*math.pi)
            cr.arc(right_eye_x, eye_y, 7*s, 0, 2*math.pi)
            cr.fill()
            # Pupils looking down
            cr.set_source_rgb(0.1, 0.1, 0.1)
            cr.arc(left_eye_x, eye_y + 3*s, 3*s, 0, 2*math.pi)
            cr.arc(right_eye_x, eye_y + 3*s, 3*s, 0, 2*math.pi)
            cr.fill()
            # Sad eyebrows
            cr.set_source_rgb(0.2, 0.2, 0.2)
            cr.set_line_width(2*s)
            cr.arc(left_eye_x, eye_y - 10*s, 8*s, 0.5, math.pi - 0.5)
            cr.stroke()
            cr.arc(right_eye_x, eye_y - 10*s, 8*s, 0.5, math.pi - 0.5)
            cr.stroke()
        else:
            # Normal open eyes
            cr.set_source_rgb(1, 1, 1)
            cr.arc(left_eye_x, eye_y, 7*s, 0, 2*math.pi)
            cr.arc(right_eye_x, eye_y, 7*s, 0, 2*math.pi)
            cr.fill()
            
            # Pupils - look direction based on state
            pupil_offset_x = 0
            pupil_offset_y = 0
            if self.state == self.THINKING or self.state == self.CONFUSED:
                pupil_offset_x = 3*s
                pupil_offset_y = -2*s
            elif self.state == self.WORKING:
                pupil_offset_y = 2*s  # Looking down at work
            elif self.state == self.RUNNING:
                pupil_offset_x = 3*s * math.sin(self.frame * 0.3)
            
            cr.set_source_rgb(0.1, 0.1, 0.1)
            cr.arc(left_eye_x + pupil_offset_x, eye_y + pupil_offset_y, 3*s, 0, 2*math.pi)
            cr.arc(right_eye_x + pupil_offset_x, eye_y + pupil_offset_y, 3*s, 0, 2*math.pi)
            cr.fill()
            
            # Eye shine
            cr.set_source_rgba(1, 1, 1, 0.8)
            cr.arc(left_eye_x + 2*s, eye_y - 2*s, 1.5*s, 0, 2*math.pi)
            cr.arc(right_eye_x + 2*s, eye_y - 2*s, 1.5*s, 0, 2*math.pi)
            cr.fill()
        
        # Mouth based on emotion
        mouth_y = cy + 10*s
        cr.set_source_rgb(0.2, 0.2, 0.2)
        cr.set_line_width(2*s)
        
        if self.state == self.CELEBRATING or self.state == self.LAUGHING or self.state == self.EXCITED:
            # Big happy mouth
            cr.arc(cx, mouth_y - 5*s, 10*s, 0.2, math.pi - 0.2)
            cr.stroke()
        elif self.state == self.SLEEPING or self.state == self.TIRED or self.state == self.MEDITATING:
            # Relaxed mouth
            cr.move_to(cx - 5*s, mouth_y)
            cr.line_to(cx + 5*s, mouth_y)
            cr.stroke()
        elif self.state == self.ANGRY:
            # Frowning mouth
            cr.arc(cx, mouth_y + 8*s, 8*s, math.pi + 0.3, 2*math.pi - 0.3)
            cr.stroke()
        elif self.state == self.SAD or self.state == self.CRYING:
            # Sad frown
            cr.arc(cx, mouth_y + 8*s, 10*s, math.pi + 0.2, 2*math.pi - 0.2)
            cr.stroke()
        elif self.state == self.SHOCKED:
            # Open mouth (O shape)
            cr.arc(cx, mouth_y + 3*s, 5*s, 0, 2*math.pi)
            cr.stroke()
        elif self.state == self.THINKING or self.state == self.CONFUSED:
            # Hmm mouth (small o)
            cr.arc(cx + 5*s, mouth_y, 3*s, 0, 2*math.pi)
            cr.stroke()
        elif self.state == self.DANCING:
            # Playful smile
            animated_offset = math.sin(self.frame * 0.2) * 2*s
            cr.arc(cx, mouth_y - 3*s + animated_offset, 8*s, 0.3, math.pi - 0.3)
            cr.stroke()
        else:
            # Normal smile
            cr.arc(cx, mouth_y - 3*s, 8*s, 0.3, math.pi - 0.3)
            cr.stroke()
        
        # Blush cheeks (more intense for certain emotions)
        blush_alpha = 0.3
        if self.state in [self.EXCITED, self.LAUGHING, self.CELEBRATING]:
            blush_alpha = 0.5
        elif self.state in [self.ANGRY, self.CRYING]:
            blush_alpha = 0.4
        
        cr.set_source_rgba(1, 0.5, 0.5, blush_alpha)
        cr.arc(cx - 18*s, cy + 3*s, 5*s, 0, 2*math.pi)
        cr.arc(cx + 18*s, cy + 3*s, 5*s, 0, 2*math.pi)
        cr.fill()
    
    def _draw_arms(self, cr, cx, cy, s, color):
        """Draw arms based on current state"""
        cr.set_source_rgb(*[c * 0.9 for c in color])
        cr.set_line_width(8*s)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        
        # Left arm
        left_arm_angle = 0
        left_arm_length = 15*s
        
        # Right arm
        right_arm_angle = 0
        right_arm_length = 15*s
        
        if self.state == self.WAVING:
            # Wave animation
            right_arm_angle = -0.8 + math.sin(self.frame * 0.3) * 0.4
            right_arm_length = 20*s
        elif self.state == self.WORKING:
            # Typing motion
            left_arm_angle = 0.5 + math.sin(self.frame * 0.4) * 0.1
            right_arm_angle = 0.5 + math.cos(self.frame * 0.4) * 0.1
        elif self.state == self.THINKING or self.state == self.CONFUSED:
            # Hand on chin
            right_arm_angle = -0.3
            right_arm_length = 18*s
        elif self.state == self.RUNNING:
            # Running arms
            left_arm_angle = math.sin(self.frame * 0.3) * 0.5
            right_arm_angle = -math.sin(self.frame * 0.3) * 0.5
        elif self.state == self.CELEBRATING or self.state == self.EXCITED:
            # Arms up!
            left_arm_angle = -0.8 + math.sin(self.frame * 0.2) * 0.2
            right_arm_angle = -0.8 + math.cos(self.frame * 0.2) * 0.2
            left_arm_length = 20*s
            right_arm_length = 20*s
        elif self.state == self.SLEEPING or self.state == self.TIRED:
            left_arm_angle = 0.8
            right_arm_angle = 0.8
        elif self.state == self.ANGRY:
            # Fists clenched down
            left_arm_angle = 0.6
            right_arm_angle = 0.6
            left_arm_length = 18*s
            right_arm_length = 18*s
        elif self.state == self.CRYING or self.state == self.SAD:
            # Arms drooping
            left_arm_angle = 0.9
            right_arm_angle = 0.9
        elif self.state == self.SHOCKED:
            # Arms out in surprise
            left_arm_angle = -0.5
            right_arm_angle = -0.5
            left_arm_length = 18*s
            right_arm_length = 18*s
        elif self.state == self.DANCING:
            # Dancing arms
            left_arm_angle = -0.5 + math.sin(self.frame * 0.4) * 0.6
            right_arm_angle = -0.5 + math.cos(self.frame * 0.4) * 0.6
            left_arm_length = 18*s
            right_arm_length = 18*s
        elif self.state == self.MEDITATING:
            # Meditation pose
            left_arm_angle = 0.3
            right_arm_angle = 0.3
        elif self.state == self.LAUGHING:
            # Holding belly laugh
            left_arm_angle = 0.4
            right_arm_angle = 0.4
        
        # Draw left arm
        arm_start_x = cx - 22*s
        arm_start_y = cy + 5*s
        cr.move_to(arm_start_x, arm_start_y)
        cr.line_to(
            arm_start_x - math.cos(left_arm_angle) * left_arm_length,
            arm_start_y + math.sin(left_arm_angle + 0.5) * left_arm_length
        )
        cr.stroke()
        
        # Draw right arm
        arm_start_x = cx + 22*s
        cr.move_to(arm_start_x, arm_start_y)
        cr.line_to(
            arm_start_x + math.cos(right_arm_angle) * right_arm_length,
            arm_start_y + math.sin(right_arm_angle + 0.5) * right_arm_length
        )
        cr.stroke()
    
    def _draw_ironman_body(self, cr, cx, cy, s, color):
        """Draw realistic Iron Man Mark 50 armor"""
        # === CHEST ARMOR (realistic plating) ===
        # Dark red base layer
        cr.set_source_rgb(0.55, 0.08, 0.08)
        
        # Main chest plate (angular, not rounded)
        chest_plates = [
            # Left pectoral plate
            [(cx - 22*s, cy - 8*s), (cx - 18*s, cy - 24*s), (cx - 2*s, cy - 20*s), (cx - 4*s, cy - 6*s)],
            # Right pectoral plate
            [(cx + 4*s, cy - 6*s), (cx + 2*s, cy - 20*s), (cx + 18*s, cy - 24*s), (cx + 22*s, cy - 8*s)]
        ]
        
        for plate in chest_plates:
            cr.move_to(*plate[0])
            for point in plate[1:]:
                cr.line_to(*point)
            cr.close_path()
            cr.fill()
            
            # Metallic highlight on each plate
            cr.set_source_rgba(0.9, 0.3, 0.2, 0.3)
            cr.move_to(*plate[0])
            for i, point in enumerate(plate[1:3]):
                cr.line_to(*point)
            cr.close_path()
            cr.fill()
        
        # Central sternum plate (gold)
        cr.set_source_rgb(0.78, 0.55, 0.12)
        sternum_points = [
            (cx - 4*s, cy - 6*s),
            (cx - 2*s, cy - 20*s),
            (cx + 2*s, cy - 20*s),
            (cx + 4*s, cy - 6*s),
            (cx + 3*s, cy + 8*s),
            (cx - 3*s, cy + 8*s)
        ]
        cr.move_to(*sternum_points[0])
        for point in sternum_points[1:]:
            cr.line_to(*point)
        cr.close_path()
        cr.fill()
        
        # Gold metallic shine
        cr.set_source_rgba(1, 0.85, 0.4, 0.4)
        cr.move_to(cx - 3*s, cy - 18*s)
        cr.line_to(cx + 1*s, cy - 19*s)
        cr.line_to(cx + 2*s, cy - 8*s)
        cr.line_to(cx - 1*s, cy - 7*s)
        cr.close_path()
        cr.fill()
        
        # === ARC REACTOR (high detail) ===
        reactor_pulse = abs(math.sin(self.frame * 0.15))
        reactor_glow = 0.85 + reactor_pulse * 0.15
        
        # Housing rim (dark metal)
        cr.set_source_rgb(0.25, 0.28, 0.32)
        cr.arc(cx, cy - 2*s, 9*s, 0, 2*math.pi)
        cr.fill()
        
        # Outer ring (metallic)
        cr.set_source_rgb(0.4, 0.45, 0.5)
        cr.set_line_width(1.5*s)
        cr.arc(cx, cy - 2*s, 8*s, 0, 2*math.pi)
        cr.stroke()
        
        # Glow corona
        cr.set_source_rgba(0.4, 0.7, 1, 0.3 * reactor_glow)
        cr.arc(cx, cy - 2*s, 10*s, 0, 2*math.pi)
        cr.fill()
        
        # Energy ring
        cr.set_source_rgba(0.3, 0.6, 0.95, reactor_glow)
        cr.arc(cx, cy - 2*s, 7*s, 0, 2*math.pi)
        cr.fill()
        
        # Bright core
        cr.set_source_rgba(0.6, 0.85, 1, reactor_glow)
        cr.arc(cx, cy - 2*s, 5*s, 0, 2*math.pi)
        cr.fill()
        
        # Hot center
        cr.set_source_rgba(0.85, 0.95, 1, reactor_glow)
        cr.arc(cx, cy - 2*s, 3*s, 0, 2*math.pi)
        cr.fill()
        
        # White hot core
        cr.set_source_rgba(1, 1, 1, 0.95)
        cr.arc(cx, cy - 2*s, 1.5*s, 0, 2*math.pi)
        cr.fill()
        
        # Triangular energy pattern
        cr.set_source_rgba(0.2, 0.4, 0.6, 0.7)
        cr.set_line_width(0.8*s)
        for i in range(3):
            angle = i * 2 * math.pi / 3 + self.frame * 0.02
            x1 = cx + math.cos(angle) * 2*s
            y1 = cy - 2*s + math.sin(angle) * 2*s
            x2 = cx + math.cos(angle) * 7*s
            y2 = cy - 2*s + math.sin(angle) * 7*s
            cr.move_to(x1, y1)
            cr.line_to(x2, y2)
            cr.stroke()
        
        # === ABDOMINAL ARMOR ===
        cr.set_source_rgb(0.78, 0.55, 0.12)
        ab_segments = [
            [(cx - 16*s, cy + 8*s), (cx - 14*s, cy + 12*s), (cx - 3*s, cy + 12*s), (cx - 3*s, cy + 8*s)],
            [(cx + 3*s, cy + 8*s), (cx + 3*s, cy + 12*s), (cx + 14*s, cy + 12*s), (cx + 16*s, cy + 8*s)],
            [(cx - 14*s, cy + 13*s), (cx - 12*s, cy + 18*s), (cx - 3*s, cy + 18*s), (cx - 3*s, cy + 13*s)],
            [(cx + 3*s, cy + 13*s), (cx + 3*s, cy + 18*s), (cx + 12*s, cy + 18*s), (cx + 14*s, cy + 13*s)]
        ]
        
        for seg in ab_segments:
            cr.move_to(*seg[0])
            for point in seg[1:]:
                cr.line_to(*point)
            cr.close_path()
            cr.fill()
        
        # Dark panel lines between segments
        cr.set_source_rgba(0.1, 0.1, 0.12, 0.8)
        cr.set_line_width(1.2*s)
        cr.move_to(cx - 16*s, cy + 8*s)
        cr.line_to(cx + 16*s, cy + 8*s)
        cr.move_to(cx - 3*s, cy + 8*s)
        cr.line_to(cx - 3*s, cy + 18*s)
        cr.move_to(cx + 3*s, cy + 8*s)
        cr.line_to(cx + 3*s, cy + 18*s)
        cr.move_to(cx - 14*s, cy + 12*s)
        cr.line_to(cx - 3*s, cy + 12*s)
        cr.move_to(cx + 3*s, cy + 12*s)
        cr.line_to(cx + 14*s, cy + 12*s)
        cr.stroke()
        
        # === SHOULDER PAULDRONS (angular armor) ===
        # Left shoulder
        cr.set_source_rgb(0.6, 0.09, 0.09)
        cr.save()
        cr.translate(cx - 25*s, cy - 14*s)
        cr.rotate(-0.25)
        # Multi-layer shoulder plate
        shoulder_layers = [
            [(-7*s, -8*s), (-5*s, -8*s), (-3*s, -4*s), (-5*s, 0)],
            [(-5*s, 0), (-3*s, -4*s), (0, -2*s), (0, 4*s), (-3*s, 6*s)],
            [(0, 4*s), (0, -2*s), (5*s, 0), (7*s, 4*s), (4*s, 8*s)]
        ]
        for layer in shoulder_layers:
            cr.move_to(*layer[0])
            for point in layer[1:]:
                cr.line_to(*point)
            cr.close_path()
            cr.fill()
            # Highlight
            cr.set_source_rgba(0.85, 0.2, 0.15, 0.25)
            cr.move_to(*layer[0])
            cr.line_to(*layer[1])
            cr.line_to(*layer[2])
            cr.stroke()
        cr.restore()
        
        # Right shoulder (mirrored)
        cr.set_source_rgb(0.6, 0.09, 0.09)
        cr.save()
        cr.translate(cx + 25*s, cy - 14*s)
        cr.rotate(0.25)
        for layer in shoulder_layers:
            mirrored = [(-x, y) for x, y in layer]
            cr.move_to(*mirrored[0])
            for point in mirrored[1:]:
                cr.line_to(*point)
            cr.close_path()
            cr.fill()
            cr.set_source_rgba(0.85, 0.2, 0.15, 0.25)
            cr.move_to(*mirrored[0])
            cr.line_to(*mirrored[1])
            cr.line_to(*mirrored[2])
            cr.stroke()
        cr.restore()
        
        # === HELMET (Mark 50 accurate design) ===
        mask_lift = self.mask_animation * 2.5 * s
        
        # Back of helmet (red)
        cr.set_source_rgb(0.6, 0.09, 0.09)
        helmet_back = [
            (cx - 20*s, cy - 8*s),
            (cx - 18*s, cy - 26*s),
            (cx - 12*s, cy - 32*s),
            (cx + 12*s, cy - 32*s),
            (cx + 18*s, cy - 26*s),
            (cx + 20*s, cy - 8*s)
        ]
        cr.move_to(*helmet_back[0])
        for point in helmet_back[1:]:
            cr.line_to(*point)
        cr.close_path()
        cr.fill()
        
        # Helmet panel lines
        cr.set_source_rgba(0.1, 0.1, 0.12, 0.6)
        cr.set_line_width(1*s)
        cr.move_to(cx - 15*s, cy - 20*s)
        cr.line_to(cx - 10*s, cy - 28*s)
        cr.move_to(cx + 15*s, cy - 20*s)
        cr.line_to(cx + 10*s, cy - 28*s)
        cr.stroke()
        
        # Side plates (darker red)
        cr.set_source_rgb(0.52, 0.07, 0.07)
        for side in [-1, 1]:
            plate = [
                (cx + side * 18*s, cy - 26*s),
                (cx + side * 20*s, cy - 8*s),
                (cx + side * 18*s, cy - 6*s),
                (cx + side * 14*s, cy - 20*s)
            ]
            cr.move_to(*plate[0])
            for point in plate[1:]:
                cr.line_to(*point)
            cr.close_path()
            cr.fill()
        
        # === FACEPLATE (gold, articulated) ===
        cr.set_source_rgb(0.82, 0.60, 0.14)
        
        # Upper faceplate
        face_upper = [
            (cx - 16*s, cy - 12*s - mask_lift),
            (cx - 12*s, cy - 24*s - mask_lift),
            (cx + 12*s, cy - 24*s - mask_lift),
            (cx + 16*s, cy - 12*s - mask_lift)
        ]
        cr.move_to(*face_upper[0])
        for point in face_upper[1:]:
            cr.line_to(*point)
        cr.close_path()
        cr.fill()
        
        # Metallic highlight on faceplate
        cr.set_source_rgba(1, 0.9, 0.5, 0.35)
        cr.move_to(cx - 10*s, cy - 22*s - mask_lift)
        cr.line_to(cx, cy - 23*s - mask_lift)
        cr.line_to(cx + 4*s, cy - 20*s - mask_lift)
        cr.line_to(cx - 2*s, cy - 18*s - mask_lift)
        cr.close_path()
        cr.fill()
        
        # Cheek guards
        for side in [-1, 1]:
            cheek = [
                (cx + side * 16*s, cy - 12*s - mask_lift),
                (cx + side * 18*s, cy - 6*s - mask_lift),
                (cx + side * 12*s, cy - 8*s - mask_lift)
            ]
            cr.move_to(*cheek[0])
            for point in cheek[1:]:
                cr.line_to(*point)
            cr.close_path()
            cr.fill()
        
        # Chin piece (movable with mask)
        chin_piece = [
            (cx - 10*s, cy - 8*s - mask_lift * 0.7),
            (cx - 8*s, cy - 4*s - mask_lift * 0.7),
            (cx + 8*s, cy - 4*s - mask_lift * 0.7),
            (cx + 10*s, cy - 8*s - mask_lift * 0.7)
        ]
        cr.move_to(*chin_piece[0])
        for point in chin_piece[1:]:
            cr.line_to(*point)
        cr.close_path()
        cr.fill()
        
        # === EYE SLITS (glowing) ===
        if self.mask_animation < 5:
            glow_pulse = 0.85 + math.sin(self.frame * 0.2) * 0.15
            
            for side in [-1, 1]:
                # Eye slit shape (triangular/angular)
                eye_points = [
                    (cx + side * 5*s, cy - 18*s - mask_lift),
                    (cx + side * 12*s, cy - 16*s - mask_lift),
                    (cx + side * 11*s, cy - 14*s - mask_lift),
                    (cx + side * 6*s, cy - 15*s - mask_lift)
                ]
                
                # Outer glow
                cr.set_source_rgba(0.7, 0.85, 1, 0.4 * glow_pulse)
                cr.move_to(*eye_points[0])
                for point in eye_points[1:]:
                    cr.line_to(*point)
                cr.close_path()
                cr.fill()
                
                # Bright core
                cr.set_source_rgba(0.85, 0.95, 1, glow_pulse)
                eye_core = [(x * 0.7 + cx * 0.3, y * 0.7 + (cy - 16*s - mask_lift) * 0.3) for x, y in eye_points]
                cr.move_to(*eye_core[0])
                for point in eye_core[1:]:
                    cr.line_to(*point)
                cr.close_path()
                cr.fill()
                
                # Hotspot
                cr.set_source_rgba(1, 1, 1, 0.9 * glow_pulse)
                cr.arc(cx + side * 8*s, cy - 16*s - mask_lift, 1.5*s, 0, 2*math.pi)
                cr.fill()
        else:
            # Face visible behind mask
            cr.set_source_rgb(0.88, 0.76, 0.66)
            cr.arc(cx, cy - 15*s, 10*s, 0, 2*math.pi)
            cr.fill()
            # Eyes
            cr.set_source_rgb(0.15, 0.1, 0.08)
            cr.arc(cx - 4*s, cy - 17*s, 1.5*s, 0, 2*math.pi)
            cr.arc(cx + 4*s, cy - 17*s, 1.5*s, 0, 2*math.pi)
            cr.fill()
            # Mouth
            cr.set_line_width(1*s)
            cr.move_to(cx - 3*s, cy - 12*s)
            cr.line_to(cx + 3*s, cy - 12*s)
            cr.stroke()
        
        # Panel separation lines on helmet
        cr.set_source_rgba(0.08, 0.08, 0.1, 0.7)
        cr.set_line_width(0.8*s)
        cr.move_to(cx, cy - 32*s)
        cr.line_to(cx, cy - 8*s)
        cr.move_to(cx - 12*s, cy - 24*s - mask_lift)
        cr.line_to(cx + 12*s, cy - 24*s - mask_lift)
        cr.stroke()
    
    def _draw_ironman_arms(self, cr, cx, cy, s):
        """Draw realistic Iron Man arms with detailed armor plating"""
        # Calculate arm angles
        left_angle = 0
        right_angle = 0
        left_length = 20*s
        right_length = 20*s
        
        if self.state == self.FIRING:
            right_angle = -0.7
            right_length = 24*s
            self.repulsor_charge = min(self.repulsor_charge + 1, 10)
        elif self.state == self.CHARGING:
            left_angle = -0.5
            right_angle = -0.5
            left_length = 22*s
            right_length = 22*s
            self.repulsor_charge = min(self.repulsor_charge + 0.5, 10)
        elif self.state == self.FLYING:
            left_angle = -0.2
            right_angle = -0.2
        elif self.state == self.LANDING:
            left_angle = 0.4
            right_angle = 0.4
        elif self.state == self.WAVING:
            right_angle = -0.8 + math.sin(self.frame * 0.3) * 0.4
            right_length = 22*s
        elif self.state == self.WORKING:
            left_angle = 0.5 + math.sin(self.frame * 0.4) * 0.1
            right_angle = 0.5 + math.cos(self.frame * 0.4) * 0.1
        else:
            self.repulsor_charge = max(self.repulsor_charge - 0.3, 0)
        
        # === LEFT ARM ===
        arm_start_x = cx - 25*s
        arm_start_y = cy - 5*s
        
        # Bicep armor (red, angular)
        cr.set_source_rgb(0.6, 0.09, 0.09)
        upper_end_x = arm_start_x - math.cos(left_angle) * (left_length * 0.45)
        upper_end_y = arm_start_y + math.sin(left_angle + 0.5) * (left_length * 0.45)
        
        cr.save()
        cr.translate(arm_start_x, arm_start_y)
        cr.rotate(left_angle + 0.5)
        # Upper bicep plate
        bicep_shape = [(-5*s, 0), (-5*s, left_length * 0.2), (-3*s, left_length * 0.4), (3*s, left_length * 0.4), (5*s, left_length * 0.2), (5*s, 0)]
        cr.move_to(*bicep_shape[0])
        for point in bicep_shape[1:]:
            cr.line_to(*point)
        cr.close_path()
        cr.fill()
        # Highlight
        cr.set_source_rgba(0.85, 0.2, 0.15, 0.3)
        cr.move_to(-4*s, 1*s)
        cr.line_to(-2*s, left_length * 0.3)
        cr.line_to(1*s, left_length * 0.35)
        cr.stroke()
        cr.restore()
        
        # Elbow joint (gold, mechanical)
        cr.set_source_rgb(0.78, 0.55, 0.12)
        cr.arc(upper_end_x, upper_end_y, 3.5*s, 0, 2*math.pi)
        cr.fill()
        # Joint detail
        cr.set_source_rgba(0.3, 0.32, 0.35, 0.7)
        cr.set_line_width(0.8*s)
        cr.arc(upper_end_x, upper_end_y, 2.5*s, 0, 2*math.pi)
        cr.stroke()
        
        # Forearm armor (darker red)
        cr.set_source_rgb(0.55, 0.08, 0.08)
        forearm_end_x = arm_start_x - math.cos(left_angle + 0.1) * left_length
        forearm_end_y = arm_start_y + math.sin(left_angle + 0.6) * left_length
        
        cr.save()
        cr.translate(upper_end_x, upper_end_y)
        cr.rotate(left_angle + 0.6)
        # Forearm segments
        segment_length = left_length * 0.5
        forearm_shape = [(-4*s, 0), (-4*s, segment_length * 0.6), (-3*s, segment_length), (3*s, segment_length), (4*s, segment_length * 0.6), (4*s, 0)]
        cr.move_to(*forearm_shape[0])
        for point in forearm_shape[1:]:
            cr.line_to(*point)
        cr.close_path()
        cr.fill()
        # Panel lines
        cr.set_source_rgba(0.1, 0.1, 0.12, 0.6)
        cr.set_line_width(0.8*s)
        cr.move_to(-3*s, segment_length * 0.3)
        cr.line_to(3*s, segment_length * 0.3)
        cr.move_to(-3*s, segment_length * 0.6)
        cr.line_to(3*s, segment_length * 0.6)
        cr.stroke()
        cr.restore()
        
        # Repulsor gauntlet (gold, detailed)
        cr.set_source_rgb(0.82, 0.60, 0.14)
        cr.save()
        cr.translate(forearm_end_x, forearm_end_y)
        cr.rotate(left_angle + 0.5)
        # Gauntlet housing
        gauntlet = [(-5*s, -3*s), (-4*s, 0), (-3*s, 4*s), (3*s, 4*s), (4*s, 0), (5*s, -3*s)]
        cr.move_to(*gauntlet[0])
        for point in gauntlet[1:]:
            cr.line_to(*point)
        cr.close_path()
        cr.fill()
        # Repulsor emitter ring
        cr.set_source_rgb(0.35, 0.38, 0.42)
        cr.arc(0, 2*s, 3*s, 0, 2*math.pi)
        cr.fill()
        # Repulsor core
        cr.set_source_rgb(0.4, 0.65, 0.95)
        cr.arc(0, 2*s, 2*s, 0, 2*math.pi)
        cr.fill()
        cr.restore()
        
        # === RIGHT ARM (mirror) ===
        arm_start_x = cx + 25*s
        
        # Bicep armor
        cr.set_source_rgb(0.6, 0.09, 0.09)
        upper_end_x = arm_start_x + math.cos(right_angle) * (right_length * 0.45)
        upper_end_y = arm_start_y + math.sin(right_angle + 0.5) * (right_length * 0.45)
        
        cr.save()
        cr.translate(arm_start_x, arm_start_y)
        cr.rotate(-(right_angle + 0.5))
        mirrored_bicep = [(-x, y) for x, y in bicep_shape]
        cr.move_to(*mirrored_bicep[0])
        for point in mirrored_bicep[1:]:
            cr.line_to(*point)
        cr.close_path()
        cr.fill()
        cr.set_source_rgba(0.85, 0.2, 0.15, 0.3)
        cr.move_to(4*s, 1*s)
        cr.line_to(2*s, right_length * 0.3)
        cr.line_to(-1*s, right_length * 0.35)
        cr.stroke()
        cr.restore()
        
        # Elbow
        cr.set_source_rgb(0.78, 0.55, 0.12)
        cr.arc(upper_end_x, upper_end_y, 3.5*s, 0, 2*math.pi)
        cr.fill()
        cr.set_source_rgba(0.3, 0.32, 0.35, 0.7)
        cr.set_line_width(0.8*s)
        cr.arc(upper_end_x, upper_end_y, 2.5*s, 0, 2*math.pi)
        cr.stroke()
        
        # Forearm
        cr.set_source_rgb(0.55, 0.08, 0.08)
        forearm_end_x = arm_start_x + math.cos(right_angle + 0.1) * right_length
        forearm_end_y = arm_start_y + math.sin(right_angle + 0.6) * right_length
        
        cr.save()
        cr.translate(upper_end_x, upper_end_y)
        cr.rotate(-(right_angle + 0.6))
        mirrored_forearm = [(-x, y) for x, y in forearm_shape]
        cr.move_to(*mirrored_forearm[0])
        for point in mirrored_forearm[1:]:
            cr.line_to(*point)
        cr.close_path()
        cr.fill()
        cr.set_source_rgba(0.1, 0.1, 0.12, 0.6)
        cr.set_line_width(0.8*s)
        cr.move_to(-3*s, segment_length * 0.3)
        cr.line_to(3*s, segment_length * 0.3)
        cr.move_to(-3*s, segment_length * 0.6)
        cr.line_to(3*s, segment_length * 0.6)
        cr.stroke()
        cr.restore()
        
        # Repulsor gauntlet
        cr.set_source_rgb(0.82, 0.60, 0.14)
        cr.save()
        cr.translate(forearm_end_x, forearm_end_y)
        cr.rotate(-(right_angle + 0.5))
        mirrored_gauntlet = [(-x, y) for x, y in gauntlet]
        cr.move_to(*mirrored_gauntlet[0])
        for point in mirrored_gauntlet[1:]:
            cr.line_to(*point)
        cr.close_path()
        cr.fill()
        cr.set_source_rgb(0.35, 0.38, 0.42)
        cr.arc(0, 2*s, 3*s, 0, 2*math.pi)
        cr.fill()
        cr.set_source_rgb(0.4, 0.65, 0.95)
        cr.arc(0, 2*s, 2*s, 0, 2*math.pi)
        cr.fill()
        cr.restore()
    
    def _draw_ironman_legs(self, cr, cx, cy, s):
        """Draw realistic Iron Man legs with armor plating"""
        leg_y = cy + 18*s
        
        # Calculate leg positions
        left_offset = 0
        right_offset = 0
        left_angle = 0
        right_angle = 0
        
        if self.state == self.RUNNING:
            left_offset = math.sin(self.frame * 0.3) * 5*s
            right_offset = -math.sin(self.frame * 0.3) * 5*s
            left_angle = math.sin(self.frame * 0.3) * 0.2
            right_angle = -math.sin(self.frame * 0.3) * 0.2
        elif self.state in [self.FLYING, self.LANDING]:
            # Legs together for flight/landing
            left_angle = 0.1
            right_angle = 0.1
        
        # === LEFT LEG ===
        leg_x = cx - 10*s
        
        # Thigh armor (red, angular plates)
        cr.set_source_rgb(0.6, 0.09, 0.09)
        cr.save()
        cr.translate(leg_x, leg_y)
        cr.rotate(left_angle)
        # Thigh plates (front and side)
        thigh_front = [(-4.5*s, 0), (-5*s, 5*s), (-4*s, 13*s), (4*s, 13*s), (5*s, 5*s), (4.5*s, 0)]
        cr.move_to(*thigh_front[0])
        for point in thigh_front[1:]:
            cr.line_to(*point)
        cr.close_path()
        cr.fill()
        # Highlight
        cr.set_source_rgba(0.85, 0.2, 0.15, 0.28)
        cr.move_to(-3*s, 2*s)
        cr.line_to(-2*s, 10*s)
        cr.line_to(1*s, 12*s)
        cr.stroke()
        # Panel line
        cr.set_source_rgba(0.1, 0.1, 0.12, 0.6)
        cr.set_line_width(0.8*s)
        cr.move_to(-3*s, 6*s)
        cr.line_to(3*s, 6*s)
        cr.stroke()
        cr.restore()
        
        # Knee joint (gold, mechanical)
        knee_x = leg_x + left_offset * 0.3
        knee_y = leg_y + 13*s
        cr.set_source_rgb(0.78, 0.55, 0.12)
        cr.arc(knee_x, knee_y, 3.5*s, 0, 2*math.pi)
        cr.fill()
        # Joint ring detail
        cr.set_source_rgba(0.3, 0.32, 0.35, 0.7)
        cr.set_line_width(0.8*s)
        cr.arc(knee_x, knee_y, 2.5*s, 0, 2*math.pi)
        cr.stroke()
        
        # Shin armor (darker red)
        cr.set_source_rgb(0.55, 0.08, 0.08)
        cr.save()
        cr.translate(knee_x, knee_y)
        cr.rotate(left_angle * 0.5)
        shin_shape = [(-3.5*s, 0), (-4*s, 5*s), (-3.5*s, 12*s), (3.5*s, 12*s), (4*s, 5*s), (3.5*s, 0)]
        cr.move_to(*shin_shape[0])
        for point in shin_shape[1:]:
            cr.line_to(*point)
        cr.close_path()
        cr.fill()
        # Shin panel lines
        cr.set_source_rgba(0.1, 0.1, 0.12, 0.6)
        cr.set_line_width(0.7*s)
        cr.move_to(-3*s, 4*s)
        cr.line_to(3*s, 4*s)
        cr.move_to(-3*s, 8*s)
        cr.line_to(3*s, 8*s)
        cr.stroke()
        cr.restore()
        
        # Boot (gold armor with thruster)
        boot_x = leg_x + left_offset
        boot_y = leg_y + 25*s
        cr.set_source_rgb(0.82, 0.60, 0.14)
        cr.save()
        cr.translate(boot_x, boot_y)
        # Boot housing (angular)
        boot_shape = [(-5*s, 0), (-5.5*s, 3*s), (-4.5*s, 7*s), (4.5*s, 7*s), (5.5*s, 3*s), (5*s, 0)]
        cr.move_to(*boot_shape[0])
        for point in boot_shape[1:]:
            cr.line_to(*point)
        cr.close_path()
        cr.fill()
        # Metallic highlight
        cr.set_source_rgba(1, 0.85, 0.45, 0.35)
        cr.move_to(-3*s, 1*s)
        cr.line_to(-2*s, 5*s)
        cr.line_to(1*s, 6*s)
        cr.stroke()
        # Thruster opening (circular)
        cr.set_source_rgb(0.25, 0.28, 0.32)
        cr.arc(0, 7*s, 3.5*s, 0, 2*math.pi)
        cr.fill()
        # Inner thruster ring
        cr.set_source_rgb(0.35, 0.38, 0.42)
        cr.arc(0, 7*s, 2.5*s, 0, 2*math.pi)
        cr.fill()
        cr.restore()
        
        # === RIGHT LEG (mirror) ===
        leg_x = cx + 10*s
        
        # Thigh armor
        cr.set_source_rgb(0.6, 0.09, 0.09)
        cr.save()
        cr.translate(leg_x, leg_y)
        cr.rotate(right_angle)
        mirrored_thigh = [(-x, y) for x, y in thigh_front]
        cr.move_to(*mirrored_thigh[0])
        for point in mirrored_thigh[1:]:
            cr.line_to(*point)
        cr.close_path()
        cr.fill()
        cr.set_source_rgba(0.85, 0.2, 0.15, 0.28)
        cr.move_to(3*s, 2*s)
        cr.line_to(2*s, 10*s)
        cr.line_to(-1*s, 12*s)
        cr.stroke()
        cr.set_source_rgba(0.1, 0.1, 0.12, 0.6)
        cr.set_line_width(0.8*s)
        cr.move_to(-3*s, 6*s)
        cr.line_to(3*s, 6*s)
        cr.stroke()
        cr.restore()
        
        # Knee joint
        knee_x = leg_x + right_offset * 0.3
        cr.set_source_rgb(0.78, 0.55, 0.12)
        cr.arc(knee_x, knee_y, 3.5*s, 0, 2*math.pi)
        cr.fill()
        cr.set_source_rgba(0.3, 0.32, 0.35, 0.7)
        cr.set_line_width(0.8*s)
        cr.arc(knee_x, knee_y, 2.5*s, 0, 2*math.pi)
        cr.stroke()
        
        # Shin armor
        cr.set_source_rgb(0.55, 0.08, 0.08)
        cr.save()
        cr.translate(knee_x, knee_y)
        cr.rotate(right_angle * 0.5)
        mirrored_shin = [(-x, y) for x, y in shin_shape]
        cr.move_to(*mirrored_shin[0])
        for point in mirrored_shin[1:]:
            cr.line_to(*point)
        cr.close_path()
        cr.fill()
        cr.set_source_rgba(0.1, 0.1, 0.12, 0.6)
        cr.set_line_width(0.7*s)
        cr.move_to(-3*s, 4*s)
        cr.line_to(3*s, 4*s)
        cr.move_to(-3*s, 8*s)
        cr.line_to(3*s, 8*s)
        cr.stroke()
        cr.restore()
        
        # Boot
        boot_x = leg_x + right_offset
        cr.set_source_rgb(0.82, 0.60, 0.14)
        cr.save()
        cr.translate(boot_x, boot_y)
        mirrored_boot = [(-x, y) for x, y in boot_shape]
        cr.move_to(*mirrored_boot[0])
        for point in mirrored_boot[1:]:
            cr.line_to(*point)
        cr.close_path()
        cr.fill()
        cr.set_source_rgba(1, 0.85, 0.45, 0.35)
        cr.move_to(3*s, 1*s)
        cr.line_to(2*s, 5*s)
        cr.line_to(-1*s, 6*s)
        cr.stroke()
        cr.set_source_rgb(0.25, 0.28, 0.32)
        cr.arc(0, 7*s, 3.5*s, 0, 2*math.pi)
        cr.fill()
        cr.set_source_rgb(0.35, 0.38, 0.42)
        cr.arc(0, 7*s, 2.5*s, 0, 2*math.pi)
        cr.fill()
        cr.restore()
    
    def _draw_ironman_effects(self, cr, cx, cy, s):
        """Draw Iron Man special effects: repulsor blasts, flight flames, etc."""
        # === BOOT THRUSTERS (when flying) ===
        if self.state in [self.FLYING, self.LANDING, self.JUMPING]:
            flame_intensity = abs(math.sin(self.frame * 0.25))
            
            for leg_offset in [-10*s, 10*s]:
                boot_x = cx + leg_offset
                boot_y = cy + 42*s
                
                # Flame layers
                for i in range(3):
                    alpha = 0.7 - i * 0.2
                    flame_length = (6 + i * 3) * s * (0.7 + flame_intensity * 0.3)
                    
                    cr.set_source_rgba(1, 0.5, 0.1, alpha)
                    cr.save()
                    cr.translate(boot_x, boot_y)
                    cr.move_to(-1.5*s, 0)
                    cr.curve_to(-2*s, flame_length * 0.5, -1*s, flame_length * 0.8, 0, flame_length)
                    cr.curve_to(1*s, flame_length * 0.8, 2*s, flame_length * 0.5, 1.5*s, 0)
                    cr.close_path()
                    cr.fill()
                    cr.restore()
                
                # Bright core
                cr.set_source_rgba(1, 1, 0.8, 0.9)
                cr.arc(boot_x, boot_y + 2*s, 1.5*s, 0, 2*math.pi)
                cr.fill()
        
        # === HAND STABILIZERS (when flying) ===
        if self.state == self.FLYING:
            for hand_x in [cx - 42*s, cx + 42*s]:
                hand_y = cy + 15*s
                
                # Small flames
                cr.set_source_rgba(1, 0.6, 0.2, 0.6)
                cr.save()
                cr.translate(hand_x, hand_y)
                cr.move_to(-1*s, 0)
                cr.curve_to(-1*s, 4*s, -0.5*s, 5*s, 0, 6*s)
                cr.curve_to(0.5*s, 5*s, 1*s, 4*s, 1*s, 0)
                cr.close_path()
                cr.fill()
                cr.restore()
        
        # === REPULSOR BLASTS ===
        if self.repulsor_charge > 3:
            # Calculate hand positions
            if self.state == self.FIRING:
                # Right hand blast
                hand_x = cx + 24*s + math.cos(-0.7) * 22*s
                hand_y = cy + 15*s
                
                # Charge glow
                glow_size = self.repulsor_charge * 0.8 * s
                cr.set_source_rgba(0.5, 0.8, 1, 0.6)
                cr.arc(hand_x, hand_y, glow_size, 0, 2*math.pi)
                cr.fill()
                
                # Blast beam
                if self.repulsor_charge > 7:
                    cr.set_source_rgba(0.7, 0.9, 1, 0.8)
                    cr.set_line_width(4*s)
                    cr.move_to(hand_x, hand_y)
                    cr.line_to(hand_x + 40*s, hand_y - 20*s)
                    cr.stroke()
                    
                    # Bright core
                    cr.set_source_rgba(1, 1, 1, 0.9)
                    cr.set_line_width(2*s)
                    cr.move_to(hand_x, hand_y)
                    cr.line_to(hand_x + 40*s, hand_y - 20*s)
                    cr.stroke()
                    
                    # Impact burst
                    burst_x = hand_x + 40*s
                    burst_y = hand_y - 20*s
                    for i in range(6):
                        angle = i * math.pi / 3 + self.frame * 0.1
                        cr.set_source_rgba(0.8, 0.9, 1, 0.6)
                        cr.move_to(burst_x, burst_y)
                        cr.line_to(burst_x + math.cos(angle) * 8*s, burst_y + math.sin(angle) * 8*s)
                        cr.stroke()
            
            elif self.state == self.CHARGING:
                # Both hands charging
                for hand_offset in [-46*s, 46*s]:
                    hand_x = cx + hand_offset
                    hand_y = cy
                    
                    # Pulsing glow
                    pulse = abs(math.sin(self.frame * 0.3))
                    glow_size = (self.repulsor_charge * 0.5 + pulse * 2) * s
                    cr.set_source_rgba(0.5, 0.8, 1, 0.5)
                    cr.arc(hand_x, hand_y, glow_size, 0, 2*math.pi)
                    cr.fill()
                    
                    # Particles
                    for i in range(4):
                        particle_angle = i * math.pi / 2 + self.frame * 0.1
                        particle_dist = (8 + math.sin(self.frame * 0.2 + i) * 3) * s
                        px = hand_x + math.cos(particle_angle) * particle_dist
                        py = hand_y + math.sin(particle_angle) * particle_dist
                        cr.set_source_rgba(0.7, 0.9, 1, 0.7)
                        cr.arc(px, py, 1*s, 0, 2*math.pi)
                        cr.fill()
        
        # === LANDING IMPACT ===
        if self.state == self.LANDING:
            impact_frame = self.frame % 40
            if impact_frame < 15:
                # Shockwave rings
                ring_radius = impact_frame * 3 * s
                cr.set_source_rgba(0.8, 0.8, 0.9, 0.5 - impact_frame * 0.03)
                cr.set_line_width(2*s)
                cr.arc(cx, cy + 50*s, ring_radius, 0, 2*math.pi)
                cr.stroke()
                
                # Dust particles
                for i in range(8):
                    angle = i * math.pi / 4
                    dist = impact_frame * 2 * s
                    px = cx + math.cos(angle) * dist
                    py = cy + 50*s
                    cr.set_source_rgba(0.6, 0.6, 0.6, 0.4 - impact_frame * 0.02)
                    cr.arc(px, py, 2*s, 0, 2*math.pi)
                    cr.fill()
    
    def _draw_astronaut_arms(self, cr, cx, cy, s):
        """Draw detailed astronaut spacesuit arms"""
        # Calculate arm positions based on state
        left_arm_angle = 0
        left_arm_length = 15*s
        right_arm_angle = 0
        right_arm_length = 15*s
        
        if self.state == self.WAVING:
            right_arm_angle = -0.8 + math.sin(self.frame * 0.3) * 0.4
            right_arm_length = 20*s
        elif self.state == self.WORKING:
            left_arm_angle = 0.5 + math.sin(self.frame * 0.4) * 0.1
            right_arm_angle = 0.5 + math.cos(self.frame * 0.4) * 0.1
        elif self.state == self.THINKING or self.state == self.CONFUSED:
            right_arm_angle = -0.3
            right_arm_length = 18*s
        elif self.state == self.RUNNING:
            left_arm_angle = math.sin(self.frame * 0.3) * 0.5
            right_arm_angle = -math.sin(self.frame * 0.3) * 0.5
        elif self.state == self.CELEBRATING or self.state == self.EXCITED:
            left_arm_angle = -0.8 + math.sin(self.frame * 0.2) * 0.2
            right_arm_angle = -0.8 + math.cos(self.frame * 0.2) * 0.2
            left_arm_length = 20*s
            right_arm_length = 20*s
        elif self.state == self.SLEEPING or self.state == self.TIRED:
            left_arm_angle = 0.8
            right_arm_angle = 0.8
        elif self.state == self.ANGRY:
            left_arm_angle = 0.6
            right_arm_angle = 0.6
            left_arm_length = 18*s
            right_arm_length = 18*s
        elif self.state == self.CRYING or self.state == self.SAD:
            left_arm_angle = 0.9
            right_arm_angle = 0.9
        elif self.state == self.SHOCKED:
            left_arm_angle = -0.5
            right_arm_angle = -0.5
            left_arm_length = 18*s
            right_arm_length = 18*s
        elif self.state == self.DANCING:
            left_arm_angle = -0.5 + math.sin(self.frame * 0.4) * 0.6
            right_arm_angle = -0.5 + math.cos(self.frame * 0.4) * 0.6
            left_arm_length = 18*s
            right_arm_length = 18*s
        elif self.state == self.MEDITATING:
            left_arm_angle = 0.3
            right_arm_angle = 0.3
        elif self.state == self.LAUGHING:
            left_arm_angle = 0.4
            right_arm_angle = 0.4
        
        # === LEFT ARM ===
        arm_start_x = cx - 22*s
        arm_start_y = cy + 5*s
        
        # Upper arm segment
        upper_arm_end_x = arm_start_x - math.cos(left_arm_angle) * (left_arm_length * 0.55)
        upper_arm_end_y = arm_start_y + math.sin(left_arm_angle + 0.5) * (left_arm_length * 0.55)
        
        cr.set_source_rgb(0.85, 0.87, 0.90)
        cr.save()
        cr.translate(arm_start_x, arm_start_y)
        cr.rotate(left_arm_angle + 0.5)
        self._draw_rounded_rect_shape(cr, -4*s, 0, 8*s, left_arm_length * 0.5, 2*s)
        cr.fill()
        cr.restore()
        
        # Elbow joint
        cr.set_source_rgb(0.5, 0.52, 0.55)
        cr.arc(upper_arm_end_x, upper_arm_end_y, 3*s, 0, 2*math.pi)
        cr.fill()
        
        # Forearm segment
        forearm_end_x = arm_start_x - math.cos(left_arm_angle) * left_arm_length
        forearm_end_y = arm_start_y + math.sin(left_arm_angle + 0.5) * left_arm_length
        
        cr.set_source_rgb(0.82, 0.85, 0.88)
        cr.save()
        cr.translate(upper_arm_end_x, upper_arm_end_y)
        cr.rotate(left_arm_angle + 0.6)
        self._draw_rounded_rect_shape(cr, -3.5*s, 0, 7*s, left_arm_length * 0.5, 2*s)
        cr.fill()
        cr.restore()
        
        # Glove (hand)
        cr.set_source_rgb(0.75, 0.78, 0.82)
        cr.save()
        cr.translate(forearm_end_x, forearm_end_y)
        cr.rotate(left_arm_angle + 0.5)
        # Palm
        cr.arc(0, 0, 4*s, 0, 2*math.pi)
        cr.fill()
        # Fingers (simplified)
        for i in range(3):
            finger_angle = (i - 1) * 0.3
            cr.save()
            cr.rotate(finger_angle)
            cr.rectangle(-1*s, 0, 2*s, 3*s)
            cr.fill()
            cr.restore()
        cr.restore()
        
        # Arm panel details
        cr.set_source_rgba(0.3, 0.35, 0.4, 0.3)
        cr.set_line_width(1*s)
        cr.move_to(arm_start_x - 2*s, arm_start_y + 3*s)
        cr.line_to(upper_arm_end_x + 2*s, upper_arm_end_y - 2*s)
        cr.stroke()
        
        # === RIGHT ARM ===
        arm_start_x = cx + 22*s
        
        # Upper arm segment
        upper_arm_end_x = arm_start_x + math.cos(right_arm_angle) * (right_arm_length * 0.55)
        upper_arm_end_y = arm_start_y + math.sin(right_arm_angle + 0.5) * (right_arm_length * 0.55)
        
        cr.set_source_rgb(0.85, 0.87, 0.90)
        cr.save()
        cr.translate(arm_start_x, arm_start_y)
        cr.rotate(-(right_arm_angle + 0.5))
        self._draw_rounded_rect_shape(cr, -4*s, 0, 8*s, right_arm_length * 0.5, 2*s)
        cr.fill()
        cr.restore()
        
        # Elbow joint
        cr.set_source_rgb(0.5, 0.52, 0.55)
        cr.arc(upper_arm_end_x, upper_arm_end_y, 3*s, 0, 2*math.pi)
        cr.fill()
        
        # Forearm segment
        forearm_end_x = arm_start_x + math.cos(right_arm_angle) * right_arm_length
        forearm_end_y = arm_start_y + math.sin(right_arm_angle + 0.5) * right_arm_length
        
        cr.set_source_rgb(0.82, 0.85, 0.88)
        cr.save()
        cr.translate(upper_arm_end_x, upper_arm_end_y)
        cr.rotate(-(right_arm_angle + 0.6))
        self._draw_rounded_rect_shape(cr, -3.5*s, 0, 7*s, right_arm_length * 0.5, 2*s)
        cr.fill()
        cr.restore()
        
        # Glove (hand)
        cr.set_source_rgb(0.75, 0.78, 0.82)
        cr.save()
        cr.translate(forearm_end_x, forearm_end_y)
        cr.rotate(-(right_arm_angle + 0.5))
        # Palm
        cr.arc(0, 0, 4*s, 0, 2*math.pi)
        cr.fill()
        # Fingers (simplified)
        for i in range(3):
            finger_angle = (i - 1) * 0.3
            cr.save()
            cr.rotate(-finger_angle)
            cr.rectangle(-1*s, 0, 2*s, 3*s)
            cr.fill()
            cr.restore()
        cr.restore()
        
        # Arm panel details
        cr.set_source_rgba(0.3, 0.35, 0.4, 0.3)
        cr.set_line_width(1*s)
        cr.move_to(arm_start_x + 2*s, arm_start_y + 3*s)
        cr.line_to(upper_arm_end_x - 2*s, upper_arm_end_y - 2*s)
        cr.stroke()
    
    def _draw_astronaut_legs(self, cr, cx, cy, s):
        """Draw detailed astronaut spacesuit legs with boots"""
        leg_y = cy + 20*s
        
        # Calculate leg positions based on state
        left_offset = 0
        right_offset = 0
        left_angle = 0
        right_angle = 0
        
        if self.state == self.RUNNING:
            left_offset = math.sin(self.frame * 0.3) * 8*s
            right_offset = -math.sin(self.frame * 0.3) * 8*s
            left_angle = math.sin(self.frame * 0.3) * 0.3
            right_angle = -math.sin(self.frame * 0.3) * 0.3
        elif self.state == self.JUMPING:
            left_angle = -0.2
            right_angle = -0.2
        
        # === LEFT LEG ===
        leg_start_x = cx - 10*s
        
        # Upper leg (thigh)
        cr.set_source_rgb(0.80, 0.83, 0.86)
        cr.save()
        cr.translate(leg_start_x, leg_y)
        cr.rotate(left_angle)
        self._draw_rounded_rect_shape(cr, -4*s, 0, 8*s, 14*s, 2*s)
        cr.fill()
        cr.restore()
        
        # Knee joint
        knee_x = leg_start_x + left_offset * 0.5
        knee_y = leg_y + 14*s
        cr.set_source_rgb(0.5, 0.52, 0.55)
        cr.arc(knee_x, knee_y, 3*s, 0, 2*math.pi)
        cr.fill()
        
        # Lower leg (shin)
        cr.set_source_rgb(0.85, 0.87, 0.90)
        cr.save()
        cr.translate(knee_x, knee_y)
        cr.rotate(left_angle * 0.5)
        self._draw_rounded_rect_shape(cr, -3.5*s, 0, 7*s, 12*s, 2*s)
        cr.fill()
        cr.restore()
        
        # Boot
        boot_x = leg_start_x + left_offset
        boot_y = leg_y + 26*s
        cr.set_source_rgb(0.65, 0.68, 0.72)
        # Boot upper
        cr.save()
        cr.translate(boot_x, boot_y)
        cr.rectangle(-4.5*s, 0, 9*s, 6*s)
        cr.fill()
        # Boot sole (thick)
        cr.set_source_rgb(0.35, 0.38, 0.42)
        cr.rectangle(-5*s, 6*s, 10*s, 3*s)
        cr.fill()
        # Boot toe
        cr.set_source_rgb(0.65, 0.68, 0.72)
        cr.move_to(-5*s, 6*s)
        cr.line_to(-6*s, 8*s)
        cr.line_to(6*s, 8*s)
        cr.line_to(5*s, 6*s)
        cr.close_path()
        cr.fill()
        cr.restore()
        
        # Boot details (laces/straps)
        cr.set_source_rgba(0.3, 0.35, 0.4, 0.5)
        cr.set_line_width(1*s)
        for i in range(2):
            cr.move_to(boot_x - 3*s, boot_y + 2*s + i * 2*s)
            cr.line_to(boot_x + 3*s, boot_y + 2*s + i * 2*s)
            cr.stroke()
        
        # === RIGHT LEG ===
        leg_start_x = cx + 10*s
        
        # Upper leg (thigh)
        cr.set_source_rgb(0.80, 0.83, 0.86)
        cr.save()
        cr.translate(leg_start_x, leg_y)
        cr.rotate(right_angle)
        self._draw_rounded_rect_shape(cr, -4*s, 0, 8*s, 14*s, 2*s)
        cr.fill()
        cr.restore()
        
        # Knee joint
        knee_x = leg_start_x + right_offset * 0.5
        knee_y = leg_y + 14*s
        cr.set_source_rgb(0.5, 0.52, 0.55)
        cr.arc(knee_x, knee_y, 3*s, 0, 2*math.pi)
        cr.fill()
        
        # Lower leg (shin)
        cr.set_source_rgb(0.85, 0.87, 0.90)
        cr.save()
        cr.translate(knee_x, knee_y)
        cr.rotate(right_angle * 0.5)
        self._draw_rounded_rect_shape(cr, -3.5*s, 0, 7*s, 12*s, 2*s)
        cr.fill()
        cr.restore()
        
        # Boot
        boot_x = leg_start_x + right_offset
        boot_y = leg_y + 26*s
        cr.set_source_rgb(0.65, 0.68, 0.72)
        # Boot upper
        cr.save()
        cr.translate(boot_x, boot_y)
        cr.rectangle(-4.5*s, 0, 9*s, 6*s)
        cr.fill()
        # Boot sole (thick)
        cr.set_source_rgb(0.35, 0.38, 0.42)
        cr.rectangle(-5*s, 6*s, 10*s, 3*s)
        cr.fill()
        # Boot toe
        cr.set_source_rgb(0.65, 0.68, 0.72)
        cr.move_to(-5*s, 6*s)
        cr.line_to(-6*s, 8*s)
        cr.line_to(6*s, 8*s)
        cr.line_to(5*s, 6*s)
        cr.close_path()
        cr.fill()
        cr.restore()
        
        # Boot details (laces/straps)
        cr.set_source_rgba(0.3, 0.35, 0.4, 0.5)
        cr.set_line_width(1*s)
        for i in range(2):
            cr.move_to(boot_x - 3*s, boot_y + 2*s + i * 2*s)
            cr.line_to(boot_x + 3*s, boot_y + 2*s + i * 2*s)
            cr.stroke()
    
    def _draw_legs(self, cr, cx, cy, s, color):
        """Draw legs with animation"""
        cr.set_source_rgb(*[c * 0.85 for c in color])
        cr.set_line_width(8*s)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        
        leg_y = cy + 25*s
        leg_length = 12*s
        
        left_offset = 0
        right_offset = 0
        
        if self.state == self.RUNNING:
            left_offset = math.sin(self.frame * 0.3) * 8*s
            right_offset = -math.sin(self.frame * 0.3) * 8*s
        elif self.state == self.JUMPING:
            # Legs together when jumping
            pass
        
        # Left leg
        cr.move_to(cx - 10*s, leg_y)
        cr.line_to(cx - 10*s + left_offset, leg_y + leg_length)
        cr.stroke()
        
        # Right leg
        cr.move_to(cx + 10*s, leg_y)
        cr.line_to(cx + 10*s + right_offset, leg_y + leg_length)
        cr.stroke()
    
    def _draw_state_effects(self, cr, cx, cy, s):
        """Draw extra effects based on state"""
        
        if self.state == self.THINKING or self.state == self.CONFUSED:
            # Question mark or thought bubble
            cr.set_source_rgba(0.3, 0.3, 0.3, 0.7)
            cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            cr.set_font_size(16*s)
            symbol = "?" if self.state == self.THINKING else "?"
            if self.state == self.CONFUSED:
                # Multiple question marks
                cr.move_to(cx + 18*s, cy - 30*s)
                cr.show_text("?")
                cr.move_to(cx + 25*s, cy - 25*s)
                cr.set_font_size(12*s)
                cr.show_text("?")
            else:
                cr.move_to(cx + 20*s, cy - 30*s)
                cr.show_text(symbol)
        
        elif self.state == self.SLEEPING or self.state == self.TIRED:
            # Zzz
            cr.set_source_rgba(0.3, 0.3, 0.3, 0.6)
            cr.select_font_face("Sans", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_BOLD)
            offset = math.sin(self.frame * 0.1) * 3
            cr.set_font_size(10*s)
            cr.move_to(cx + 15*s, cy - 20*s + offset)
            cr.show_text("z")
            cr.set_font_size(12*s)
            cr.move_to(cx + 22*s, cy - 28*s + offset)
            cr.show_text("z")
            cr.set_font_size(14*s)
            cr.move_to(cx + 30*s, cy - 38*s + offset)
            cr.show_text("Z")
        
        elif self.state == self.WORKING:
            # Little laptop/keyboard in front
            cr.set_source_rgba(0.3, 0.3, 0.4, 0.8)
            cr.rectangle(cx - 15*s, cy + 20*s, 30*s, 5*s)
            cr.fill()
            # Blinking cursor effect
            if self.frame % 20 < 10:
                cr.set_source_rgba(0.2, 0.8, 0.3, 0.8)
                cr.rectangle(cx - 12*s + (self.frame % 40) * 0.5*s, cy + 21*s, 2*s, 3*s)
                cr.fill()
        
        elif self.state == self.CELEBRATING or self.state == self.EXCITED:
            # Sparkles
            cr.set_source_rgba(1, 0.85, 0.2, 0.8)
            for i in range(3):
                angle = self.frame * 0.1 + i * 2.1
                dist = 35*s + math.sin(self.frame * 0.2 + i) * 5*s
                px = cx + math.cos(angle) * dist
                py = cy - 25*s + math.sin(angle) * dist * 0.3
                cr.arc(px, py, 2*s, 0, 2*math.pi)
                cr.fill()
        
        elif self.state == self.ANGRY:
            # Anger symbol (vein)
            cr.set_source_rgba(0.8, 0.1, 0.1, 0.8)
            cr.set_line_width(2*s)
            pulse = abs(math.sin(self.frame * 0.3))
            cr.move_to(cx + 22*s, cy - 15*s)
            cr.line_to(cx + 28*s, cy - 20*s)
            cr.line_to(cx + 25*s, cy - 12*s)
            cr.stroke()
            # Steam from head
            if self.frame % 15 < 8:
                cr.set_source_rgba(0.7, 0.7, 0.7, 0.5)
                offset = (self.frame % 15) * 2*s
                cr.arc(cx - 20*s, cy - 30*s - offset, 3*s, 0, 2*math.pi)
                cr.arc(cx + 20*s, cy - 30*s - offset, 3*s, 0, 2*math.pi)
                cr.fill()
        
        elif self.state == self.CRYING:
            # Extra tears
            cr.set_source_rgba(0.3, 0.5, 0.9, 0.6)
            for i in range(3):
                tear_y = cy + 15*s + (self.frame + i * 10) % 30 * 1*s
                cr.arc(cx - 10*s, tear_y, 2*s, 0, 2*math.pi)
                cr.arc(cx + 10*s, tear_y, 2*s, 0, 2*math.pi)
                cr.fill()
        
        elif self.state == self.SHOCKED:
            # Exclamation marks
            cr.set_source_rgba(0.9, 0.1, 0.1, 0.9)
            cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            cr.set_font_size(18*s)
            cr.move_to(cx - 25*s, cy - 25*s)
            cr.show_text("!")
            cr.move_to(cx + 20*s, cy - 25*s)
            cr.show_text("!")
        
        elif self.state == self.LAUGHING:
            # "Ha Ha" text
            cr.set_source_rgba(0.2, 0.2, 0.2, 0.5)
            cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            cr.set_font_size(10*s)
            offset = math.sin(self.frame * 0.2) * 2*s
            cr.move_to(cx + 20*s, cy - 20*s + offset)
            cr.show_text("Ha")
        
        elif self.state == self.MEDITATING:
            # Meditation aura
            cr.set_source_rgba(0.5, 0.8, 1.0, 0.3)
            aura_size = 35*s + math.sin(self.frame * 0.1) * 5*s
            cr.arc(cx, cy, aura_size, 0, 2*math.pi)
            cr.stroke()
            # Om symbol or lotus
            cr.set_source_rgba(0.6, 0.4, 0.8, 0.6)
            cr.arc(cx, cy - 40*s, 4*s, 0, 2*math.pi)
            cr.fill()
        
        elif self.state == self.DANCING:
            # Music notes
            cr.set_source_rgba(0.2, 0.2, 0.8, 0.7)
            cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            cr.set_font_size(14*s)
            note_offset = math.sin(self.frame * 0.2) * 5*s
            cr.move_to(cx - 25*s, cy - 30*s + note_offset)
            cr.show_text("♪")
            cr.move_to(cx + 20*s, cy - 25*s - note_offset)
            cr.show_text("♫")

