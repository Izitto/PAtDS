from time import sleep
import threading

value = 0

def up():
    global value
    while True:
        if value < 10:
            value += 5
        print(value)
        sleep(1)

def down():
    global value
    while True:
        if value > 0:
            value -= 5
        print(value)
        sleep(1)


def run1():
    up()

def run2():
    down()

threading.Thread(target=run1).start()
threading.Thread(target=run2).start()

while True:
    value += 1
    sleep(1)
