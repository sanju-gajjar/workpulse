"""
Character Module
Table-driven, multi-mascot, skeletal animation system
"""

import math
import random
import cairo
from dataclasses import dataclass, field
from enum import Enum, auto


# =======================
# STATE
# =======================

class State(Enum):
    IDLE = auto()
    THINKING = auto()
    WORKING = auto()
    RUNNING = auto()
    JUMPING = auto()
    WAVING = auto()
    # SLEEPING removed - not needed
    CELEBRATING = auto()
    EXCITED = auto()
    CONFUSED = auto()
    SHOCKED = auto()
    LAUGHING = auto()
    TIRED = auto()
    DANCING = auto()
    MEDITATING = auto()
    DRINKING = auto()
    HAPPY = auto()


# =======================
# SKELETON
# =======================

@dataclass
class Bone:
    name: str
    length: float
    angle: float = 0.0
    parent: str | None = None


@dataclass
class Skeleton:
    bones: dict[str, Bone]


# =======================
# MASCOT SPEC
# =======================

@dataclass(frozen=True)
class MascotSpec:
    # colors
    body_idle: tuple
    body_working: tuple
    body_paused: tuple
    ear_inner: tuple = (0.9, 0.6, 0.7, 0.6)
    eye_white: tuple = (1, 1, 1)
    eye_black: tuple = (0.1, 0.1, 0.1)

    # geometry
    body_radius: float = 25
    body_scale_x: float = 1.2

    ear_radius: float = 18
    ear_offset: tuple = (20, -8)

    leg_size: tuple = (10, 20)
    leg_offsets: tuple = ((-18, 0), (8, 0))

    trunk: bool = True
    tail: bool = False

    skeleton: Skeleton | None = None


# =======================
# MASCOTS
# =======================

ELEPHANT_SKELETON = Skeleton(bones={
    "ear_l": Bone("ear_l", 8),
    "ear_r": Bone("ear_r", 8),
    "trunk": Bone("trunk", 25),
    "leg_l": Bone("leg_l", 20),
    "leg_r": Bone("leg_r", 20),
})

THEMES = {
    "elephant": MascotSpec(
        body_idle=(0.65, 0.65, 0.70),
        body_working=(0.55, 0.65, 0.75),
        body_paused=(0.75, 0.70, 0.65),
        skeleton=ELEPHANT_SKELETON,
        trunk=True,
        tail=True,
    ),
}


# =======================
# BACKWARD COMPATIBILITY
# =======================

class MascotTheme:
    ELEPHANT = "elephant"

    THEMES = {
        "elephant": {
            "name": "Ellie (Elephant)",
            "icon": "🐘",
        }
    }

    @classmethod
    def get_theme(cls, theme_name):
        return cls.THEMES.get(theme_name, cls.THEMES["elephant"])

    @classmethod
    def get_all_themes(cls):
        return list(cls.THEMES.keys())


# =======================
# STATE TABLES
# =======================

STATE_POOLS = {
    "idle": [
        State.IDLE, State.IDLE, State.WAVING,
        State.THINKING, State.JUMPING, State.CONFUSED, State.LAUGHING
    ],
    "tracking": [
        State.WORKING, State.WORKING, State.WORKING,
        State.THINKING, State.RUNNING,
        State.CELEBRATING, State.EXCITED, State.DANCING
    ],
    "paused": [
        State.IDLE, State.THINKING,
        State.TIRED, State.MEDITATING, State.CONFUSED
    ],
}

CLOSED_EYES = {State.TIRED}
WIDE_EYES = {State.SHOCKED, State.EXCITED}
HAPPY_EYES = {State.HAPPY, State.CELEBRATING}


# =======================
# BONE ANIMATION TABLE
# =======================

BONE_ANIMATIONS = {
    State.IDLE: {
        "ear_l": lambda f: math.sin(f*0.15) * 0.1,
        "ear_r": lambda f: -math.sin(f*0.15) * 0.1,
        "trunk": lambda f: math.sin(f*0.1) * 0.2,
    },
    State.RUNNING: {
        "leg_l": lambda f: math.sin(f*0.3) * 0.6,
        "leg_r": lambda f: -math.sin(f*0.3) * 0.6,
    },
    State.WAVING: {
        "trunk": lambda f: -0.5 + math.sin(f*0.4) * 0.5,
    },
}


# =======================
# CHARACTER
# =======================

