@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo  Mouse Tools - Demo Runner
echo ============================================================
echo.

:: Ensure dependencies are installed
echo [setup] Running uv sync...
uv sync
if errorlevel 1 (
    echo ERROR: uv sync failed.
    exit /b 1
)
echo.

:: ── Scenario 1: right-click every 10s + jiggle every 3s, 5 moves ─────────────
echo [1/5] Right-click interval=10s, jiggle interval=3s, 5 moves
uv run mouse_tools.py --interval 3 --pixels 50 --direction random --count 5 --mouse-right-click-interval 10 --sleep 10
echo.
pause

:: ── Scenario 2: show help / usage ────────────────────────────────────────────
echo [2/5] Show help / usage
uv run mouse_tools.py --help
echo.
pause

:: ── Scenario 3: quick test — 3 moves, 1s interval, 5px random ────────────────
echo [3/5] Quick test: 3 moves, 1s interval, 5px random direction
uv run mouse_tools.py --interval 1 --pixels 5 --direction random --count 3 
echo.
pause

:: ── Scenario 4: YAML config file, override pixels via CLI ────────────────────
echo [4/5] YAML config + CLI override: pixels=10, count=3
uv run mouse_tools.py --config mouse_config.yaml --pixels 10 --count 3 --interval 1 
echo.
pause

:: ── Scenario 5: directional move — move right only ───────────────────────────
echo [5/5] Directional: move right 3 times, 1s interval, 8px
uv run mouse_tools.py --interval 1 --pixels 8 --direction right --count 3
echo.
pause

:: ── Scenario 6: user-activity sleep — short sleep=10s for demo purposes ───────
echo [6/6] Activity detection: interval=3s, sleep=10s on user activity
echo       (move mouse or press a key during the 3s interval to trigger sleep)
uv run mouse_tools.py --interval 3 --pixels 5 --count 5 --sleep 10
echo.

echo ============================================================
echo  All 6 scenarios completed.
echo ============================================================
pause
