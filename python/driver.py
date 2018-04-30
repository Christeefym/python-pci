#Distributed under the MIT licesnse.
#Copyright (c) 2011 Dave McCoy (dave.mccoy@cospandesign.com)

#Permission is hereby granted, free of charge, to any person obtaining a copy of
#this software and associated documentation files (the "Software"), to deal in
#the Software without restriction, including without limitation the rights to
#use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
#of the Software, and to permit persons to whom the Software is furnished to do
#so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import sys
import os
import time

from array import array as Array

class Driver(object):
    def __init__(self,
                 driver,
                 base_address,
                 debug):
        self.driver = driver
        self.debug = debug
        self.base_addr = base_address

    def __del__(self):
        pass

    def read_register(self, address):
        """read_register

        Reads a single register from the read command and then converts it to an
        integer

        Args:
          address (int):  Address of the register/memory to read

        Returns:
          (int): 32-bit unsigned register value

        Raises:
          NysaCommError: Error in communication
        """
        return self.read(address, 1)[0]

    def read(self, address, length = 1):
        """read

        Args:
          length (int): Number of 32 bit words to read from the FPGA
          address (int):  Address of the register/memory to read

        Returns:
          (Array of unsigned bytes): A byte array containtin the raw data
                                     returned from Nysa

        Raises:
          NysaCommError: Error in communication
        """
        address = int((self.base_addr + address) >> 2)
        return self.driver.read(address, length)

    def write_register(self, address, value):
        """write_register

        Writes a single register from a 32-bit unsingned integer

        Args:
          address (int):  Address of the register/memory to read
          value (int)  32-bit unsigned integer to be written into the register

        Returns:
          Nothing

        Raises:
          NysaCommError: Error in communication
        """
        self.write(address, [value])

    def write(self, address, data):
        """write

        Generic write command usd to write data to an Nysa image, this will be
        overriden based on the communication method with the specific FPGA board

        Args:
          address (int): Address of the register/memory to read
          data (array of unsigned bytes): Array of raw bytes to send to the
                                          device

        Returns:
          Nothing

        Raises:
          AssertionError: This function must be overriden by a board specific
          implementation
        """
        address = int((self.base_addr + address) >> 2)
        self.driver.write(address, data)

    def enable_register_bit(self, address, bit, enable):
        """enable_register_bit

        Pass a bool value to set/clear a bit

        Args:
          address (int): Address of the register/memory to modify
          bit (int): Address of bit to set (31 - 0)
          enable (bool): set or clear a bit

        Returns:
          Nothing

        Raises:
          NysaCommError: Error in communication
        """
        if enable:
            self.set_register_bit(address, bit)
        else:
            self.clear_register_bit(address, bit)

    def set_register_bit(self, address, bit):
        """set_register_bit

        Sets an individual bit in a register

        Args:
          address (int): Address of the register/memory to modify
          bit (int): Address of bit to set (31 - 0)

        Returns:
          Nothing

        Raises:
          NysaCommError: Error in communication
        """
        register = self.read_register(address)
        bit_mask =  1 << bit
        register |= bit_mask
        self.write_register(address, register)

    def clear_register_bit(self, address, bit):
        """clear_register_bit

        Clear an individual bit in a register

        Args:
          address (int): Address of the register/memory to modify
          bit (int): Address of bit to set (31 - 0)

        Returns:
          Nothing

        Raises:
          NysaCommError: Error in communication
        """
        register = self.read_register(address)
        bit_mask =  1 << bit
        register &= ~bit_mask
        self.write_register(address, register)

    def is_register_bit_set(self, address, bit):
        """is_register_bit_set

        returns true if an individual bit is set, false if clear

        Args:
          address (int): Address of the register/memory to read
          bit (int): Address of bit to check (31 - 0)

        Returns:
          (boolean):
            True: bit is set
            False: bit is not set

        Raises:
          NysaCommError
        """
        register = self.read_register(address)
        bit_mask =  1 << bit
        return ((register & bit_mask) > 0)

    def write_register_bit_range(self, address, high_bit, low_bit, value):
        """
        Write data to a range of bits within a register

        Register = [XXXXXXXXXXXXXXXXXXXXXXXH---LXXXX]

        Write to a range of bits within ia register

        Args:
            address (unsigned int): Address or the register/memory to write
            high_bit (int): the high bit of the bit range to edit
            low_bit (int): the low bit of the bit range to edit
            value (int): the value to write in the range

        Returns:
            Nothing

        Raises:
            NysaCommError
        
        """
        reg = self.read_register(address)
        bitmask = (((1 << (high_bit + 1))) - (1 << low_bit))
        reg &= ~(bitmask)
        reg |= value << low_bit
        self.write_register(address, reg)

    def read_register_bit_range(self, address, high_bit, low_bit):
        """
        Read a range of bits within a register at address 'address'

        Register = [XXXXXXXXXXXXXXXXXXXXXXXH---LXXXX]

        Read the value within a register, the top bit is H and bottom is L

        Args:
            address (unsigned int): Address or the register/memory to read
            high_bit (int): the high bit of the bit range to read
            low_bit (int): the low bit of the bit range to read

        Returns (unsigned integer):
            Value within the bitfield

        Raises:
            NysaCommError
            
        """
        value = self.read_register(address)
        bitmask = (((1 << (high_bit + 1))) - (1 << low_bit))
        value = value & bitmask
        value = value >> low_bit
        return value

