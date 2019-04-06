'''
Michael You

DDR Konami dancepad USB decoder and event handler for
                ASA Booth 2019: The Lorax

Program sniffs USB traffic using the XHC20 interface.
Intended for use on mac.

NOTE: I tried using pyusb, but for some reason the dancepads
      don't show up on the devices list on pyusb. They do
      show up in the system information for mac, so maybe
      there is some way to grab them? I already installed the
      XBOX360 controller drivers so I'm not entirely sure what's up.
'''
import pyshark
from CONST import *
import serial
import serial.tools.list_ports

def setup_arduino():
  '''
  Scans the ports for an Arduino matching the serial number
  and returns the serial object connecting to the Arduino
  '''
  ports = list(serial.tools.list_ports.comports())

  print('Serial Ports')
  print([p[0] for p in ports])

  arduino = [p[0] for p in ports if (ARDUINO_SERIAL == p.serial_number)][0]

  return serial.Serial(
    arduino,
    baudrate=9600,
    timeout=0
  )

def main():
    # Start sniffing XHC20 for USB interface data.
    # Notice that we only want to grab packets that are completed
    capture = pyshark.LiveCapture(interface=INTERFACE, display_filter='usb.darwin.request_type == 1')

    # Connect Arduino
    arduino = setup_arduino()

    ctr = 0
    pkts = []
    prev_pkt = 0
    new_pkt = 0

    # Process incoming packets
    for packet in capture.sniff_continuously():
        try:
            # Convert raw data to hex
            data = int(packet.data.usb_capdata[6:8], 16)
            pkts.append(data)
            ctr += 1

            if ctr == GRANULARITY:
                new_pkt = sum(pkts)

                # Edge detection
                if prev_pkt != new_pkt:
                    prev_pkt = new_pkt

                    if new_pkt != 0:
                        arduino.write(100)

                # Reset local capture
                pkts = []
                ctr = 0

        except Exception as e:
            print('Error', e)

if __name__ == '__main__':
  main()
