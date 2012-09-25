import sh
print sh.ifconfig('eth0')
# print sh.git('status')

print sh.ntpdate('uk.pool.ntp.org')
