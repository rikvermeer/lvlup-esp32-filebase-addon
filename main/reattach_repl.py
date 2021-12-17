import os, machine

def rates():
    return [115200, 230400, 460800, 576000, 921600]

def print_rates():
    print(rates())

def reattach(rate=115200):
    #os.dupterm(None, 0)
    uart = machine.UART(1, tx=1, rx=3 ,baudrate=rate)
    os.dupterm(uart, 0)