@dataclass
class MascotCharacter:
     # --- tamagotchi ---
    hunger: float = 0.0
    energy: float = 1.0
    boredom: float = 0.0

    tamagotchi: bool = False
    theme: str = "elephant"
    state: State = State.IDLE

    frame: int = 0
    state_timer: int = 0
    state_duration: int = 120

    blink_timer: int = 0
    blinking: bool = False

    bounce: float = 0.0
    bounce_dir: int = 1
    sleepy: bool = False  # DISABLED - never sleep

    spec: MascotSpec = field(init=False)
    
    # Backward compatibility - expose State constants as class attributes
    IDLE = State.IDLE
    THINKING = State.THINKING
    WORKING = State.WORKING
    RUNNING = State.RUNNING
    JUMPING = State.JUMPING
    WAVING = State.WAVING
    # SLEEPING = State.SLEEPING  # REMOVED
    CELEBRATING = State.CELEBRATING
    EXCITED = State.EXCITED
    CONFUSED = State.CONFUSED
    SHOCKED = State.SHOCKED
    LAUGHING = State.LAUGHING
    TIRED = State.TIRED
    DANCING = State.DANCING
    MEDITATING = State.MEDITATING
    DRINKING = State.DRINKING
    HAPPY = State.HAPPY

    def __post_init__(self):
        self.set_theme(self.theme)
        # Ensure tamagotchi values are floats with safe defaults
        try:
            self.hunger = float(self.hunger)
        except (ValueError, TypeError):
            self.hunger = 0.0
        try:
            self.energy = float(self.energy)
        except (ValueError, TypeError):
            self.energy = 1.0
        try:
            self.boredom = float(self.boredom)
        except (ValueError, TypeError):
            self.boredom = 0.0

    # ---------- compatibility ----------

    def set_theme(self, theme):
        self.theme = theme
        self.spec = THEMES.get(theme, THEMES["elephant"])

    def set_sleepy(self, sleepy):
        # DISABLED - sleep mode removed
        self.sleepy = False  # Always keep awake
        if self.state == State.IDLE:  # Don't change if doing something
            self.state = State.IDLE
        self.state_timer = 0

    def change_random_state(self, is_tracking=False, is_paused=False):
        self.change_state(is_tracking, is_paused)

    # ---------- math ----------

    def _sin(self, speed, amp=1.0):
        return math.sin(self.frame * speed) * amp

    def _abs_sin(self, speed, amp=1.0):
        return abs(math.sin(self.frame * speed)) * amp

    # ---------- animation ----------

    def next_frame(self):
        self.frame += 1
        self.brain_tick()
        self.state_timer += 1

        self.blink_timer += 1
        if not self.blinking and self.blink_timer > 60 and random.random() < 0.05:
            self.blinking = True
            self.blink_timer = 0
        elif self.blinking and self.blink_timer > 5:
            self.blinking = False
            self.blink_timer = 0

        self.bounce += 0.15 * self.bounce_dir
        if abs(self.bounce) > 2:
            self.bounce_dir *= -1

        if self.state_timer > self.state_duration:
            self.change_state()

        self._apply_skeleton()

    def change_state(self, tracking=False, paused=False):
        self.state_timer = 0
        self.state_duration = random.randint(80, 200)

        # SLEEP MODE DISABLED - never enter sleeping state
        # if self.sleepy:
        #     self.state = State.SLEEPING
        #     return

        key = "paused" if paused else "tracking" if tracking else "idle"
        self.state = random.choice(STATE_POOLS[key])

    def _apply_skeleton(self):
        skel = self.spec.skeleton
        if not skel:
            return

        anim = BONE_ANIMATIONS.get(self.state)
        if not anim:
            return

        for name, fn in anim.items():
            if name in skel.bones:
                skel.bones[name].angle = fn(self.frame)

    # =======================
    # DRAW
    # =======================

    def draw(self, cr, cx, cy, size, tracking=False, paused=False):
        s = size / 80
        cy += self.bounce

        if self.state == State.JUMPING:
            cy -= abs(self._sin(0.2, 15 * s))

        body_color = (
            self.spec.body_working if tracking and not paused else
            self.spec.body_paused if paused else
            self.spec.body_idle
        )

        self._shadow(cr, cx, cy, s)
        self._body(cr, cx, cy, s, body_color)
        self._ears(cr, cx, cy, s, body_color)
        self._legs(cr, cx, cy, s, body_color)

        if self.spec.trunk:
            self._trunk(cr, cx, cy, s, body_color)

        self._face(cr, cx, cy, s)
        self._effects(cr, cx, cy, s)

    # ---------- parts ----------

    def _shadow(self, cr, cx, cy, s):
        cr.save()
        cr.set_source_rgba(0, 0, 0, 0.15)
        cr.translate(cx, cy + 35*s)
        cr.scale(40*s, 10*s)
        cr.arc(0, 0, 1, 0, 2*math.pi)
        cr.restore()
        cr.fill()

    def _body(self, cr, cx, cy, s, color):
        cr.set_source_rgb(*color)
        cr.save()
        cr.translate(cx, cy)
        cr.scale(self.spec.body_scale_x, 1)
        cr.arc(0, 0, self.spec.body_radius*s, 0, 2*math.pi)
        cr.restore()
        cr.fill()

    def _ears(self, cr, cx, cy, s, color):
        flap = self._abs_sin(0.15, 0.01)
        for sign, bone in ((-1, "ear_l"), (1, "ear_r")):
            angle = flap
            if self.spec.skeleton:
                angle += self.spec.skeleton.bones[bone].angle

            cr.save()
            cr.translate(cx + sign*self.spec.ear_offset[0]*s, cy + self.spec.ear_offset[1]*s)
            cr.rotate(sign * (0.3 + angle))
            cr.scale(1, 1.3)
            cr.set_source_rgb(*[c * 0.9 for c in color])
            cr.arc(0, 0, self.spec.ear_radius*s, 0, 2*math.pi)
            cr.fill()
            cr.set_source_rgba(*self.spec.ear_inner)
            cr.arc(0, 0, self.spec.ear_radius*0.66*s, 0, 2*math.pi)
            cr.fill()
            cr.restore()

    def _legs(self, cr, cx, cy, s, color):
        cr.set_source_rgb(*[c * 0.85 for c in color])
        w, h = self.spec.leg_size

        for (x, _), bone in zip(self.spec.leg_offsets, ("leg_l", "leg_r")):
            off = 0
            if self.spec.skeleton:
                off = self.spec.skeleton.bones[bone].angle * 10*s

            cr.rectangle(cx + x*s, cy + 15*s + off, w*s, h*s)

        cr.fill()

    def _trunk(self, cr, cx, cy, s, color):
        angle = self.spec.skeleton.bones["trunk"].angle if self.spec.skeleton else 0
        cr.set_source_rgb(*color)
        cr.set_line_width(10*s)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)

        sx = math.sin(angle)
        cr.move_to(cx, cy + 8*s)
        cr.curve_to(
            cx + sx * 10*s, cy + 18*s,
            cx + sx * 15*s, cy + 28*s,
            cx + sx * 20*s, cy + 35*s
        )
        cr.stroke()

    def _face(self, cr, cx, cy, s):
        eye_y = cy - 8*s

        if self.blinking or self.state in CLOSED_EYES:
            cr.set_line_width(2*s)
            for dx in (-15, 10):
                cr.move_to(cx + dx*s, eye_y)
                cr.line_to(cx + (dx+5)*s, eye_y)
            cr.stroke()
            return

        if self.state in HAPPY_EYES:
            cr.set_line_width(2*s)
            for dx in (-12, 12):
                cr.arc(cx + dx*s, eye_y, 4*s, 0.3, math.pi - 0.3)
            cr.stroke()
            return

        r, pr = (5*s, 3*s) if self.state in WIDE_EYES else (4*s, 2*s)

        cr.set_source_rgb(*self.spec.eye_white)
        for dx in (-12, 12):
            cr.arc(cx + dx*s, eye_y, r, 0, 2*math.pi)
        cr.fill()

        cr.set_source_rgb(*self.spec.eye_black)
        for dx in (-12, 12):
            cr.arc(cx + dx*s, eye_y, pr, 0, 2*math.pi)
        cr.fill()

    def _effects(self, cr, cx, cy, s):
        if self.state in (State.THINKING, State.CONFUSED):
            cr.set_font_size(16*s)
            cr.move_to(cx + 25*s, cy - 30*s)
            cr.show_text("?")
        # Sleep/zzz animation removed - no sleeping mode
    def brain_tick(self):
        if not self.tamagotchi:
            return

        # decay
        self.hunger = min(1.0, self.hunger + 0.001)
        self.energy = max(0.0, self.energy - 0.0008)
        self.boredom = min(1.0, self.boredom + 0.0006)

        # hard overrides - but never sleep
        if self.energy < 0.2:
            self.state = State.TIRED  # Just tired, not sleeping
            return

        if self.hunger > 0.85:
            self.state = State.DRINKING
            return

        # soft decisions (occasionally)
        if self.state_timer > self.state_duration:
            roll = random.random()

            if self.boredom > 0.6 and roll < 0.4:
                self.state = random.choice([State.DANCING, State.RUNNING, State.WAVING])
                self.boredom *= 0.5
            elif roll < 0.3:
                self.state = State.THINKING
            else:
                self.state = State.IDLE

            self.state_timer = 0
            self.state_duration = random.randint(60, 180)

