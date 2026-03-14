"""
mouse_tools.py — Mouse jiggler / mover utility.

Priority order for configuration:
  1. CLI arguments (highest)
  2. YAML config file (--config or mouse_config.yaml)
  3. Built-in defaults (lowest)

Defaults:
  interval     : 30 seconds
  pixels       : 5
  direction    : random
  keep_running : true  (loop forever after count is reached)
  sleep        : 300 seconds (user-activity sleep duration)
"""

import argparse
import random
import sys
import threading
import time
from pathlib import Path

import pyautogui
import yaml
from pynput import keyboard

# ── defaults ──────────────────────────────────────────────────────────────────
DEFAULTS = {
    "interval": 30,   # seconds between moves
    "pixels": 5,      # pixels to move
    "direction": "random",  # random | up | down | left | right
    "count": 0,                    # 0 = infinite
    "keep_running": True,          # restart loop after count is reached
    "mouse_right_click_interval": 0,  # 0 = disabled; >0 = seconds between right-clicks
    "sleep": 300,                  # seconds to sleep when user activity is detected
    "move_threshold": 10,          # minimum pixels moved to count as user activity
    "corner_recovery": True,       # move cursor to screen centre when fail-safe corner is hit
}

# ── activity detection ─────────────────────────────────────────────────────────
_key_pressed = threading.Event()

def _on_key_press(_key):
    _key_pressed.set()

def _start_key_listener() -> keyboard.Listener:
    listener = keyboard.Listener(on_press=_on_key_press)
    listener.daemon = True
    listener.start()
    return listener

DEFAULT_CONFIG = Path("mouse_config.yaml")

# ── config loading ─────────────────────────────────────────────────────────────
def load_yaml(path: Path) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f) or {}


def build_config(args: argparse.Namespace) -> dict:
    cfg = dict(DEFAULTS)

    # layer 2: yaml file
    yaml_path = Path(args.config) if args.config else DEFAULT_CONFIG
    if yaml_path.exists():
        yaml_cfg = load_yaml(yaml_path)
        cfg.update({k: v for k, v in yaml_cfg.items() if v is not None})

    # layer 1: cli overrides
    for key in ("interval", "pixels", "direction", "count", "mouse_right_click_interval", "sleep", "move_threshold"):
        val = getattr(args, key, None)
        if val is not None:
            cfg[key] = val

    # boolean flags — check explicitly
    if getattr(args, "no_keep_running", False):
        cfg["keep_running"] = False
    if getattr(args, "no_corner_recovery", False):
        cfg["corner_recovery"] = False

    return cfg


# ── mouse logic ────────────────────────────────────────────────────────────────
DIRECTION_MAP = {
    "up":    (0, -1),
    "down":  (0,  1),
    "left":  (-1, 0),
    "right": (1,  0),
}


def jiggle(pixels: int, direction: str) -> tuple[int, int]:
    if direction == "random":
        dx = random.choice([-1, 1]) * pixels
        dy = random.choice([-1, 1]) * pixels
    else:
        vx, vy = DIRECTION_MAP.get(direction, (0, 0))
        dx, dy = vx * pixels, vy * pixels
    pyautogui.moveRel(dx, dy, duration=0.1)
    return dx, dy


