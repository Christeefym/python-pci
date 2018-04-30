#! /usr/bin/env python

# Copyright (c) 2017 Dave McCoy (dave.mccoy@cospandesign.com)
#
# NAME is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
#
# NAME is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NAME; If not, see <http://www.gnu.org/licenses/>.


import sys
import os
import argparse
import select
import pcie
from stream_fifo import StreamFIFO
from stream_fifo import StreamFIFOCommands as SFO
from array import array as Array
from config.get_device_map import DeviceMap

DM = DeviceMap().get_dict()

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
STREAM_FIFO_BASE = DM["h2d_fifo"]
DEFAULT_INTERRUPT = "4"


NAME = os.path.basename(os.path.realpath(__file__))

EVENT_INTERRUPT_DEVICE="/dev/xdma/card0/events%d"

DESCRIPTION = "\n" \
              "\n" \
              "Listen for interrupts from a given event file\n" \
              "\n" \
              "usage: %s [options]\n" % NAME

EPILOG = "\n" \
         "\n"


def listen_for_interrupts(device, debug=False):
        dfile = open(device, 'r', 0)
	while True:
		print "Waiting for a response from select"
		readable, writeable, exceptional = select.select([sys.stdin, dfile], [], [])
		for s in readable:
			if s is sys.stdin:
				print "Read from input, done!"
				return None
			else:
				data = dfile.read(4)
                data = Array('B', data)
                for d in data:
                    print "0x%02X " % d,
                return 0


def main(argv):
    #Parse out the commandline arguments
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=DESCRIPTION,
        epilog=EPILOG
    )

    parser.add_argument("-i", "--interrupt",
            nargs=1,
            default=[DEFAULT_INTERRUPT],
            help="Interrupt to test (DEFAULT: %s)" % DEFAULT_INTERRUPT)


    parser.add_argument("-d", "--debug",
            action="store_true",
            help="Enable Debug Messages")

    args = parser.parse_args()
    interrupt = int(args.interrupt[0], 0)
    interrupt_device = EVENT_INTERRUPT_DEVICE % interrupt
    print "Running Script: %s" % NAME
    print "Wait for an interrupt from the PCIE"
    print "This application would usually be run in a terminal while using another terminal to stimulate an interrupt using a GPIO device within the FPGA"
    print "Press 'return' to quit"

    retval = listen_for_interrupts(interrupt_device, args.debug)

if __name__ == "__main__":
    main(sys.argv)

