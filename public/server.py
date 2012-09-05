from flask import Flask, render_template, request
from uwsgidecorators import *
import time

public = Flask(__name__)
public.config['PROPAGATE_EXCEPTIONS'] = True

# config for upload
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
ALLOWED_DIRECTORIES = set(['static/uploads/', 'static/pictures/'])
LIVE_PINS = ['LED', '2', '3', '4', '5', '8', '9', '10', '11', '12', '13']
# public.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024

def toggle_pin(pin):
    from pytronics import digitalRead, digitalWrite
    if digitalRead(pin) == '1':
        digitalWrite(pin, 'LOW')
    else:
        digitalWrite(pin, 'HIGH')

@public.route('/pin/<pin>/<state>')
def update_pin(pin, state):
    from pytronics import digitalWrite, pinMode
    try:
        if state.lower() == 'on':
            digitalWrite(pin, 'HIGH')
            return 'Set pin %s high' % pin
        elif state.lower() == 'off':                       
            digitalWrite(pin, 'LOW')
            return 'Set pin %s low' % pin
        elif state.lower() == 'in':
            pinMode(pin,'INPUT')
            return 'Set pin %s input' % pin
        elif state.lower() == 'out':
            pinMode(pin,'OUTPUT')
            return 'Set pin %s output' % pin
        return "Something's wrong with your syntax. You should send something like: /pin/2/on"
    except:
        return 'Forbidden', 403

@public.route('/read-pins', methods=['POST'])
def read_pins():
    from pytronics import readPins
    import json
    return json.dumps(readPins(LIVE_PINS))

@public.route('/i2cget/<addr>/<reg>/<mode>')
def i2cget(addr, reg, mode):
    from pytronics import i2cRead
    iaddr = int(addr, 0)
    ireg = int(reg, 0)
    try:
        res = i2cRead(iaddr, ireg, mode)
        print '## i2cget ## {0}'.format(res)
        return str(res)
    except (OSError, IOError) as e:
        import errno
        print '## i2cget ## Error: [{0}] {1}'.format(errno.errorcode[e.errno], e.strerror)
        return str(-1)
    except Exception as e:
        return 'Internal server error', 500

@public.route('/i2cset/<addr>/<reg>/<val>/<mode>')
def i2cset(addr, reg, val, mode):
    from pytronics import i2cWrite
    iaddr = int(addr, 0)
    ireg = int(reg, 0)
    ival = int(val, 0)
    try:
        i2cWrite(iaddr, ireg, ival, mode)
        print '## i2cset ##'
        return str(0)
    except (OSError, IOError) as e:
        import errno
        print '## i2cset ## Error: [{0}] {1}'.format(errno.errorcode[e.errno], e.strerror)
        return str(-1)
    except Exception as e:
        return 'Internal server error', 500

@public.route('/i2cscan', methods=['POST'])
def i2cscan():
    from i2c import scanBus
    import json
    return json.dumps(scanBus())

#@rbtimer(60)
def fetch_calendar(num):
    import thermostat
    thermostat.update_calendar_file()
    print('Calendar reload attempt')

#@rbtimer(3)
def update_relay(num):
    import pytronics, thermostat
    actual = float(thermostat.read_sensor(0x48)) * 1.8 + 32.0
    target = float(thermostat.get_target_temp('/var/www/public/static/basic.ics', 'America/New_York'))
    print("Measured temperature: %f degrees. Target is %f degrees." % (actual, target))
    if actual < target:
        pytronics.digitalWrite(2, 'HIGH')
        print("Heat on")
    else:
        pytronics.digitalWrite(2, 'LOW')
        print("Heat off")

@public.route('/<template_name>.html')
def template(template_name):
    return render_template(template_name + '.html', magic="Hey presto!")

@public.route('/relay.html')
def index():
    import pytronics
    pin = pytronics.digitalRead(2)
    (chan0, chan1, chan2, chan3) = pytronics.summarize_analog_data()
    return render_template('/relay.html', chan0=chan0, chan1=chan1, chan2=chan2, chan3=chan3, pin=pin)

@public.route('/toggle', methods=['POST'])
def toggle():
    import pytronics
    if(request.form['target_state'] == '1'):
        pytronics.digitalWrite(2, 'HIGH')
        result = 'Pins set high'
    elif(request.form['target_state'] == '0'):
        pytronics.digitalWrite(2, 'LOW')
        result = 'Pins set low'
    else:
        result = 'Target_state is screwed up'
    return result