# ── main loop ──────────────────────────────────────────────────────────────────
def run(cfg: dict) -> None:
    interval        = float(cfg["interval"])
    pixels          = int(cfg["pixels"])
    direction       = str(cfg["direction"])
    count           = int(cfg["count"])
    keep_running    = bool(cfg["keep_running"])
    rc_interval     = float(cfg["mouse_right_click_interval"])
    sleep_duration  = float(cfg["sleep"])
    move_threshold  = float(cfg["move_threshold"])
    corner_recovery = bool(cfg["corner_recovery"])

    mode = "infinite" if count == 0 else f"{count} moves"
    print(f"Mouse jiggler started")
    print(f"  interval                  : {interval}s")
    print(f"  pixels                    : {pixels}")
    print(f"  direction                 : {direction}")
    print(f"  count                     : {mode}")
    print(f"  keep_running              : {keep_running}")
    print(f"  mouse_right_click_interval: {'disabled' if rc_interval == 0 else f'{rc_interval}s'}")
    print(f"  sleep (on user activity)  : {sleep_duration}s")
    print(f"  move_threshold            : {move_threshold}px")
    print(f"  corner_recovery           : {corner_recovery}")
    print("Press Ctrl+C to stop.\n")

    pyautogui.FAILSAFE = True  # move mouse to top-left corner to abort
    _start_key_listener()

    moves = 0
    last_rc = time.monotonic() if rc_interval > 0 else None
    last_pos = pyautogui.position()
    try:
        while True:
            _key_pressed.clear()
            time.sleep(interval)

            # detect user activity during the sleep
            cur_pos = pyautogui.position()
            dist = ((cur_pos.x - last_pos.x) ** 2 + (cur_pos.y - last_pos.y) ** 2) ** 0.5
            mouse_moved = dist >= move_threshold
            key_hit = _key_pressed.is_set()

            if mouse_moved or key_hit:
                reason = "mouse moved" if mouse_moved else "key pressed"
                print(f"\n  User active ({reason}), sleeping {sleep_duration:.0f}s...", flush=True)
                time.sleep(sleep_duration)
                # discard any activity that happened during the sleep — fresh baseline
                _key_pressed.clear()
                last_pos = pyautogui.position()
                print(f"  Resuming.", flush=True)
                continue

            try:
                dx, dy = jiggle(pixels, direction)
            except pyautogui.FailSafeException:
                if corner_recovery:
                    sw, sh = pyautogui.size()
                    pyautogui.FAILSAFE = False
                    pyautogui.moveTo(sw // 2, sh // 2, duration=0.3)
                    pyautogui.FAILSAFE = True
                    print("\n  Fail-safe: moved cursor to screen centre.", flush=True)
                else:
                    print("\n  Fail-safe: mouse at corner, skipping move.", flush=True)
                last_pos = pyautogui.position()
                continue
            last_pos = pyautogui.position()
            moves += 1

            # right-click on its own independent timer
            if rc_interval > 0:
                now = time.monotonic()
                if now - last_rc >= rc_interval:
                    pyautogui.click(button="right")
                    last_rc = now
                    print(f"\r  right-click                            ", end="", flush=True)
                    time.sleep(0.05)

            print(f"\r  moved [{moves}] ({dx:+d}, {dy:+d})   ", end="", flush=True)

            if count > 0 and moves >= count:
                if not keep_running:
                    break
                moves = 0  # reset counter and loop again
    except KeyboardInterrupt:
        pass
    print(f"\nStopped after {moves} move(s).")


# ── CLI ────────────────────────────────────────────────────────────────────────
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Mouse jiggler — keeps screen active by moving the mouse.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--config",    metavar="FILE",  help="Path to YAML config file (default: mouse_config.yaml)")
    p.add_argument("--interval",  type=float,      metavar="SEC",  help="Seconds between moves")
    p.add_argument("--pixels",    type=int,        metavar="PX",   help="Pixels to move each time")
    p.add_argument("--direction", choices=["random", "up", "down", "left", "right"], help="Move direction")
    p.add_argument("--count",          type=int, metavar="N", help="Number of moves (0 = infinite)")
    p.add_argument("--no-keep-running",          action="store_true", help="Stop after --count moves instead of looping")
    p.add_argument("--mouse-right-click-interval", type=float, metavar="SEC", dest="mouse_right_click_interval",
                   help="Seconds between right-clicks (0 = disabled)")
    p.add_argument("--sleep", type=float, metavar="SEC",
                   help="Seconds to sleep when user activity is detected (default: 300)")
    p.add_argument("--move-threshold", type=float, metavar="PX", dest="move_threshold",
                   help="Minimum pixels moved to count as user activity (default: 10)")
    p.add_argument("--no-corner-recovery", action="store_true",
                   help="Skip corner recovery — leave cursor at corner instead of moving to centre")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    cfg  = build_config(args)
    run(cfg)
"""
mouse_tools.py — Mouse jiggler / mover utility.

Priority order for configuration:
  1. CLI arguments (highest)
  2. YAML config file (--config or mouse_config.yaml)
  3. Built-in defaults (lowest)

Defaults:
  interval     : 30 seconds
  pixels       : 5
  direction    : random
  keep_running : true  (loop forever after count is reached)
  sleep        : 300 seconds (user-activity sleep duration)
"""

import argparse
import random
import sys
import threading
import time
from pathlib import Path

import pyautogui
import yaml
from pynput import keyboard

# ── defaults ──────────────────────────────────────────────────────────────────
DEFAULTS = {
    "interval": 30,   # seconds between moves
    "pixels": 5,      # pixels to move
    "direction": "random",  # random | up | down | left | right
    "count": 0,                    # 0 = infinite
    "keep_running": True,          # restart loop after count is reached
    "mouse_right_click_interval": 0,  # 0 = disabled; >0 = seconds between right-clicks
    "sleep": 300,                  # seconds to sleep when user activity is detected
    "move_threshold": 10,          # minimum pixels moved to count as user activity
}

# ── activity detection ─────────────────────────────────────────────────────────
_key_pressed = threading.Event()

def _on_key_press(_key):
    _key_pressed.set()

def _start_key_listener() -> keyboard.Listener:
    listener = keyboard.Listener(on_press=_on_key_press)
    listener.daemon = True
    listener.start()
    return listener

DEFAULT_CONFIG = Path("mouse_config.yaml")

# ── config loading ─────────────────────────────────────────────────────────────
def load_yaml(path: Path) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f) or {}


def build_config(args: argparse.Namespace) -> dict:
    cfg = dict(DEFAULTS)

    # layer 2: yaml file
    yaml_path = Path(args.config) if args.config else DEFAULT_CONFIG
    if yaml_path.exists():
        yaml_cfg = load_yaml(yaml_path)
        cfg.update({k: v for k, v in yaml_cfg.items() if v is not None})

    # layer 1: cli overrides
    for key in ("interval", "pixels", "direction", "count", "mouse_right_click_interval", "sleep", "move_threshold"):
        val = getattr(args, key, None)
        if val is not None:
            cfg[key] = val

    # keep_running is a boolean flag — check explicitly
    if getattr(args, "no_keep_running", False):
        cfg["keep_running"] = False

    return cfg


