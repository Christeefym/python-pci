# Python PCIE

Python interface to PCIE using the Xilinx PCIE Driver.

This API uses the AXI Lite interface to read and write registers within the
FPGA. It is not meant for speed.


# Quickstart

* Make sure your XDMA driver is loaded
* Within base directory make the cpp pcie library
* run 'make', you should see this:

    Building Library
    g++ -o lib/libpypcie.so -Iinclude -I/usr/include -c -Wall -Werror -fpic src/python_pcie.cpp
    Compiling Test application object
    g++ -o obj/test.o -Iinclude -I/usr/include -c test/test.cpp
    Building Test application
    g++ -o build/test -Llib -lpypcie obj/test.o

* Go to: 'sip' directory
* run 'make', you should see this:

    g++ -c -g -O2 -fstack-protector-strong -Wformat -Werror=format-security  -Wdate-time -D_FORTIFY_SOURCE=2 -fPIC -Wall -W -DNDEBUG -I. -I/usr/include/python2.7 -o sippciecmodule.o sippciecmodule.cpp
    g++ -c -g -O2 -fstack-protector-strong -Wformat -Werror=format-security  -Wdate-time -D_FORTIFY_SOURCE=2 -fPIC -Wall -W -DNDEBUG -I. -I/usr/include/python2.7 -o sippcieuint64_t.o sippcieuint64_t.cpp
    g++ -c -g -O2 -fstack-protector-strong -Wformat -Werror=format-security  -Wdate-time -D_FORTIFY_SOURCE=2 -fPIC -Wall -W -DNDEBUG -I. -I/usr/include/python2.7 -o sippciePythonPCIE.o sippciePythonPCIE.cpp
    g++ -c -g -O2 -fstack-protector-strong -Wformat -Werror=format-security  -Wdate-time -D_FORTIFY_SOURCE=2 -fPIC -Wall -W -DNDEBUG -I. -I/usr/include/python2.7 -o sippciestdvector1400.o sippciestdvector1400.cpp
    g++ -c -g -O2 -fstack-protector-strong -Wformat -Werror=format-security  -Wdate-time -D_FORTIFY_SOURCE=2 -fPIC -Wall -W -DNDEBUG -I. -I/usr/include/python2.7 -o sippciestdvector1800.o sippciestdvector1800.cpp
    g++ -c -g -O2 -fstack-protector-strong -Wformat -Werror=format-security  -Wdate-time -D_FORTIFY_SOURCE=2 -fPIC -Wall -W -DNDEBUG -I. -I/usr/include/python2.7 -o sippciestdvector2000.o sippciestdvector2000.cpp
    g++ -Wl,-Bsymbolic-functions -Wl,-z,relro -shared -Wl,--version-script=pcie.exp -o pcie.so sippciecmodule.o sippcieuint64_t.o sippciePythonPCIE.o sippciestdvector1400.o sippciestdvector1800.o sippciestdvector2000.o -L../lib

* 'sudo make install', you shoud see this
    [sudo] password for <user>:
    cp -f pcie.so /usr/lib/python2.7/dist-packages/pcie.so

* using the 'address editor' within Vivado's block diagram find the address of a block ram
* edit python/config/device_map.json and change the address to your block ram ie if your block ram is at 0x00010000 change the 0x000E0000 to 0x00010000
* run 'python2 demo_block_ram_driver.py' you should see this:

    Demo Reading and Writing of Blockram over PCIE using Python
    Write 0x01233210 to address 0x00000000 (Relative to BRAM Base)
    Write 0xDEADBEAF to address 0x00000001 (Relative to BRAM Base)
    Read 0x01233210 from address 0x00000000 (Relative to BRAM Base)
    Read 0xDEADBEEF from address 0x00000001 (Relative to BRAM Base)


# Driver

An example 'driver' is availble to help write your own driver, it will simplify the process of reading and writing data to/from the FPGA.

The driver provides the following functions

* read: read 'length' number of 32-bit values from core
* write: write 'length' number of 32-bit values from the core
* read_register: Read a register value and return a simple integer
* write_register: Write a register value
* set_register_bit: 'set' a register bit within an address
* clear_register_bit: 'clear' a register bit within an address
* enable_register_bit: 'sets' or 'clears' a register bit within an address
* is_register_bit_set: returns true if a register bit is set within an address
* read_register_bit_range: returns an integer representing a register bit range
* write_register_bit_range: writes a range of bits into a register without modifying other bits in the register


An example 'block ram driver' is available to demonstrate the use of the driver class.


## NOTE: addresses need to be shifted by the user
The AXI Lite Addresses are 32-bit aligned and are not done by the low level driver. Instead the user must shift the address as can be demonstred by the 'block_ram_driver.py'

    def set_value(self, address, value):
        self.write_register(address << 2, value)


# DEMO Script

An example python script: 'demo_block_ram_driver.py' which writes two values to the BRAM and read them back


# Device Manager

In order to reduce the amount of script modification required to get this demo up and running the address of the BRAM should be entered into the JSON file:

    <base>/python/config/device_map.json

As an example the BRAM on this FPGA design is located at 0x000E0000 so I added an entry "bram":"0x000E0000" within the 'json' file adding another entry would look something like this ('gpio' @ address 0x000F0000)


    {
	    "bram":"0x000E0000",
      "gpio":"0x000F0000"
    }


# Interrupts

When using the XDMA driver users might want to employ interrupts to initiate communciations. There is another example application called 'test_interrupts.py' that will listen for interrupts from the FPGA.
The if run without arguments the script will wait for an interrupt on '4' which can be stimulated by raising the 4th bit 'usr_irq_req' the application will report this interrupt and then exit.

## Note on interrupts

I haven't researched this too much but it seems as though interrupt 0-3 are reserved for the driver itself, so it is recommended to only use interrupt 4 - 15

# NOTES about SIP

SIP is a tool to bind python to C and C++ its very useful but can be a headache to install and use so I've generated all the C++ files and, hopefully, any users who wish to use this will not be required to install SIP and instead just run 'make' and 'make install' within the 'sip' directory

