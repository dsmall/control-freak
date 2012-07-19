# Report functions available on i2c bus
import os, fcntl
from ctypes import *

RASCAL_I2C = '/dev/i2c-0'

I2C_FUNCS = 0x0705

I2C_FUNC_I2C = 0x00000001
I2C_FUNC_10BIT_ADDR = 0x00000002
I2C_FUNC_PROTOCOL_MANGLING = 0x00000004         # I2C_M_NOSTART etc.
I2C_FUNC_SMBUS_PEC = 0x00000008
I2C_FUNC_SMBUS_BLOCK_PROC_CALL = 0x00008000     # SMBus 2.0
I2C_FUNC_SMBUS_QUICK = 0x00010000
I2C_FUNC_SMBUS_READ_BYTE = 0x00020000
I2C_FUNC_SMBUS_WRITE_BYTE = 0x00040000
I2C_FUNC_SMBUS_READ_BYTE_DATA = 0x00080000
I2C_FUNC_SMBUS_WRITE_BYTE_DATA = 0x00100000
I2C_FUNC_SMBUS_READ_WORD_DATA = 0x00200000
I2C_FUNC_SMBUS_WRITE_WORD_DATA = 0x00400000
I2C_FUNC_SMBUS_PROC_CALL = 0x00800000
I2C_FUNC_SMBUS_READ_BLOCK_DATA = 0x01000000
I2C_FUNC_SMBUS_WRITE_BLOCK_DATA = 0x02000000
I2C_FUNC_SMBUS_READ_I2C_BLOCK = 0x04000000      # I2C-like block xfer 
I2C_FUNC_SMBUS_WRITE_I2C_BLOCK = 0x08000000     # w/ 1-byte reg. addr.

all_funcs = [
    ('I2C', I2C_FUNC_I2C),
    ('SMBus Quick Command', I2C_FUNC_SMBUS_QUICK),
    ('SMBus Send Byte', I2C_FUNC_SMBUS_WRITE_BYTE),
    ('SMBus Receive Byte', I2C_FUNC_SMBUS_READ_BYTE),
    ('SMBus Write Byte', I2C_FUNC_SMBUS_WRITE_BYTE_DATA),
    ('SMBus Read Byte', I2C_FUNC_SMBUS_READ_BYTE_DATA),
    ('SMBus Write Word', I2C_FUNC_SMBUS_WRITE_WORD_DATA),
    ('SMBus Read Word', I2C_FUNC_SMBUS_READ_WORD_DATA),
    ('SMBus Process Call', I2C_FUNC_SMBUS_PROC_CALL),
    ('SMBus Block Write', I2C_FUNC_SMBUS_WRITE_BLOCK_DATA),
    ('SMBus Block Read', I2C_FUNC_SMBUS_READ_BLOCK_DATA),
    ('SMBus Block Process Call', I2C_FUNC_SMBUS_BLOCK_PROC_CALL),
    ('SMBus PEC', I2C_FUNC_SMBUS_PEC),
    ('I2C Block Write', I2C_FUNC_SMBUS_WRITE_I2C_BLOCK),
    ('I2C Block Read', I2C_FUNC_SMBUS_READ_I2C_BLOCK),
]

debug = False
    
def i2c_functions():
    filename = RASCAL_I2C
    try:
        file = os.open(filename, os.O_RDWR)
        funcs = c_ulong(0)
        if debug: print 'Calling fcntl.ioctl on file for I2C_FUNCS'
        result = fcntl.ioctl(file, I2C_FUNCS, funcs)
        if debug: print 'result={0}'.format(result)
        if debug: print 'funcs value=0x{0:08X}'.format(funcs.value)
        if debug: print
        print 'Functions supported by {0}:'.format(filename)
        for i in range(0, len(all_funcs)):
            f = all_funcs[i]
            print '{0:<32s} {1}'.format(f[0], 'yes' if funcs.value & f[1] else 'no')
        os.close(file)
    except OSError:
        print 'Can\'t open {0}'.format(filename)
        return

i2c_functions()
