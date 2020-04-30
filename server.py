'''
Michael You

Client that interprets messages over ethernet to 
decode DDR dancepad inputs that are read by the Raspberry Pi
'''
import socket
from CONST import *
import win32api
import win32con
from time import sleep

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST_IP, HOST_PORT))
s.listen(NUM_DEVICES)

print('Waiting for new device...')
conn, addr = s.accept()
print('Connection address:', addr)

# win32api functions to press keys on windows
def pressAndHold(*args):
    '''
    press and hold. Do NOT release.
    accepts as many arguments as you want.
    e.g. pressAndHold('left_arrow', 'a','b').
    '''
    print('pressing ', args)
    for i in args:
        win32api.keybd_event(VK_CODE[i], 0,0,0)
        sleep(KEY_DELAY_TIME)

def release(*args):
    '''
    release depressed keys
    accepts as many arguments as you want.
    e.g. release('left_arrow', 'a','b').
    '''
    print('releasing', args)
    for i in args:
        win32api.keybd_event(VK_CODE[i],0 ,win32con.KEYEVENTF_KEYUP ,0)

# Processes incoming raw data from the dancepad
def process(data):
    data = data.decode(ENCODING).rstrip()
    print(data)
    l = data.split(DELIMITER)
    print(l)

    for x in range(len(l)//2):
        key_state, key_id = l[2*x], l[2*x+1]
        key_state = int(key_state)
        key_id = int(key_id)
        print(key_state, key_id)

        # TODO: select the proper controller
        controller = CONTROLLER_1

        if key_id == 316:
            print('detected', key_id)

        if key_id not in controller:
            pass

        if key_state == KEYSTATE_DOWN:
            pressAndHold(controller[key_id])
        elif key_state == KEYSTATE_UP:
            release(controller[key_id])

while 1:
    data = conn.recv(BUFFER_SIZE)

    # Disconnected, wait for new device
    if not data:
        print('Waiting for new device...')
        conn, addr = s.accept()
        print('Connection address:', addr)

    process(data)

conn.close()