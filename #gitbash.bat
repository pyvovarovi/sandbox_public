@echo off
if not exist "%ProgramFiles%\Git\git-bash.exe" (
    echo ERROR: git-bash.exe not found at "%ProgramFiles%\Git\git-bash.exe"
    pause
    exit /b 1
)
start /D "%~dp0" "" "%ProgramFiles%\Git\git-bash.exe"
:: -------------------------------------------------
:: cd /d "%~dp0"
:: start "" "%ProgramFiles%\Git\git-bash.exe"
:: start "" "%ProgramFiles%\Git\git-bash.exe" -c "echo 1 && echo 2; exec bash --login -i"
:: start "" "%ProgramFiles%\Git\git-bash.exe" -c "echo 1 && echho 2 && exit; exec bash --login -i"
:: -------------------------------------------------
:: pause
