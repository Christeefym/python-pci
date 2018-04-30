#! /usr/bin/env python

# Copyright (c) 2018 Dave McCoy (dave.mccoy@cospandesign.com)
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
import pcie
from block_ram_driver import BlockRamDriver
from config.device_map import DeviceMap

DM = DeviceMap().get_dict()
NAME = os.path.basename(os.path.realpath(__file__))


DEVICE_NAME_DEFAULT="/dev/xdma/card0/user"
#ADDR_MEM_BASE = 0x060000
ADDR_MEM_BASE = DM["bram"]
DEFAULT_SIZE = 0x200000

DESCRIPTION = "\n" \
              "\n" \
              "usage: %s [options]\n" % NAME

EPILOG = "\n" \
         "\n" \
         "Examples:\n" \
         "\t%s [%s]\n" \
         "\n" % (NAME, DEVICE_NAME_DEFAULT)

def test_mem(device, size, debug=False):
    p = pcie.PythonPCIE(debug)
    p.open_pcie(device, size)
    amm = BlockRamDriver(p, ADDR_MEM_BASE, debug)
    value = 0x01233210
    addr = 0x00000000
    print ("Write 0x%08X to address 0x%08X (Relative to BRAM Base)" % (value, addr))
    amm.set_value(addr, value)
    value = 0xDEADBEAF
    addr = 0x00000001
    print ("Write 0x%08X to address 0x%08X (Relative to BRAM Base)" % (value, addr))
    amm.set_value(0x01, 0xDEADBEEF)


    addr = 0x00000000
    data = amm.get_value(addr)
    print ("Read 0x%08X from address 0x%08X (Relative to BRAM Base)" % (data, addr))
    addr = 0x00000001
    data = amm.get_value(addr)
    print ("Read 0x%08X from address 0x%08X (Relative to BRAM Base)" % (data, addr))


def main(argv):
    #Parse out the commandline arguments
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=DESCRIPTION,
        epilog=EPILOG
    )

    parser.add_argument("--device",
            nargs=1,
            default=[DEVICE_NAME_DEFAULT],
            help="Listen for interrupts on this file default: %s" % DEVICE_NAME_DEFAULT)

    parser.add_argument("--size",
            nargs=1,
            default=[DEFAULT_SIZE],
            help="Listen for interrupts on this file default: 0x%08X" % DEFAULT_SIZE)


    parser.add_argument("-d", "--debug",
                        action="store_true",
                        help="Enable Debug Messages")

    args = parser.parse_args()
    size = args.size[0]
    device = args.device[0]
    print ("Demo Reading and Writing of Blockram over PCIE using Python")

    if args.debug:
        print ("test: %s" % device)
        print ("Size: 0x%08X" % size)

    test_mem(device, size, debug = args.debug)

if __name__ == "__main__":
    main(sys.argv)


