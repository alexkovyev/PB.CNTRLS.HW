@echo off

set python_path="%ProgramFiles%\dispenser_python27"
if not exist %python_path% (
    set python_path="%ProgramFiles(x86)%\dispenser_python27"
)
set python_executable=%python_path%\python.exe

%python_executable% main.py