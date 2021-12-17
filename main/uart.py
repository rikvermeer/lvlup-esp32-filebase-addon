from machine import UART

#TX = from CPU to UI
#RX = from UI to CPU

# Reads captures button presses
# This reads on the ui_uart TX line
# cpu_uart RX reads recipies
cpu_uart = UART(1, baudrate=38400, tx=None, rx=27)

# Reads captures CPU answers (acks)
# This reads on the cpu_uart TX line
ui_uart = UART(2, baudrate=38400, tx=None, rx=26)

# For now only reading is allowed!
#import select
#timeout = 
#poll = select.poll()
#poll.register(cpu_uart, select.POLLIN)
#poll.poll(timeout)

chunks = ''
running = True
import etna_parser

def readloop():
    while running:
        chunk = cpu_uart.read()
        chunks = chunks + chunk

