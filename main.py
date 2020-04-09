# coding=utf-8
import threading

from Dispenser import Dispenser
from Dispenser import Message

dispenser = Dispenser(None)

dispenser.start()


# add_light_mode_msg = "#[Dispenser;add_light_mode](blink;1;0;1;25;255;1.5;0;1;0)#"
# dispenser.interfacing.raw_messages_q.put(add_light_mode_msg)

# add_light_mode_msg = "#[Dispenser;add_light_mode](idle;0;1;0;25;255;1.5;0;1;0)#"
# dispenser.interfacing.raw_messages_q.put(add_light_mode_msg)

# add_light_mode_msg = "#[Dispenser;add_light_mode](wrong_qr;0;0;1;50;255;1;1;1;0)#"
# dispenser.interfacing.raw_messages_q.put(add_light_mode_msg)

# set_light_mode_msg = "#[Dispenser;set_light_mode](blink)#"
# dispenser.interfacing.raw_messages_q.put(set_light_mode_msg)

# set_display_text_msg = "#[Dispenser;set_display_text](hello, world!;15;255;255;255)#"
# dispenser.interfacing.raw_messages_q.put(set_display_text_msg)

# set_display_img_msg = "#[Dispenser;set_display_image](gui/images/image1.jpg)#"
# dispenser.interfacing.raw_messages_q.put(set_display_img_msg)

# set_display_video_msg = "#[Dispenser;set_display_video](gui/videos/test.mp4;60)#"
# dispenser.interfacing.raw_messages_q.put(set_display_video_msg)

# will_dispense_msg = "#[Dispenser;will_dispense]()#"
# dispenser.interfacing.raw_messages_q.put(will_dispense_msg)

# time.sleep(5)

# is_littered_msg = "#[Dispenser;is_littered]()#"
# dispenser.interfacing.raw_messages_q.put(is_littered_msg)

# time.sleep(2)

# dispensed_msg = "#[Dispenser;dispensed](42)#"
# dispenser.interfacing.raw_messages_q.put(dispensed_msg)


def cli():
    try:
        while True:
            message = raw_input()
            dispenser.interfacing.raw_messages_q.put(message)
            # time.sleep(6.5)
            # set_light_mode_msg = "#[Dispenser;set_light_mode](blink)#"
            # dispenser.interfacing.raw_messages_q.put(set_light_mode_msg)
    except KeyboardInterrupt:
        dispenser.join()


def demo():
    dispenser.interfacing.raw_messages_q.put("#[Dispenser;add_light_mode](idle;1;0;1;25;255;1.5;1;1.5;1;0)#")
    dispenser.interfacing.raw_messages_q.put("#[Dispenser;add_light_mode](wrong_qr;1;0;0;0;255;0.5;0.5;0.5;0.5;2)#")
    dispenser.interfacing.raw_messages_q.put("#[Dispenser;add_light_mode](wait;0;0;1;25;255;1.5;0.5;1.5;0.5;0)#")
    dispenser.interfacing.raw_messages_q.put("#[Dispenser;add_light_mode](dispensed;0;1;0;25;255;0.5;1.5;0.5;1.5;0)#")
    dispenser.interfacing.raw_messages_q.put("#[Dispenser;add_light_mode](littered;1;0;0;25;255;0.25;0.5;0.25;0.5;3)#")
    dispenser.interfacing.raw_messages_q.put("#[Dispenser;add_light_mode](none;0;0;0;0;0;0;0;0;0;0)#")

    msgs_q = dispenser.interfacing.bridge.send_q
    qr_code = None
    while True:
        if not msgs_q.empty():
            msg_raw = msgs_q.get()
            msg = Message(msg_raw)

            if msg.header.command_name == "qr_scanned":
                dispenser.interfacing.raw_messages_q.put("#[Dispenser;is_littered]()#")
                qr_code = msg.parameters[0]
            elif msg.header.command_name == "is_littered":
                if msg.parameters[0] == "1":
                    dispenser.interfacing.raw_messages_q.put("#[Dispenser;set_light_mode](littered)#")
                    dispenser.interfacing.raw_messages_q.put(
                        "#[Dispenser;set_display_text](Модуль загрязнён!;2000;15;255;255;255)#")
                else:
                    dispenser.interfacing.raw_messages_q.put("#[Dispenser;will_dispense]()#")
                    dispenser.interfacing.raw_messages_q.put("#[Dispenser;set_light_mode](wait)#")
                    dispenser.interfacing.raw_messages_q.put(
                        "#[Dispenser;set_display_text](Ожидайте выдачи!;0;15;255;255;255)#")
                    raw_input("press any key...")
                    dispenser.interfacing.raw_messages_q.put("#[Dispenser;dispensed]({})#".format(qr_code))
                    dispenser.interfacing.raw_messages_q.put("#[Dispenser;set_light_mode](dispensed)#")
                    dispenser.interfacing.raw_messages_q.put(
                        "#[Dispenser;set_display_text](Приятного аппетита!;0;15;255;255;255)#")
            elif msg.header.command_name == "picked_up":
                dispenser.interfacing.raw_messages_q.put(
                    "#[Dispenser;set_display_text](Наслаждайтесь!;1000;15;255;255;255)#")
                dispenser.interfacing.raw_messages_q.put("#[Dispenser;set_light_mode](none)#")


cli_th = threading.Thread(target=cli)
cli_th.daemon = True
cli_th.start()

demo_th = threading.Thread(target=demo)
demo_th.daemon = True
demo_th.start()

dispenser.gui.window.mainloop()
