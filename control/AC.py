import lirc
def power():
    client = lirc.Client()
    client.send_once("AC", "KEY_POWER")
def fan():
    client = lirc.Client()
    client.send_once("AC", "FAN")
def cool():
    client = lirc.Client()
    client.send_once("AC", "COOL")
def swing():
    client = lirc.Client()
    client.send_once("AC", "SWING")