@public.route('/temperature', methods=['POST'])
def temperature():
    import json, thermostat
    data = {
        "time" : float(time.time()),
        "actual" : float(thermostat.read_sensor(0x48)),
        "target" : thermostat.get_target_temp('/var/www/public/static/basic.ics', 'America/New_York')
    }
    return json.dumps(data)

@public.route('/analog', methods=['POST'])
def analog():
    from pytronics import analogRead
    import json, time
    try:
        ad_ref = float(request.form['adref'])
    except KeyError:
        ad_ref = 3.3
    data = {
        "time" : float(time.time()),
        "A0" : float(analogRead('A0')) * ad_ref / 1024.0
    }
    return json.dumps(data)

@public.route('/send-to-lcd', methods=['POST'])
def send_to_lcd():
    import pytronics
    pytronics.serialWrite(request.form['serial_text'], 9600)
    return render_template('/lcd.html')

@public.route('/clear-lcd', methods=['POST'])
def clear_lcd():
    import pytronics
    pytronics.serialWrite(chr(0xFE) + chr(0x01), 9600)
    return render_template('/lcd.html')

@public.route('/set-color', methods=['POST'])
def set_color():
    import colorsys, kinet, subprocess
    color = request.form['color']
    print "RGB = " + str(color)
    #cmd = 'blinkm set-rgb -d 9 -r ' + str(int(color[0:2], 16)) + ' -g ' + str(int(color[2:4], 16)) + ' -b ' + str(int(color[4:6], 16))
    #subprocess.Popen([cmd], shell=True)
    pds = kinet.PowerSupply("192.168.10.57")
    pds.append(kinet.FixtureRGB(0))
    hsv = (colorsys.rgb_to_hsv(int(color[0:2], 16)/255.0, int(color[2:4], 16)/255.0, int(color[4:6], 16)/255.0))
    print "HSV = " + str(hsv)
    pds[0].hsv = hsv
    pds.go()
    return ('color sent to Blinkm and CK box')

@public.route('/sms', methods=['POST'])
def parse_sms():
    import subprocess
    message = request.form['Body']
    print "Received text message: " + str(message)
    f = open('/var/www/public/thermostat-target.txt', 'w')
    f.write(str(message))
    f.close()
    return ('Message processed')

@public.route('/sprinkler', methods=['POST'])
def sprinkler():
    import pytronics
    command = request.form['command']
    if(command == "ON"):
        pytronics.digitalWrite(2, 'HIGH')
    else:
        pytronics.digitalWrite(2, 'LOW')
    return ('Sprinkler toggled')

##### The following procedures support sending email via SMTP #####
# They are used by email.html. Configure smtp settings in smtp_lib.py
@public.route('/')
@public.route('/email.html')
def email_form():
    import smtp_lib
    return render_template('email.html', sender=smtp_lib.sender(), help=smtp_lib.help())

@public.route('/send-email', methods=['POST'])
def send_email():
    import smtp_lib, json
    sender = request.form['sender'].strip()
    recipients = request.form['recipients'].strip()
    subject = request.form['subject'].strip()
    body = request.form['body'].strip()
    if sender == '':
        result = (1, 'Please enter the sender')
    elif recipients == '':
        result = (1, 'Please enter at least one recipient')
    else:
        result = smtp_lib.sendmail(sender, recipients, subject, body)
    data = {
        "status" : int(result[0]),
        "message" : result[1]
    }
    return json.dumps(data)
##### End of email procedures

##### The following procedures support file upload #####
# They are called from rascal-1.03.js and used by upload-cf.html, upload-dd.html and album.html
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_folder(folder):
    return folder in ALLOWED_DIRECTORIES

@public.route('/xupload', methods=['POST'])
def xupload_file():
    import os
    from werkzeug import secure_filename
    from werkzeug.exceptions import RequestEntityTooLarge
    if request.method == 'POST':
        try:
            root = '/var/www/public/'
            # Check file type and folder
            filename = secure_filename(request.headers['X-File-Name'])
            if not allowed_file(filename):
                print '## xupload ## bad file type ' + filename
                return 'Forbidden', 403
            try:
                folder = request.headers['X-Folder']
            except:
                folder = ''
            if not allowed_folder(folder):
                print '## xupload ## bad folder ' + folder
                return 'Forbidden', 403
            fpath = os.path.join(root, os.path.join(folder, filename))
            # Write out the stream
            f = file(fpath, 'wb')
            f.write(request.stream.read())
            f.close()
            print '## xupload ## ' + fpath
        except RequestEntityTooLarge:
            return 'File too large', 413
        except:
            return 'Bad request', 400
    return 'OK', 200

