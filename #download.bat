@echo off
setlocal EnableDelayedExpansion

:: Set to "curl" or "gh"
set DOWNLOADER=gh

set REPO=pyvovarovi/claude-mouse-tools
set BRANCH=master

:: List of files to download
set FILES=mouse_config.yaml demo.bat mouse_tools.py pyproject.toml uv.lock

set BASE_URL=https://raw.githubusercontent.com/%REPO%/%BRANCH%
set ERRORS=0

echo Downloading files using %DOWNLOADER%...

if /i "%DOWNLOADER%"=="curl" (
    for %%F in (%FILES%) do (
        curl -fsSL "%BASE_URL%/%%F" -o %%F
        if errorlevel 1 ( echo FAILED: %%F [exit code !errorlevel!] & set /a ERRORS+=1 ) else ( echo Downloaded %%F )
    )
) else if /i "%DOWNLOADER%"=="gh" (
    for %%F in (%FILES%) do (
        gh api repos/%REPO%/contents/%%F --header "Accept: application/vnd.github.raw" > %%F
        if errorlevel 1 ( echo FAILED: %%F [exit code !errorlevel!] & set /a ERRORS+=1 ) else ( echo Downloaded %%F )
    )
) else (
    echo ERROR: Unknown DOWNLOADER "%DOWNLOADER%". Set to "curl" or "gh".
    set /a ERRORS+=1
)

echo.
if %ERRORS%==0 (
    echo All files downloaded successfully.
) else (
    echo Done with %ERRORS% error(s). Window will stay open.
    pause
)

endlocal