# ── mouse logic ────────────────────────────────────────────────────────────────
DIRECTION_MAP = {
    "up":    (0, -1),
    "down":  (0,  1),
    "left":  (-1, 0),
    "right": (1,  0),
}


def jiggle(pixels: int, direction: str) -> tuple[int, int]:
    if direction == "random":
        dx = random.choice([-1, 1]) * pixels
        dy = random.choice([-1, 1]) * pixels
    else:
        vx, vy = DIRECTION_MAP.get(direction, (0, 0))
        dx, dy = vx * pixels, vy * pixels
    pyautogui.moveRel(dx, dy, duration=0.1)
    return dx, dy


# ── main loop ──────────────────────────────────────────────────────────────────
def run(cfg: dict) -> None:
    interval        = float(cfg["interval"])
    pixels          = int(cfg["pixels"])
    direction       = str(cfg["direction"])
    count           = int(cfg["count"])
    keep_running    = bool(cfg["keep_running"])
    rc_interval     = float(cfg["mouse_right_click_interval"])
    sleep_duration  = float(cfg["sleep"])
    move_threshold  = float(cfg["move_threshold"])

    mode = "infinite" if count == 0 else f"{count} moves"
    print(f"Mouse jiggler started")
    print(f"  interval                  : {interval}s")
    print(f"  pixels                    : {pixels}")
    print(f"  direction                 : {direction}")
    print(f"  count                     : {mode}")
    print(f"  keep_running              : {keep_running}")
    print(f"  mouse_right_click_interval: {'disabled' if rc_interval == 0 else f'{rc_interval}s'}")
    print(f"  sleep (on user activity)  : {sleep_duration}s")
    print(f"  move_threshold            : {move_threshold}px")
    print("Press Ctrl+C to stop.\n")

    pyautogui.FAILSAFE = True  # move mouse to top-left corner to abort
    _start_key_listener()

    moves = 0
    last_rc = time.monotonic() if rc_interval > 0 else None
    last_pos = pyautogui.position()
    try:
        while True:
            _key_pressed.clear()
            time.sleep(interval)

            # detect user activity during the sleep
            cur_pos = pyautogui.position()
            dist = ((cur_pos.x - last_pos.x) ** 2 + (cur_pos.y - last_pos.y) ** 2) ** 0.5
            mouse_moved = dist >= move_threshold
            key_hit = _key_pressed.is_set()

            if mouse_moved or key_hit:
                reason = "mouse moved" if mouse_moved else "key pressed"
                print(f"\n  User active ({reason}), sleeping {sleep_duration:.0f}s...", flush=True)
                time.sleep(sleep_duration)
                # discard any activity that happened during the sleep — fresh baseline
                _key_pressed.clear()
                last_pos = pyautogui.position()
                print(f"  Resuming.", flush=True)
                continue

            try:
                dx, dy = jiggle(pixels, direction)
            except pyautogui.FailSafeException:
                print("\n  Fail-safe: mouse at corner, skipping move.", flush=True)
                last_pos = pyautogui.position()
                continue
            last_pos = pyautogui.position()
            moves += 1

            # right-click on its own independent timer
            if rc_interval > 0:
                now = time.monotonic()
                if now - last_rc >= rc_interval:
                    pyautogui.click(button="right")
                    last_rc = now
                    print(f"\r  right-click                            ", end="", flush=True)
                    time.sleep(0.05)

            print(f"\r  moved [{moves}] ({dx:+d}, {dy:+d})   ", end="", flush=True)

            if count > 0 and moves >= count:
                if not keep_running:
                    break
                moves = 0  # reset counter and loop again
    except KeyboardInterrupt:
        pass
    print(f"\nStopped after {moves} move(s).")


# ── CLI ────────────────────────────────────────────────────────────────────────
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Mouse jiggler — keeps screen active by moving the mouse.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--config",    metavar="FILE",  help="Path to YAML config file (default: mouse_config.yaml)")
    p.add_argument("--interval",  type=float,      metavar="SEC",  help="Seconds between moves")
    p.add_argument("--pixels",    type=int,        metavar="PX",   help="Pixels to move each time")
    p.add_argument("--direction", choices=["random", "up", "down", "left", "right"], help="Move direction")
    p.add_argument("--count",          type=int, metavar="N", help="Number of moves (0 = infinite)")
    p.add_argument("--no-keep-running",          action="store_true", help="Stop after --count moves instead of looping")
    p.add_argument("--mouse-right-click-interval", type=float, metavar="SEC", dest="mouse_right_click_interval",
                   help="Seconds between right-clicks (0 = disabled)")
    p.add_argument("--sleep", type=float, metavar="SEC",
                   help="Seconds to sleep when user activity is detected (default: 300)")
    p.add_argument("--move-threshold", type=float, metavar="PX", dest="move_threshold",
                   help="Minimum pixels moved to count as user activity (default: 10)")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    cfg  = build_config(args)
    run(cfg)
