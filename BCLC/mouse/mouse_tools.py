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
"""

import argparse
import random
import sys
import time
from pathlib import Path

import pyautogui
import yaml

# ── defaults ──────────────────────────────────────────────────────────────────
DEFAULTS = {
    "interval": 30,   # seconds between moves
    "pixels": 5,      # pixels to move
    "direction": "random",  # random | up | down | left | right
    "count": 0,                    # 0 = infinite
    "keep_running": True,          # restart loop after count is reached
    "mouse_right_click_interval": 0,  # 0 = disabled; >0 = seconds between right-clicks
}

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
    for key in ("interval", "pixels", "direction", "count", "mouse_right_click_interval"):
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

    mode = "infinite" if count == 0 else f"{count} moves"
    print(f"Mouse jiggler started")
    print(f"  interval                  : {interval}s")
    print(f"  pixels                    : {pixels}")
    print(f"  direction                 : {direction}")
    print(f"  count                     : {mode}")
    print(f"  keep_running              : {keep_running}")
    print(f"  mouse_right_click_interval: {'disabled' if rc_interval == 0 else f'{rc_interval}s'}")
    print("Press Ctrl+C to stop.\n")

    pyautogui.FAILSAFE = True  # move mouse to top-left corner to abort

    moves = 0
    last_rc = time.monotonic() if rc_interval > 0 else None
    try:
        while True:
            time.sleep(interval)
            dx, dy = jiggle(pixels, direction)
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
    except pyautogui.FailSafeException:
        print("\nFail-safe triggered: mouse moved to a screen corner.")
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
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    cfg  = build_config(args)
    run(cfg)
