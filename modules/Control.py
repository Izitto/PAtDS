
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
import logging

# Initialize logger
logger = logging.getLogger("Control")

screen = 1
ccard = 1

def commands(term):
    global screen, ccard
    def start():
        global screen, ccard
        try:
            screen == 1
            ccard == 1
            HDMI.a1()
            HDMI.b1()
            sleep(1.5)
        except Exception as e:
            print("problem with setting initual screen and card state: " + str(e))
        sleep(0.5)
    def switch_usb():
        try:
            USB.run()
        except Exception as e:
            print("problem with usb switch: " + str(e))
        sleep(0.5)
    def start_main():
        try:
            main.run()
        except Exception as e:
            print("problem with starting main pc: " + str(e))
        sleep(0.5)
    def start_game():
        try:
            game.run()
        except Exception as e:
            print("problem with starting game pc: " + str(e))
        sleep(0.5)

    def HDMI_A1():
        global screen, ccard
        try:
            screen = 1
            
            HDMI.a1()
        except Exception as e:
            print("problem with HDMI A1: " + str(e))
        sleep(0.5)
    def HDMI_A2():
        global screen, ccard
        try:
            screen = 2
            HDMI.a2()
        except Exception as e:
            print("problem with HDMI A2: " + str(e))
        sleep(0.5)
    def HDMI_A3():
        global screen, ccard
        try:
            screen = 3
            HDMI.a3()
        except Exception as e:
            print("problem with HDMI A3: " + str(e))
        sleep(0.5)
    def HDMI_A4():
        global screen, ccard
        try:
            screen = 4
            HDMI.a4()
        except Exception as e:
            print("problem with HDMI A4: " + str(e))
        sleep(0.5)
    def HDMI_B1():
        global screen, ccard
        try:
            ccard = 1
            HDMI.b1()
        except Exception as e:
            print("problem with HDMI B1: " + str(e))
        sleep(0.5)
    def HDMI_B2():
        global screen, ccard
        try:
            ccard = 2
            HDMI.b2()
        except Exception as e:
            print("problem with HDMI B2: " + str(e))
        sleep(0.5)
    def HDMI_B3():
        global screen, ccard
        try:
            ccard = 3
            HDMI.b3()
        except Exception as e:
            print("problem with HDMI B3: " + str(e))
        sleep(0.5)
    def HDMI_B4():
        global screen, ccard
        try:
            ccard = 4
            HDMI.b4()
        except Exception as e:
            print("problem with HDMI B4: " + str(e))
        sleep(0.5)
    def reboot():
        try:
            os.system("sudo reboot")
        except Exception as e:
            print("problem with reboot: " + str(e))
        sleep(0.5)

    


    
    if term == "start":
        start()
    elif term == "switch_usb":
        switch_usb()
    elif term == "start_main":
        start_main()
    elif term == "start_game":
        start_game()
    elif term == "HDMI_A1":
        HDMI_A1()
    elif term == "HDMI_A2":
        HDMI_A2()
    elif term == "HDMI_A3":
        HDMI_A3()
    elif term == "HDMI_A4":
        HDMI_A4()
    elif term == "HDMI_B1":
        HDMI_B1()
    elif term == "HDMI_B2":
        HDMI_B2()
    elif term == "HDMI_B3":
        HDMI_B3()
    elif term == "HDMI_B4":
        HDMI_B4()
    elif term == "reboot":
        reboot()
    else:
        print("no command found")
    
    shared.emit_socketio_event('HDMI_updated', {'message': 'HDMI updated'})
    shared.emit_socketio_event('HDMI_updated', {'message': ''})

        

def thread_control():
    sys.stdout = open("/home/izitto/Desktop/Code/PAtDS/static/log.txt", "w")
    global screen, ccard
    commands("start")
    


    while True:
        if keyboard.is_pressed(98):
            commands("switch_usb")
        if keyboard.is_pressed(55):
            commands("start_main")
        if keyboard.read_key() == "-":
            commands("start_game")
        if keyboard.read_key() == "7":
            commands("HDMI_A1")
        if keyboard.read_key() == "8":
            commands("HDMI_A2")
        if keyboard.read_key() == "9":
            commands("HDMI_A3")
        if keyboard.read_key() == "+":
            commands("HDMI_A4")
        if keyboard.read_key() == "4":
            commands("HDMI_B1")
        if keyboard.read_key() == "5":
            commands("HDMI_B2")
        if keyboard.read_key() == "6":
            commands("HDMI_B3")
        if keyboard.read_key() == "backspace":
            commands("HDMI_B4")
        if keyboard.read_key() == ".":
            commands("reboot")
        if keyboard.read_key() == "1":
            pass
        if keyboard.read_key() == "2":
            pass
        if keyboard.read_key() == "0":
            pass


con = threading.Thread(target=thread_control)
def start():
    con.start()

def join():
    con.join()

def getScreens():
    global screen
    return screen

def getCCard():
    global ccard
    return ccard
    
