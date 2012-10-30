import datalogger

# Set one or both args to True to initialise
# These functions initialise the log tables, insert and
# print a test row, then delete it leaving the table empty
# WARNING: deletes all data

datalogger.init(False)
datalogger.init_byhour(False)
