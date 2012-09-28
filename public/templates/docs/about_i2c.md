I2C Support on Rascal
=====================

--

### i2cWrite - set I2C registers

The i2cWrite function is

    i2cWrite(address, register, [value], [mode])

There are two required arguments.
*address* specifies the address of the chip on the I2C bus
and is an integer between 0x03 and 0x77 (3 to 119).
*register* specifies the address on that chip to write to
and is an integer between 0x00 and 0xFF (0 to 255).

The *value* parameter, if specified, is the value to write to that address on the chip.
If this parameter is omitted, then a **short write** is issued. For most chips,
this simply sets an internal pointer to the target location, but doesn’t actually write to it.
For a few chips though, in particular simple ones with a single register, 
this short write is an actual write, while for others it is equivalent to sending a command.
If the mode parameter is I (I2C block write), values are specified as a list.

The *mode* parameter, if specified, is one of the letters B, W, or I, corresponding to
a write size of a single byte, a 16-bit word, or an I2C block write, respectively.
For I2C block writes, the write size is determined by the length of the value list (range 1 to 32).
If the mode parameter is omitted, i2cWrite defaults to byte mode.
The value provided must be within range for the specified data type
(0x00-0xFF for byte and block writes, 0x0000-0xFFFF for words).
Another possible mode is C, which doesn’t write any value (the so-called short write).
You usually don’t have to specify this mode, as it is the default when no value is provided.

[ASSUME I when value is a list]
[ASSUME W when value is > 255]
[CHECK format of Python docs]

#### Examples

    result = i2cWrite(address, register, value, 'B')  - write byte value to register
    result = i2cWrite(address, register, value, 'W')  - write word value to register
    result = i2cWrite(address, register, list, 'I')  - write bytes from list to register
    result = i2cWrite(address, register, value, 'C')  - short write to register (value ignored)

You can leave out some of the arguments:

    result = i2cWrite(address, register) - short write to register (normally nothing written)
    result = i2cWrite(address, register, value)  - write byte value to register (value 0-255)
    result = i2cWrite(address, register, value)  - write word value to register (value > 255)
    result = i2cWrite(address, register, list)  - write bytes from list to register