@public.route('/list-directory', methods=['POST'])
def list_directory():
    import os, json
    root = '/var/www/public/'
    dir = request.form['directory']
    try:
        dirlist = os.listdir(os.path.join(root, dir))
        return json.JSONEncoder().encode(dirlist)
    except OSError:
        return 'Not Found', 404
    except Exception, e:
        print '## list_directory ## {}'.format(e)
    return 'Bad request', 400

@public.route('/clear-directory', methods=['POST'])
def clear_directory():
    import os
    root = '/var/www/public/'
    dir = request.form['directory']
    if dir not in ALLOWED_DIRECTORIES:
        return 'Forbidden', 403
    folder = os.path.join(root, dir)
    try:
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception, e:
                print '## clear_directory ## {}'.format(e)
                return 'Bad request', 400
        return 'OK', 200
    except OSError:
        return 'Not Found', 404
    except Exception, e:
        print '## clear_directory ## {}'.format(e)
    return 'Bad request', 400
##### End of upload procedures #####

# Called from hello.html
@public.route('/flash_led', methods=['POST'])
def flash_led():
    from pytronics import digitalRead, digitalWrite
    if digitalRead('LED') == '1':
        digitalWrite('LED', 'LOW')
        message = "LED off"
    else:
        digitalWrite('LED', 'HIGH')
        message = "LED on"
    return (message)

# Called from hello-TMP102.html
@public.route('/read_temp', methods=['POST'])
def read_temp():
    from pytronics import i2cRead
    try:
        temp = i2cRead(0x48, 0, 'I', 2)
        strTemp = '{0:0.1f}{1}C'.format(((temp[0] << 4) | (temp[1] >> 4)) / 16.0, unichr(176))
        return strTemp
    except (OSError, IOError) as e:
        import errno
        print '## i2cget ## Error: [{0}] {1}'.format(errno.errorcode[e.errno], e.strerror)
        return 'Can\'t read from TMP102 (see log)'
    except Exception as e:
        return 'Internal server error', 500

# dsmall private branch
@rbtimer(5)
def toggle_led(num):
    from pytronics import digitalRead, digitalWrite
    if digitalRead('LED') == '1':
        digitalWrite('LED', 'LOW')
    else:
        digitalWrite('LED', 'HIGH')

@cron(0, -6, -1, -1, -1)
def ntp_daemon(num):
    import subprocess
    cmd = 'ntpdate uk.pool.ntp.org'
    subp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    try:
        data = subp.communicate()[0].strip()
        print '## NTPD ## ' + data
    except:
        print '## NTPD ## Failed.'

@public.route('/scope_analog', methods=['POST'])
def scope_analog():
    from pytronics import analogRead, digitalRead, i2cRead
    import json, time
    try:
        ad_ref = float(request.form['adref'])
    except KeyError:
        ad_ref = 3.3
    if digitalRead('LED') == '1':
        strLED = "LED is on"
    else:
        strLED = "LED is off"
    temp = i2cRead(0x48, 0, 'I', 2)
    strTemp = '{0:0.1f}{1}C'.format(((temp[0] << 4) | (temp[1] >> 4)) * 0.0625, unichr(176))
    data = {
        "time" : float(time.time()),
        "A0" : float(analogRead('A0')) * ad_ref / 1024.0,
        "date" : time.strftime("%d %b %Y %H:%M:%S %Z", time.localtime()),
        "led" : strLED,
        "temp" : strTemp
    }
    return json.dumps(data)

# Reload editor button
@public.route('/reload', methods=['POST'])
def reload():
    import subprocess
    res = subprocess.call(['touch', '/etc/uwsgi/editor.ini'])
    if res <> 0:
        return 'Bad request', 400
    return 'OK', 200

headlines = ['No news']
lastUpdate = 12

@rbtimer(5)
def update_lcd(num):
    from pytronics import i2cRead
    from i2c_lcd import reset, writeString, setCursor
    import time
    reset()
    writeString(time.strftime("%H:%M:%S %Z", time.localtime()))
    setCursor(1, 0)
    temp = i2cRead(0x48, 0, 'I', 2)
    writeString('Temp {0:0.1f}'.format(((temp[0] << 4) | (temp[1] >> 4)) * 0.0625))
    writeString(chr(0xdf) + 'C')

