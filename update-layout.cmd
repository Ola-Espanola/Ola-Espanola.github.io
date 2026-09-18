@echo off
node "%~dp0scripts\update-layout.cjs"
if errorlevel 1 (
  echo Update failed. See the message above. Node.js must be installed.
  pause
  exit /b 1
)
pause
