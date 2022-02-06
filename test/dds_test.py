import dds
from machine import Pin, SoftI2C
i2c = SoftI2C(scl=Pin(32), sda=Pin(26))
d = dds.DdsUnit(i2c)