@public.route('/send-to-i2c-lcd', methods=['POST'])
def send_to_i2c_lcd():
    from i2c_lcd import reset, writeString, setCursor
    reset()
    writeString(request.form['line1'])
    setCursor(1, 0)
    writeString(request.form['line2'])
    return 'OK', 200

@public.route('/clear-i2c-lcd', methods=['POST'])
def clear_i2c_lcd():
    from i2c_lcd import reset
    reset()
    return 'OK', 200

headlines = [ { 'title' : 'No news yet' } ]
lastFeed = 0
lastSlot = 20
lastUpdate = 'Not known'

@public.route('/headlines', methods=['POST'])
def headlines():
    global headlines, lastFeed, lastSlot, lastUpdate
    from pytronics import i2cRead
    from news import getHeadlines
    import json, time
    try:
        feed = int(request.form['feed'])
    except KeyError:
        feed = 0
    temp = i2cRead(0x48, 0, 'I', 2)
    strTemp = '{0:0.1f}{1}C'.format(((temp[0] << 4) | (temp[1] >> 4)) * 0.0625, unichr(176))
    now = time.localtime()
    # Update headlines every five minutes
    slot = now.tm_min / 5
    if feed != lastFeed or slot != lastSlot:
        headlines = getHeadlines(feed)
        lastFeed = feed
        lastSlot = slot
        lastUpdate = time.strftime("%H:%M %Z", now)
        updated = True
    else:
        updated = False
    data = {
        "date" : time.strftime("%a, %d %b %Y %H:%M %Z", now),
        "temp" : strTemp,
        "headlines" : headlines,
        "updated" : updated,
        "lastUpdate" : lastUpdate
    }
    return json.dumps(data)

def BCD(b):
    return ((b / 10) << 4) + (b % 10)

def set_rtc ():
    import subprocess
    import time
    from pytronics import i2cWrite
    cmd = 'ntpdate uk.pool.ntp.org'
    subp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    try:
        data = subp.communicate()[0].strip()
        t = time.gmtime()
        rtc = []
        rtc.append(BCD(t.tm_sec))
        rtc.append(BCD(t.tm_min))
        rtc.append(BCD(t.tm_hour))
        rtc.append(BCD(t.tm_wday + 1))
        rtc.append(BCD(t.tm_mday))
        rtc.append(BCD(t.tm_mon))
        rtc.append(BCD(t.tm_year - 2000))
        i2cWrite(0x68, 0, rtc, 'I')
        # Reset OSF (oscillator stopped flag)
        i2cWrite(0x68, 0x09, 0, 'B')
    except:
        print '## set_rtc ## Failed to set time'

@public.route('/rtc', methods=['POST'])
def rtc():
    from pytronics import i2cRead, i2cWrite
    import json
    if 'command' in request.form:
        command = request.form['command']
        if command == 'set_rtc':
            set_rtc()
        elif command == 'start':
            i2cWrite(0x68, 0, i2cRead(0x68, 0) & 0x7f)
        elif command == 'stop':
            i2cWrite(0x68, 0, i2cRead(0x68, 0) | 0x80)
        elif command == 'reset':
            i2cWrite(0x68, 0, [0x80, 0, 0], 'I')
    return json.dumps(i2cRead(0x68, 0, 'I', 7))

PCA_INC_NONE = 0
PCA_INC_ALL = 0x80      # 0x00-0x1B (28)
PCA_INC_BRI = 0xA0      # 0x02-0x11 (16)
PCA_INC_GCR = 0xC0      # 0x12-0x13 (2)
PCA_INC_BRI_GCR = 0xE0  # 0x02-0x13 (18)

@public.route('/dimmer', methods=['POST'])
def dimmer():
    from pytronics import i2cRead, i2cWrite
    import json
    try:
        if 'command' in request.form:
            command = request.form['command']
            if command == 'read_status':
                return json.dumps(i2cRead(0x40, PCA_INC_ALL | 0, 'I', 28))
            elif command == 'set_brightness':
                ireg = int(request.form['register'], 0)
                ival = int(request.form['value'], 0)
                i2cWrite(0x40, ireg, ival, 'B')
                return 'OK', 200
    except Exception as e:
        print '## dimmer ##: {0}'.format(e)
    return 'Internal server error', 500

# end dsmall private

if __name__ == "__main__":
    public.run(host='127.0.0.1:5000', debug=True)
