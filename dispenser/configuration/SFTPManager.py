import json
import os
import time
import platform


class SFTPManager(object):
    # https://ubuntuforums.org/showthread.php?t=135113
    linux_mount_cmd = "echo {password} | sshfs {user}@{ip}:{remote_dir} {local_dir} -o password_stdin"
    linux_unmount_cmd = "fusermount -uz {dir}"
    linux_mkdir_cmd = "mkdir -p {dir}"

    windows_mount_cmd = ""
    windows_unmount_cmd = ""
    windows_mkdir_cmd = ""

    settings_file = "sftp_config.json"

    def __init__(self):
        self.ip = ""
        self.user = "orangepi"
        self.password = "orangepi"
        self.remote_dir = "/home/orangepi/PB.CNTRLS.HW/dispenser/main/resources"
        self.local_dir = "remote_resources"

        self.load()

        self._sys_name = platform.system()

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
        pass

    def _mkdir_windows(self):
        pass

    def _mount_windows(self):
        pass

    def unmount(self):
        if self._sys_name == "Linux":
            self._unmount_linux()
        elif self._sys_name == "Windows":
            self._unmount_windows()

    def mount(self):
        if self._sys_name == "Linux":
            self._mount_linux()
        elif self._sys_name == "Windows":
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
