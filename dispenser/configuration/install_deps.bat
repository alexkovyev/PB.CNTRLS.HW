@echo off 

:: download and install winfsp
:: bitsadmin /transfer mydownloadjob /download /priority normal /dynamic "http://github.com/billziss-gh/winfsp/releases/download/v1.6/winfsp-1.6.20027.msi" "%cd%\winfsp.msi"
msiexec /qb! /i winfsp.msi

:: download and install sshfs
:: bitsadmin /transfer mydownloadjob /download /priority normal /dynamic "https://github.com/billziss-gh/sshfs-win/releases/download/v3.5.20024/sshfs-win-3.5.20024-x86.msi.msi" "%cd%\sshfs.msi"
:: bitsadmin /transfer mydownloadjob /download /priority normal /dynamic "https://github.com/billziss-gh/sshfs-win/releases/download/v3.5.20024/sshfs-win-3.5.20024-x64.msi" "%cd%\sshfs.msi"
msiexec /qb! /i sshfs.msi

:: install python
set python_path="%ProgramFiles%\dispenser_python27"
msiexec /qb! /norestart /i python.msi TARGETDIR=%python_path%

:: windwos just doesn't give a fuck about the specified TARGETDIR, because it will install to x86 dir anyway
if not exist %python_path% (
    set python_path="%ProgramFiles(x86)%\dispenser_python27"
)

set python_executable=%python_path%\python.exe

:: install pip
%python_executable% get-pip.py

:: install dependencies
%python_executable% -m pip install pyserial
%python_executable% -m pip install pywin32
%python_executable% -m pip install enum34