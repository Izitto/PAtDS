import lirc
def power():
    client = lirc.Client()
    client.send_once("HDMI", "KEY_POWER")
def a1():
    client = lirc.Client()
    client.send_once("HDMI", "KEY_1")
def a2():
    client = lirc.Client()
    client.send_once("HDMI", "KEY_2")
def a3():
    client = lirc.Client()
    client.send_once("HDMI", "KEY_3")
def a4():
    client = lirc.Client()
    client.send_once("HDMI", "KEY_4")
def b1():
    client = lirc.Client()
    client.send_once("HDMI", "KEY_5")
def b2():
    client = lirc.Client()
    client.send_once("HDMI", "KEY_6")
def b3():
    client = lirc.Client()
    client.send_once("HDMI", "KEY_7")
def b4():
    client = lirc.Client()
    client.send_once("HDMI", "KEY_8")