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
