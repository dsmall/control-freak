import sqlite3
import datetime

def temperature(temp):
    logdate = datetime.datetime.utcnow()
    con = sqlite3.connect('/var/log/log.db')
    with con:
        cur = con.cursor()    
        cur.execute('DROP TABLE IF EXISTS templog;')
        cur.execute('CREATE TABLE templog(Id INTEGER PRIMARY KEY, logdate TIMESTAMP, temp REAL);')
        cur.execute('INSERT INTO templog (logdate, temp) VALUES(?, ?)', (logdate, temp))


temp = 21.2
temperature(temp)

con = sqlite3.connect('/var/log/log.db', detect_types=sqlite3.PARSE_DECLTYPES)
con.row_factory = sqlite3.Row
with con:
    c = con.cursor()
    c.execute('select * from templog;')
    r = c.fetchone()
    print 'Logdate: ' + r['logdate'].strftime('%a, %d %b %Y %H:%M %Z')
    print 'Temperature: {0}'.format(r['temp'])
    c.execute('delete from templog;')
