from array import array
from pytronics import i2cRead
ta = array('H', [i2cRead(0x48, 0, 'W')])
ta.byteswap()
print 'Temperature {0:0.1f}{1}C'.format((ta[0] >> 4) * 0.0625, unichr(176))
