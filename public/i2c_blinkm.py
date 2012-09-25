from pytronics import i2cRead, i2cWrite
import json

FADE_TO = 0x63
GET_COLOR = 0x67
SET_COLOR = 0x6e
PLAY_SCRIPT = 0x70

# jargs = '[0, 73, 78]'
jargs = '[3, 1, 0]'
args = json.loads(jargs)
# print 'args ' + str(args)

# i2cWrite(0x09, 0x6f)
# i2cWrite(0x09, PLAY_SCRIPT, args, 'I')
# i2cWrite(0x09, SET_COLOR, args, 'I')
# i2cWrite(0x09, FADE_TO, args, 'I')

# Stop script
i2cWrite(0x09, 0x6f)
# Fade to
i2cWrite(0x09, 0x63, [0, 3, 4], 'I')



for i in range(20):
    result = i2cRead(0x09, GET_COLOR, 'I', 3)
    print 'result ' + str(result)
