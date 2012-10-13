import sqlite3
import datetime

def temperature(temp):
    logdate = datetime.datetime.utcnow()
    try:
        con = sqlite3.connect('/var/log/log.db')
        with con:
            cur = con.cursor()    
            cur.execute('INSERT INTO templog (logdate, temp) VALUES(?, ?)', (logdate, temp))
    except Exception, e:
        print '## log.temperature ## {0}'.format(e)

sql_live = """SELECT
    strftime('%Y-%m-%d %H:%M GMT', logdate) AS logdate,
    avg(temp) AS temp
FROM templog
WHERE logdate >= datetime('now', '-180 minutes')
GROUP BY strftime('%Y-%m-%d %H:%M', logdate)
ORDER BY 1;"""

sql_pastday = """SELECT
    strftime('%Y-%m-%d %H:%M GMT', min(logdate)) AS logdate,
    avg(temp) AS temp
FROM templog
WHERE logdate >= datetime('now', '-24 hours')
GROUP BY strftime('%Y-%m-%d %H', logdate), strftime('%M', logdate) / 10
ORDER BY 1;"""

sql_pastweek = """SELECT
    strftime('%Y-%m-%d %H:%M GMT', logdate) AS logdate,
    temp
FROM templog_byhour
WHERE logdate >= datetime('now', '-7 days')
ORDER BY 1;"""

sql_update = """INSERT INTO templog_byhour
(logdate, temp)
SELECT
    strftime('%Y-%m-%d %H:00:00', logdate) AS logdate,
    avg(temp) AS temp
FROM templog
WHERE logdate >= ? AND logdate < ?
GROUP BY strftime('%Y-%m-%d %H', logdate)
ORDER BY 1;"""

def getlog(period):
    import json
    if period == 'pastweek':
        sql = sql_pastweek
    elif period == 'pastday':
        sql = sql_pastday
    else:
        sql = sql_live
    con = sqlite3.connect('/var/log/log.db', detect_types=sqlite3.PARSE_DECLTYPES)
    with con:
        c = con.cursor()
        c.execute(sql)
        rr = c.fetchall()
        return json.dumps(rr)

def update_byhour():
    con = sqlite3.connect('/var/log/log.db', detect_types=sqlite3.PARSE_DECLTYPES)
    with con:
        c = con.cursor()
        # Get startDate for incremental update
        c.execute('SELECT MAX(logdate) FROM templog_byhour;')
        startDate = c.fetchone()[0]
        if startDate == None:
            # Rascal24 arrival in UK
            startDate = datetime.datetime(2011, 12, 30)
        else:
            startDate = datetime.datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours = 1)
        # Get endDate
        c.execute("SELECT strftime('%Y-%m-%d %H:00:00','now');")
        endDate = c.fetchone()[0]    
        # Update templog_byhour
        c.execute(sql_update, (startDate, endDate))
        rows = c.rowcount
        if rows > 0:
            c.execute("DELETE FROM templog WHERE logdate < datetime('now', '-36 hours');")
            # print '## update_byhour ## deleted ' + str(c.rowcount)
        return rows

def init(confirm):
    if confirm:
        logdate = datetime.datetime.utcnow()
        temp = 21.2
        con = sqlite3.connect('/var/log/log.db')
        with con:
            cur = con.cursor()    
            cur.execute('DROP TABLE IF EXISTS templog;')
            cur.execute('CREATE TABLE templog(logdate TIMESTAMP, temp REAL);')
            cur.execute('INSERT INTO templog (logdate, temp) VALUES(?, ?)', (logdate, temp))
        # Read back row to check, then delete
        con = sqlite3.connect('/var/log/log.db', detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        with con:
            c = con.cursor()
            c.execute('select * from templog;')
            r = c.fetchone()
            print 'Logdate: ' + r['logdate'].strftime('%a, %d %b %Y %H:%M %Z')
            print 'Temperature: {0}'.format(r['temp'])
            c.execute('delete from templog;')
    else:
        print 'Set arg to True to initialise (deletes all data)'

def init_byhour(confirm):
    if confirm:
        logdate = datetime.datetime.utcnow()
        temp = 21.2
        con = sqlite3.connect('/var/log/log.db')
        with con:
            cur = con.cursor()    
            cur.execute('DROP TABLE IF EXISTS templog_byhour;')
            cur.execute('CREATE TABLE templog_byhour(logdate TIMESTAMP, temp REAL);')
            cur.execute('INSERT INTO templog_byhour (logdate, temp) VALUES(?, ?)', (logdate, temp))
        # Read back row to check, then delete
        con = sqlite3.connect('/var/log/log.db', detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        with con:
            c = con.cursor()
            c.execute('select * from templog_byhour;')
            r = c.fetchone()
            print 'Logdate: ' + r['logdate'].strftime('%a, %d %b %Y %H:%M %Z')
            print 'Temperature: {0}'.format(r['temp'])
            c.execute('delete from templog_byhour;')
    else:
        print 'Set arg to True to initialise (deletes all data)'

