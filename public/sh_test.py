import sh
# print sh.ifconfig('eth0')
# print sh.git('status')
# print sh.ntpdate('uk.pool.ntp.org')

print sh.ruby('--version')
print sh.ls('-1', '/var/www/public/templates')
