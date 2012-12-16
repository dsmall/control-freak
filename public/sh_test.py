import sh
# print sh.ifconfig('eth0')
# print sh.git('status')
# print sh.ntpdate('uk.pool.ntp.org')

# print sh.ruby('--version')
# print sh.ls('-1', '/var/www/public/templates')
print sh.uptime()

from datetime import timedelta

with open('/proc/uptime', 'r') as f:
    uptime_seconds = float(f.readline().split()[0])
    
td = timedelta(seconds = uptime_seconds)



d = td.days
h = td.seconds//(60*60)
m = (td.seconds%(60*60))//60
print 'Up {0:d}d {1:02d}:{2:02d}:{3:02d}'.format(td.days, td.seconds//(60*60),
    (td.seconds%(60*60))//60, td.seconds%60)

