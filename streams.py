""" pySerial-like interfaces to various communications channels, such as
GPIB and Ethernet. Allows drivers to be agnostic of the physical
connection to the device. """

import socket

class EthernetSocket():
    """ Simple wrapper of Ethernet sockets, giving them an interface that's
    compatible with pySerial.
    """
    def __init__(self, addr, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((addr, port))

    def readline(self):
        """ Read a line terminated by either \n. """
        data = b""
        while True:
            char = self.sock.recv(1)
            if char == b"\n":
                break

            data += char
        return data.rstrip(b"\r")

    def read(self):
        return self.sock.recv(1024)

    def write(self, data):
        self.sock.send(data)

class EthGPIB:
    """ Prologix Ethernet to GPIB adapter. """
    def __init__(self, eth_addr, gpib_addr=0):

        self.eth = EthernetSocket(eth_addr, 1234)

        self.eth.write("++savecfg 0\n".encode())
        self.eth.write("++auto 0\n".encode())

        self.gpib_addr = None
        self.set_addr(gpib_addr)

    def set_addr(self, gpib_addr=None):
        """ Set the controller to address the device at a given GPIB address.

        If gpib_addr is None we keep the current address. """
        if self.gpib_addr == gpib_addr or gpib_addr is None:
            return

        self.gpib_addr = gpib_addr
        self.eth.write("++addr {:d}\n".format(gpib_addr).encode())

    def get_version(self):
        """ Returns a device version string. """
        self.eth.write("++ver\n".encode())
        return self.eth.readline().decode()

    def write(self, data, gpib_addr=None):
        """ Send data to the device at gpib_addr.

        If gpib_addr is None, we write to the last address set.
        """
        self.set_addr(gpib_addr)
        self.eth.write(data)

    def get_stream(self, gpib_addr):
        """ Create an interface to the device at a given GPIB address."""
        return self.stream(self, gpib_addr)

    class stream:
        """ An interface to a GPIB device. """

        def __init__(self, bus, addr):
            self.bus = bus
            self.addr = addr

        def readline(self):
            """ Read a line terminated by either \n or \r. """
            self.bus.set_addr(self.addr)
            self.bus.eth.write("++read_eoi\n".encode())
            return self.bus.eth.readline()

        def read(self):
            self.bus.set_addr(self.addr)
            self.bus.eth.write("++read_eoi\n".encode())
            return self.bus.eth.read()

        def write(self, data):
            """ Read until an EOI is received. """
            self.bus.set_addr(self.addr)
            return self.bus.eth.write(data)


if __name__ == "__main__":
    gpib = EthGPIB("10.255.6.11")
    print("Connected to {}".format(gpib.get_version()))

