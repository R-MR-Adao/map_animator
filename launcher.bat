@echo off

:: Check if 'python' is in the system path
where /q python
if %errorlevel% == 0 (
    python launcher.py
) else (
    :: Check if 'py' is in the system path
    where /q py
    if %errorlevel% == 0 (
        py launcher.py
    ) else (
        echo Error: Python executable not found in the system path.
        pause
    )
)

pause
