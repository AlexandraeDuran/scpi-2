import numpy as np

class E4405B:
    """ Driver for Agilent E4405B spectrum Analysers. """

    def __init__(self, gpib):
     """ gpib: gpib interface, e.g. from EthGPIB.get_stream
     """
     self.gpib = gpib

    def identify(self):
        self.gpib.write("*IDN?\n".encode())
        return self.gpib.readline().decode()

    def find_peak(self, f0, freq, power, window=5.):
        """ Returns the index of the point with the highest power in the
        frequency range [f0-window/2.0, f0+window/2.0]. """

        lower_idx = np.argmin(np.abs(freq-(f0-window/2.)))
        upper_idx = np.argmin(np.abs(freq-(f0+window/2.)))

        peak = np.argmax(power[lower_idx:(upper_idx+1)]) + lower_idx
        return peak

    def get_sweep_axis(self):
        """ Returns a numpy array with the current frequency axis. """
        pts = self.get_sweep_pts()
        start = self.get_sweep_start()
        stop = self.get_sweep_stop()
        scale = self.get_sweep_scale()

        if scale == "lin":
            return np.linspace(start, stop, pts)
        elif scale == "log":
            return np.round(np.logspace(np.log10(start), np.log10(stop), pts))

    def set_sweep_span(self, span):
        """ Sets the frequency span in Hz. """
        self.gpib.write("FREQ:SPAN {}\n".format(span).encode())

    def get_sweep_span(self):
        """ Returns the frequency span in Hz. """
        self.gpib.write("FREQ:SPAN?\n".encode())
        return float(self.gpib.readline().decode())

    def set_sweep_start(self, start):
        """ Sets the frequency sweep start in Hz. """
        self.gpib.write("FREQ:START {}\n".format(start).encode())

    def get_sweep_start(self):
        """ Returns the frequency sweep start in Hz. """
        self.gpib.write("FREQ:START?\n".encode())
        return float(self.gpib.readline().decode())

    def set_sweep_stop(self, stop):
        """ Sets the frequency sweep stop in Hz. """
        self.gpib.write("FREQ:STOP {}\n".format(stop).encode())

    def get_sweep_stop(self):
        """ Returns the frequency sweep stop in Hz. """
        self.gpib.write("FREQ:STOP?\n".encode())
        return float(self.gpib.readline().decode())

    def set_sweep_centre(self, centre):
        """ Sets the frequency sweep centre in Hz. """
        self.gpib.write("FREQ:CENTER {}\n".format(centre).encode())

    def get_sweep_centre(self):
        """ Returns the frequency sweep centre in Hz. """
        self.gpib.write("FREQ:CENTER?\n".encode())
        return float(self.gpib.readline().decode())

    def set_sweep_pts(self, pts):
        """ Sets the number of points in the sweep. """
        self.gpib.write("SWEEP:POINTS {:d}\n".format(pts).encode())

    def get_sweep_pts(self):
        """ Returns the number of points in the sweep. """
        self.gpib.write("SWEEP:POINTS?\n".encode())
        return int(self.gpib.readline().decode())

    def set_sweep_scale(self, scale):
        """ Sets the frequency scale to either "lin" or "log"."""
        if not scale.lower() in ["lin", "log"]:
            raise ValueError("Unrecognised frequency scale.")
        self.gpib.write("SWEEP:SPACING {}\n".format(scale.upper()).encode())

    def get_sweep_scale(self):
        """ Returns either "lin" or "log". """
        self.gpib.write("SWEEP:SPACING?\n".encode())
        return self.gpib.readline().decode().lower()

    def get_trace(self):
        """ Returns the current trace in the amplitude units.  """
        self.gpib.write(":TRACE? TRACE1\n".encode())
        return np.array([
            float(pt) for pt in self.gpib.readline().decode().split(',')])


if __name__ == "__main__":
    import streams
    from time import sleep
    gpib = streams.EthGPIB("10.255.6.204")
    print("Connected to {}".format(gpib.get_version()))
    sa = E4405B(gpib.get_stream(18))

    freq = sa.get_sweep_axis()/1e6
    power = sa.get_trace()

    import matplotlib.pyplot as plt
    print("...")
    plt.plot(freq, power)
    plt.grid()
    plt.xlabel("Frequency (MHz)")
    plt.ylabel("Power (dBm)")
    plt.show()

