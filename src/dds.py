
from micropython import const
import struct

WAVE_SINE = const(1)
WAVE_TRIANGLE = const(2)
WAVE_SQUARE = const(3)
WAVE_SAWTOOTH = const(4)

DDS_UNIT_I2CADDR = const(0x31)
DDS_DESC_ADDR = const(0x10)
DDS_MODE_ADDR = const(0x20)
DDS_CTRL_ADDR = const(0x21)
DDS_FREQ_ADDR = const(0x30)
DDS_PHASE_ADDR = const(0x34)

DDS_FMCLK = const(10000000)
DDS_MAGIC_NUM = const(2**28)

class DdsUnit:
    def __init__(self, i2c, waveform_id=WAVE_SINE, frequency_hz=100_000):
        self._i2c = i2c
        self._waveform = waveform_id
        self._frequency = frequency_hz

        self._system_control = 0x00

    def identify(self):
        # Returns the serial number of the IC - should be "ad9833"
        return self._i2c.readfrom_mem(DDS_UNIT_I2CADDR, DDS_DESC_ADDR, 6)

    @property
    def waveform(self):
        return self._waveform

    @waveform.setter
    def waveform(self, waveform_id):
        if not WAVE_SINE <= waveform_id <= WAVE_SAWTOOTH:
            raise ValueError(f"Waveform must be between {WAVE_SINE} and {WAVE_SAWTOOTH} (inclusive)")

        self._waveform = waveform_id
        self._i2c.writeto_mem(
            DDS_UNIT_I2CADDR,
            DDS_MODE_ADDR,
            bytes([0x80 + waveform_id, 0x80 + self._system_control]),
        )

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, frequency_hz):
        if not 0 <= frequency_hz <= 10_000_000:
            raise ValueError("Frequency must be between 0Hz and 10MHz")

        self._frequency = frequency_hz
        frequency_hz = frequency_hz * DDS_MAGIC_NUM // DDS_FMCLK
        freq_struct = struct.pack(">i", 0x80000000 + frequency_hz)
        self._i2c.writeto_mem(DDS_UNIT_I2CADDR, DDS_FREQ_ADDR, freq_struct)


    def reset(self):
        pass
