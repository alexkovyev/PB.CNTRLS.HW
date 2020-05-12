import json
import time
import platform

sys_name = platform.system()

import os, sys
import subprocess
import win32console, win32con

class SFTPManager(object):
    # https://ubuntuforums.org/showthread.php?t=135113
    linux_mount_cmd = "echo {password} | sshfs {user}@{ip}:{remote_dir} {local_dir} -o password_stdin"
    linux_unmount_cmd = "fusermount -uz {dir}"
    linux_mkdir_cmd = "mkdir -p {dir}"

    # windows_mount_cmd = "net use {local_dir} \\\\sshfs\\{user}@{ip}\\{remote_dir}"
    windows_mount_cmd = 'sshfs-win.exe cmd {user}@{ip}:{remote_dir} {local_dir} -o password_stdin'
    # windows_unmount_cmd = "net use {dir} /delete"
    windows_unmount_cmd = 'taskkill /IM "sshfs.exe" /F'

    settings_file = "sftp_config.json"

    def __init__(self):
        self.ip = "192.168.1.69"
        self.user = "orangepi"
        self.password = "orangepi"
        self.remote_dir = "/home/orangepi/PB.CNTRLS.HW/dispenser/main/resources"

        self.load()

        if sys_name == "Windows":
            self.local_dir = "S:"
        else:
            self.local_dir = "remote_resources"


    def _mkdir_linux(self):
        cmd = SFTPManager.linux_mkdir_cmd.format(dir=self.local_dir)
        os.popen(cmd)

    def _unmount_linux(self):
        cmd = SFTPManager.linux_unmount_cmd.format(dir=self.local_dir)
        os.popen(cmd)

    def _mount_linux(self):
        cmd = SFTPManager.linux_mount_cmd.format(password=self.password, user=self.user, ip=self.ip,
                                                 remote_dir=self.remote_dir,
                                                 local_dir=self.local_dir)
        self._mkdir_linux()
        time.sleep(0.5)
        os.popen(cmd)

    def _unmount_windows(self):
        cmd = SFTPManager.windows_unmount_cmd.format(dir=self.local_dir)
        os.popen(cmd)

    def _mount_windows(self):
        cmd = SFTPManager.windows_mount_cmd.format(user=self.user, ip=self.ip,
                                            remote_dir=self.remote_dir,
                                            local_dir=self.local_dir)

        os.chdir("C:\\Program Files\\SSHFS-Win\\bin")  # https://stackoverflow.com/a/7130809

        # https://stackoverflow.com/a/44056313
        try:
            win32console.AllocConsole()
        except win32console.error as exc:
            if exc.winerror!=5:
                raise

        stdin=win32console.GetStdHandle(win32console.STD_INPUT_HANDLE)

        p = subprocess.Popen(["cmd.exe", "/C", cmd],stdout=subprocess.PIPE)  # https://stackoverflow.com/a/9535231
        time.sleep(2)
        for c in "{}\r".format(self.password):  # end by CR to send "RETURN"
            ## write some records to the input queue
            x=win32console.PyINPUT_RECORDType(win32console.KEY_EVENT)
            x.Char=unicode(c)
            x.KeyDown=True
            x.RepeatCount=1
            x.VirtualKeyCode=0x0
            x.ControlKeyState=win32con.SHIFT_PRESSED
            stdin.WriteConsoleInput([x])

        p.wait()

    def unmount(self):
        if sys_name == "Linux":
            self._unmount_linux()
        elif sys_name == "Windows":
            self._unmount_windows()

    def mount(self):
        if sys_name == "Linux":
            self._mount_linux()
        elif sys_name == "Windows":
            self._mount_windows()

    def save(self):
        config = {x: y for x, y in self.__dict__.items() if not x.startswith("_")}
        with open(SFTPManager.settings_file, 'w') as f:
            json.dump(config, f, indent=4)

    def load(self):
        try:
            with open(SFTPManager.settings_file, "r") as f:
                j = json.load(f)
                self.__dict__ = j
        except IOError:
            self.save()
