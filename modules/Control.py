
# control system

import keyboard
import sys
import control.USB_switch as USB
import control.wake_main as main
import control.wake_gaming as game
from time import sleep
import control.HDMI as HDMI
import os
import threading
import modules.shared as shared

class ControlSystem:
    def __init__(self):
        self.screen = 1
        self.ccard = 1
        self.command_map = {
            "start": self.start,
            "switch_usb": self.switch_usb,
            "start_main": self.start_main,
            "start_game": self.start_game,
            "HDMI_A1": self.hdmi_a1,
            "HDMI_A2": self.hdmi_a2,
            "HDMI_A3": self.hdmi_a3,
            "HDMI_A4": self.hdmi_a4,
            "HDMI_B1": self.hdmi_b1,
            "HDMI_B2": self.hdmi_b2,
            "HDMI_B3": self.hdmi_b3,
            "HDMI_B4": self.hdmi_b4,
            "reboot": self.reboot
        }

    def execute_command(self, term):
        func = self.command_map.get(term, None)
        if func:
            func()
        else:
            print("No command found")

    def start(self):
        try:
            self.screen = 1
            self.ccard = 1
            HDMI.a1()
            HDMI.b1()
            sleep(1.5)
        except Exception as e:
            print(f"Problem with setting initial screen and card state: {e}")
        sleep(0.5)

    def switch_usb(self):
        try:
            USB.run()
        except Exception as e:
            print(f"Problem with USB switch: {e}")
        sleep(0.5)

    def start_main(self):
        try:
            main.run()
        except Exception as e:
            print(f"Problem with starting main PC: {e}")
        sleep(0.5)

    def start_game(self):
        try:
            game.run()
        except Exception as e:
            print(f"Problem with starting game PC: {e}")
        sleep(0.5)

    def hdmi_a1(self):
        try:
            self.screen = 1
            HDMI.a1()
        except Exception as e:
            print(f"Problem with HDMI A1: {e}")
        sleep(0.5)

    def hdmi_a2(self):
        try:
            self.screen = 2
            HDMI.a2()
        except Exception as e:
            print(f"Problem with HDMI A2: {e}")
        sleep(0.5)

    def hdmi_a3(self):
        try:
            self.screen = 3
            HDMI.a3()
        except Exception as e:
            print(f"Problem with HDMI A3: {e}")
        sleep(0.5)

    def hdmi_a4(self):
        try:
            self.screen = 4
            HDMI.a4()
        except Exception as e:
            print(f"Problem with HDMI A4: {e}")
        sleep(0.5)

    def hdmi_b1(self):
        try:
            self.ccard = 1
            HDMI.b1()
        except Exception as e:
            print(f"Problem with HDMI B1: {e}")
        sleep(0.5)

    def hdmi_b2(self):
        try:
            self.ccard = 2
            HDMI.b2()
        except Exception as e:
            print(f"Problem with HDMI B2: {e}")
        sleep(0.5)

    def hdmi_b3(self):
        try:
            self.ccard = 3
            HDMI.b3()
        except Exception as e:
            print(f"Problem with HDMI B3: {e}")
        sleep(0.5)

    def hdmi_b4(self):
        try:
            self.ccard = 4
            HDMI.b4()
        except Exception as e:
            print(f"Problem with HDMI B4: {e}")
        sleep(0.5)

    def reboot(self):
        try:
            os.system("sudo reboot")
        except Exception as e:
            print(f"Problem with reboot: {e}")
        sleep(0.5)

def thread_control(control_system):
    sys.stdout = open("/home/izitto/Desktop/Code/PAtDS/static/log.txt", "w")
    control_system.execute_command("start")

    while True:
        if keyboard.is_pressed(98):
            control_system.execute_command("switch_usb")
        if keyboard.is_pressed(55):
            control_system.execute_command("start_main")
        if keyboard.read_key() == "-":
            control_system.execute_command("start_game")
        if keyboard.read_key() == "7":
            control_system.execute_command("HDMI_A1")
        if keyboard.read_key() == "8":
            control_system.execute_command("HDMI_A2")
        if keyboard.read_key() == "9":
            control_system.execute_command("HDMI_A3")
        if keyboard.read_key() == "+":
            control_system.execute_command("HDMI_A4")
        if keyboard.read_key() == "4":
            control_system.execute_command("HDMI_B1")
        if keyboard.read_key() == "5":
            control_system.execute_command("HDMI_B2")
        if keyboard.read_key() == "6":
            control_system.execute_command("HDMI_B3")
        if keyboard.read_key() == "backspace":
            control_system.execute_command("HDMI_B4")
        if keyboard.read_key() == ".":
            control_system.execute_command("reboot")

if __name__ == "__main__":
    control_system = ControlSystem()
    con = threading.Thread(target=thread_control, args=(control_system,))
    con.start()
