# Main entry points
    def _i2cRead(addr, reg = 0, size = '', length = 0):
        if debug: print '## i2cRead ## addr={0}, reg={1}, size={2}, length={3}'.format(addr, reg, size, length)
        file = os.open(RASCAL_I2C, os.O_RDWR)
        fcntl.ioctl(file, I2C_SLAVE, addr)
        if size.upper() == 'I' and length > 0:
            data = i2c_smbus_read_i2c_block_data(file, reg, length)
        elif size.upper() == 'W':
            data = i2c_smbus_read_word_data(file, reg)
        elif size.upper() == 'B':
            data = i2c_smbus_read_byte_data(file, reg)
        else:
            data = i2c_smbus_read_byte(file)
        os.close(file)
        return data

    def _i2cWrite(addr, reg, value = '', size = 'B'):
        if value == '': size = 'C'; value = 0
        if debug: print '## i2cWrite ## addr=0x{0:02x}, reg=0x{1:02x}, value=0x{2:04X}, size={3}'.format(addr, reg, value, size)
        file = os.open(RASCAL_I2C, os.O_RDWR)
        fcntl.ioctl(file, I2C_SLAVE, addr)
        if size.upper() == 'I' and isinstance(value, list) and len(value) > 0:
            data = i2c_smbus_write_i2c_block_data(file, reg, len(value), value)
        elif size.upper() == 'W':
            data = i2c_smbus_write_word_data(file, reg, value)
        elif size.upper() == 'B':
            data = i2c_smbus_write_byte_data(file, reg, value)
        else:
            data = i2c_smbus_write_byte(file, reg)
        os.close(file)
        return data
