import datalogger

# This function aggregates data from log into log_byhour,
# inserting one row per hour with an average value for the hour
# The number of rows inserted into log_byhour is returned
# If any rows are inserted, rows older than 36 hours in log are deleted,
# thus preventing log from growing indefinitely
# This function is normally called from a @cron task in server.py

print datalogger.update_byhour()
