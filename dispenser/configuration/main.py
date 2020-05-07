from interfacing.InterfacingManager import InterfacingManager

from Interfacing import Interfacing
import GUI

interfacing = InterfacingManager(None, "Main")
interfacing.start()

device = Interfacing(interfacing)

gui = GUI.GUI(device)
