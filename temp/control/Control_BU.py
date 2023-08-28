# control system
import keyboard
import sys
import USB_switch as USB
import wake_main as main
import wake_gaming as game
from time import sleep
import HDMI
import AC
import os
import socket
import threading

# ############UDP SERVER#################
localIP = "192.168.1.107"
localPort = 20002
bufferSize = 1024
screen = 1
ccard = 1
msgFromServer = "11"
# ######################################
# os.system(f"sudo python /home/izitto/Desktop/Code/WebDebug/Debug.py")
sleep(5)
sys.stdout = open("/home/izitto/Desktop/Code/WebDebug/static/log.txt", "w")


print ("Hotkey log file")

def thread_server():

    sleep(45)

    try:
        global msgFromServer
        UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        # Bind to address and ip
        UDPServerSocket.bind((localIP, localPort))
        print("UDP server up and listening")
    except Exception as e:
        print("problem with server " +str(e))
    while True:
        try:
            newMsg = msgFromServer
            bytesToSend = str.encode(newMsg)
            bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]
            # clientMsg = "Message from Client:{}".format(message)
            # clientIP = "Client IP Address:{}".format(address)
            # print(clientMsg)
            # print(clientIP)
            # Sending a reply to client
            UDPServerSocket.sendto(bytesToSend, address)
            sleep(1)
        except Exception as e:
            print("problem with server " +str(e))


def thread_control():
    global screen, ccard, msgFromServer
    sleep(5)
    try:
        HDMI.a1()
        HDMI.b1()

        sleep(1.5)

    except Exception as e:

        print("problem with setting initual screen and card state: " + str(e))


    while True:
        if keyboard.is_pressed(98):
            print("You pressed usb switch")
            try:

                USB.run()

            except:

                print("usb switch not working")

            sleep(0.5)



        if keyboard.is_pressed(55):

            print("You pressed start main pc")

            try:

                main.run()

            except:

                print("Main PC can't start")

            sleep(0.5)



        if keyboard.read_key() == "-":

            print("You pressed start gaming pc")

            try:

                game.run()

            except:

                print("Gaming PC can't start")

            sleep(0.5)



        if keyboard.read_key() == "7":

            screen = 1

            msgFromServer = (str(screen) + str(ccard))

            print("new message: " + msgFromServer)

            try:

                HDMI.a1()

                print("code still works")

                sleep(0.5)

            except Exception as e:

                print("problemo: " + str(e))



        if keyboard.read_key() == "8":

            screen = 2

            msgFromServer = (str(screen) + str(ccard))

            print("new message: " + msgFromServer)

            try:

                print("You pressed HDMI A2")

                HDMI.a2()

                sleep(0.5)

            except:

                print("problemo")





        if keyboard.read_key() == "9":

            screen = 3

            msgFromServer = (str(screen) + str(ccard))

            print("new message: " + msgFromServer)

            try:

                print("You pressed HDMI A3")

                HDMI.a3()

                sleep(0.5)

            except:

                print("problemo")



        if keyboard.read_key() == "+":

            screen = 4

            msgFromServer = (str(screen) + str(ccard))

            print("new message: " + msgFromServer)

            try:

                print("You pressed HDMI A4")

                HDMI.a4()

                sleep(0.5)

            except:

                print("problemo")



        if keyboard.read_key() == "4":

            ccard = 1

            msgFromServer = (str(screen) + str(ccard))

            print("new message: " + msgFromServer)

            try:

                print("You pressed HDMI B1")

                HDMI.b1()

                sleep(0.5)

            except:

                print("problemo")



        if keyboard.read_key() == "5":
            ccard = 2
            msgFromServer = (str(screen) + str(ccard))
            print("new message: " + msgFromServer)
            try:
                print("You pressed HDMI B2")
                HDMI.b2()
                sleep(0.5)
            except:
                print("problemo")



        if keyboard.read_key() == "6":
            ccard = 3
            msgFromServer = (str(screen) + str(ccard))
            print("new message: " + msgFromServer)
            try:
                print("You pressed HDMI B3")
                HDMI.b3()
                sleep(0.5)
            except:
                print("problemo")



        if keyboard.read_key() == "backspace":
            ccard = 4
            msgFromServer = (str(screen) + str(ccard))
            print("new message: " + msgFromServer)
            try:
                print("You pressed HDMI B4")
                HDMI.b4()
                sleep(0.5)

            except:
                print("problemo")



        if keyboard.read_key() == ".":
            print("You pressed reboot")
            os.system("sudo reboot")

        if keyboard.read_key() == "1":
            print("Fan on")
            AC.fan()
            sleep(0.5)

        if keyboard.read_key() == "2":
            print("AC on")
            AC.cool()
            sleep(0.5)

        if keyboard.read_key() == "0":
            print("AC off")
            AC.power()
            sleep(0.5)



serv = threading.Thread(target=thread_server)
con = threading.Thread(target=thread_control)
con.start()
serv.start()
serv.join()
con.join()
