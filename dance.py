'''
Michael You

DDR Konami dancepad USB decoder and event handler for 
                ASA Booth 2019: The Lorax
'''
import usb.core
import usb.util
import serial
import serial.tools.list_ports

from CONST import *

def decode(data):
  '''
  Decodes the data received from the DDR pad.

  Returns a 0/1 list containing whether or not each
  key was pressed or not
  '''
  arrow_data  = data[ARRAY_POS_ARROW]
  button_data = data[ARRAY_POS_BUTTON]

  # TODO: design a better data structure for this
  res = [
    # Arrow inputs
    (0x1 & arrow_data), 
    (0x2 & arrow_data)  >> 1,
    (0x4 & arrow_data)  >> 2,
    (0x8 & arrow_data)  >> 3,
    (0x10 & arrow_data) >> 4,
    (0x20 & arrow_data) >> 5,

    # Button inputs
    (0x10 & button_data) >> 4,
    (0x20 & button_data) >> 5,
    (0x40 & button_data) >> 6,
    (0x80 & button_data) >> 7,

    # RAW DATA
    arrow_data, 
    button_data
  ]

  # Just for debugging
  # print(res)

  return res

def process_data_arduino(dec_data):
  '''
  Processes the decoded data so it can be sent to the Arduino.

  Returns a byte data type to be written to the Arduino.
  '''
  res = 0
  for x in range(4):
    res = res << 1
    res += dec_data[x]

  return bytes([res])


def setup_arduino():
  '''
  Scans the ports for an Arduino (actually anything in the serial port)
  and returns the serial object
  '''

  print(list(serial.tools.list_ports.comports())[0][0])

  return serial.Serial(
    list(serial.tools.list_ports.comports())[0][0], 
    timeout=0
  )

def main():
  '''
  Initializes the DDR pad. Needs the vendor and product IDs, 
  which have to be found beforehand and put in constants.
  '''
  device = usb.core.find(idVendor=VID, idProduct=PID)

  # Use the first/default configuration
  device.set_configuration()

  # First endpoint
  endpoint = device[0][(0,0)][0]

  arduino = setup_arduino()

  # Read data
  while True:
    try:
      data = device.read(
        endpoint.bEndpointAddress,
        endpoint.wMaxPacketSize
      )

      # Show the received data
      dec_data = decode(data)
      arduino_data = process_data_arduino(dec_data)

      if dec_data[-1] + dec_data[-2] > 0:
        print(dec_data)
        arduino.write(arduino_data)
      
    except usb.core.USBError as e:
      data = None
      if e.args == ('Operation timed out',):
        continue

if __name__ == '__main__':
  main()