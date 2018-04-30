from driver import Driver

class BlockRamDriver(Driver):

    def __init__(self, pcie_driver, base_address, debug = False):
        super(BlockRamDriver, self).__init__(pcie_driver, base_address, debug)

    def set_value(self, address, value):
        self.write_register(address << 2, value)

    def get_value(self, address):
        return self.read_register(address << 2)
