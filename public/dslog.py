import sqlite3
import datetime

sql = """SELECT
    strftime('%Y-%m-%d 00:00:00', logdate) AS logdate,
    avg(value) AS value
FROM log_byhour
WHERE logdate < ?
GROUP BY strftime('%Y-%m-%d', logdate)
ORDER BY 1;"""

band = """SELECT
    max(value) AS max,
    min(value) AS min
FROM log_byhour
WHERE logdate < ?
GROUP BY strftime('%Y-%m-%d', logdate)
ORDER BY 1;"""

def getlog():
    import json
    data = {}
    con = sqlite3.connect('/var/log/datalog.db', detect_types=sqlite3.PARSE_DECLTYPES)
    with con:
        c = con.cursor()
        # Get endDate
        c.execute('SELECT MAX(logdate) FROM log_byhour;')
        endDate = c.fetchone()[0]
        if endDate == None:
            print 'No data'
        else:
            print 'endDate ' + endDate
            endDate = datetime.datetime.strptime(endDate, '%Y-%m-%d %H:%M:%S').date()
            print 'endDate {0}'.format(endDate)
        c.execute(sql, (endDate,))
        rr = c.fetchall()
        data['series'] = rr
        c.execute(band, (endDate,))
        rr = c.fetchall()
        data['band'] = rr
        return json.dumps(data)

print getlog()
