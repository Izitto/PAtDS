#wake main pc
import sys
from wakeonlan import send_magic_packet
def run():
    send_magic_packet('2C.FD.A1.71.74.21')
    print("wake up link... MPC")