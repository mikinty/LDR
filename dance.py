import usb.core
import usb.util

from CONST import *

def main():
  device = usb.core.find(idVendor=VID, idProduct=PID)

  # use the first/default configuration
  device.set_configuration()

  # first endpoint
  endpoint = device[0][(0,0)][0]

  # read a data packet
  data = None
  while True:
    try:
      data = device.read(
        endpoint.bEndpointAddress,
        endpoint.wMaxPacketSize
      )

      # Show the received data
      print(data)
      
    except usb.core.USBError as e:
      data = None
      if e.args == ('Operation timed out',):
        continue

if __name__ == '__main__':
  main()