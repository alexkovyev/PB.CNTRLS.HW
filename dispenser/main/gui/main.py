# coding=utf-8

import GUI

if __name__ == "__main__":
    gui = GUI.MainGUI()

    # gui.set_image("images/image1.jpg")
    # gui.set_text("Приятного аппетита!")
    gui.set_video("videos/test.mp4")
    gui.show_video()

    gui.window.mainloop()
