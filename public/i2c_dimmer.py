from pytronics import i2cRead, i2cWrite
import json

PCA_REGS = ['MODE1', 'MODE2',
    'PWM0', 'PWM1', 'PWM2', 'PWM3', 'PWM4', 'PWM5', 'PWM6', 'PWM7',
    'PWM8', 'PWM9', 'PWM10', 'PWM11', 'PWM12', 'PWM13', 'PWM14', 'PWM15',
    'GRPPWM', 'GRPFREQ',
    'LEDOUT0', 'LEDOUT1', 'LEDOUT2', 'LEDOUT3',
    'SUBADR1', 'SUBADR2', 'SUBADR3', 'ALLCALLADR']

PCA_INC_NONE = 0
PCA_INC_ALL = 0x80      # 0x00-0x1B (28)
PCA_INC_BRI = 0xA0      # 0x02-0x11 (16)
PCA_INC_GCR = 0xC0      # 0x12-0x13 (2)
PCA_INC_BRI_GCR = 0xE0  # 0x02-0x13 (18)

settings = i2cRead(0x40, PCA_INC_ALL | 0, 'I', 28)
print json.dumps(settings)

print 'Register  Name        Value'
for i in range(len(settings)):
    print '0x{0:02X}      {1:10s}  0x{2:02X}'.format(i, PCA_REGS[i], settings[i])
