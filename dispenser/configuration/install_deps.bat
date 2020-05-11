bitsadmin /transfer mydownloadjob /download /priority normal /dynamic "http://github.com/billziss-gh/winfsp/releases/download/v1.6/winfsp-1.6.20027.msi" "%cd%\winfsp.msi"
msiexec /qr /i winfsp.msi

:: bitsadmin /transfer mydownloadjob /download /priority normal /dynamic "https://github.com/billziss-gh/sshfs-win/releases/download/v3.5.20024/sshfs-win-3.5.20024-x86.msi.msi" "%cd%\sshfs.msi"
bitsadmin /transfer mydownloadjob /download /priority normal /dynamic "https://github.com/billziss-gh/sshfs-win/releases/download/v3.5.20024/sshfs-win-3.5.20024-x64.msi" "%cd%\sshfs.msi"
msiexec /qr /i sshfs.msi