# Device info
VID = 0x05ac
PID = 0x828f

'''
start = 10
back = 20
up = 01
a = 14:00:10
down=14:02
left = 14:04
right=14:08
'''

# Wireshark sniffing
INTERFACE='XHC20'
GRANULARITY = 8

# Arduino Info
ARDUINO_SERIAL = '75735353338351911191'

# Decoding the dance pad
ARRAY_POS_ARROW  = 2
ARRAY_POS_BUTTON = 3

# Values from each arrow in ARRAY_POS_ARROW
ARROW_UP    = 0x1
ARROW_DOWN  = 0x2
ARROW_LEFT  = 0x4
ARROW_RIGHT = 0x8
ARROW_START = 0x10
ARROW_BACK  = 0x20

# Value from each button in ARRAY_POS_BUTTON
BUTTON_A = 0x10
BUTTON_B = 0x20
BUTTON_X = 0x40
BUTTON_Y = 0x80
