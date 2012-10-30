import datalogger

# The function getlog() is called to return data from the datalogger.
# The following periods can be requested:
#  'live' values averaged by minute for the past three hours (180 minutes)
#  'pastday' values averaged by ten minutes for the past 24 hours
#  'pastweek' values averaged by hour for the past seven days
# This function returns a JSON encoded string is normally called from a template
# (web page) via a $.post request to /getlog in server.py

print datalogger.getlog('live')
# print datalogger.getlog('pastday')
# print datalogger.getlog('pastweek')
