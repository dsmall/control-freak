import log

# This function aggregates data from templog into templog_byhour,
# inserting one row per hour with an average value for the hour
# The number of rows inserted into templog_byhour is returned
# If any rows are inserted, rows older than 36 hours in templog are deleted,
# thus preventing templog from growing indefinitely
# This function is normally called from a @cron task in server.py

print log.update_byhour()
