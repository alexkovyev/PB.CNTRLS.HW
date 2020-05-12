from SFTPManager import SFTPManager
from interfacing.InterfacingManager import InterfacingManager

from Interfacing import Interfacing
import GUI

interfacing = InterfacingManager(None, "Main")
interfacing.start()

device = Interfacing(interfacing)

sftp_manager = SFTPManager()
# sftp_manager._mount_windows()

gui = GUI.GUI(device, sftp_manager)
