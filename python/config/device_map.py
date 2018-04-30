import json
import os
import sys

DEFAULT_FILENAME="device_map.json"
DEFAULT_FILENAME=os.path.abspath(os.path.join(os.path.dirname(__file__), DEFAULT_FILENAME))


class DeviceMap(object):
    def __init__(self, debug=False):
        self.debug = debug
        if self.debug:
            print("Filaname: %s" % DEFAULT_FILENAME)
        file_in = open(DEFAULT_FILENAME)
        buf = file_in.read()
        self.config_dict = json.loads(buf)
        file_in.close()
        for k in self.config_dict:
            self.config_dict[k] = int(self.config_dict[k], 16)

        if self.debug:
            print("Device Map")
            for d in self.config_dict:
                print ("Device: %s: 0x%08X" % (d, self.config_dict[d]))

    def get_dict(self):
        return self.config_dict
