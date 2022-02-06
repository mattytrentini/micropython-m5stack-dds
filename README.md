
# micropython M5Stack DDS


```
>>> from machine import Pin, SoftI2C
>>> i2c = SoftI2C(scl=Pin(32), sda=Pin(26))
>>> i2c.scan()
[49]
>>> hex(49)
'0x31'
```

```
>>> i2c.readfrom_mem(0x31, 0x10, 6)
b'ad9833'
```