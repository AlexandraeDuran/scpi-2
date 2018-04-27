class Synth:
    """ Generic driver for single-channel synths, providing support for basic
    features. """

    def __init__(self, stream):
     """ Stream is an object providing a connection to the device and write,
     read and readline methods. For example, this can be an instance of
     pySerial.Serial of of any of the classes defined in scpi.streams.
     """
     self.stream = stream

    def identify(self):
        """ Return a device ID string. """
        self.stream.write("*IDN?\n".encode())
        return self.stream.readline().decode()

    def set_freq(self, freq):
        """ Program the device to a frequency in Hz. """
        self.stream.write("FREQ {} HZ\n".format(freq).encode())

    def get_freq(self):
        """ Returns the current frequency setting. """
        self.stream.write("FREQ?\n".encode())
        return self.stream.readline().decode()

    def set_power(self, power):
        self.stream.write("POW {} DBM\n".format(power).encode())

    def get_power(self):
        self.stream.write("POW?\n".encode())
        return float(self.stream.readline().decode())

    def set_rf_on(self, enabled):
        self.stream.write("OUTP {:d}\n".format(int(enabled)).encode())

    def get_rf_on(self):
        self.stream.write("OUTP?\n".encode())
        return bool(self.stream.readline().decode())

if __name__ == "__main__":
    import streams
    gpib = streams.EthGPIB("10.255.6.11")
    print("Connected to {}".format(gpib.get_version()))
    synth = Synth(gpib.get_stream(25))
    synth.set_rf_on(False)
    print(synth.get_rf_on())