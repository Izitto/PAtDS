#wake gaming pc
import sys
from wakeonlan import send_magic_packet
def run():
    send_magic_packet('30.9C.23.85.09.AC')
    print("wake up link... GPC")