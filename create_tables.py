import sqlite3

def make_table(location):
    conn = sqlite3.connect(location)
    cur = conn.cursor()
    cur.execute("CREATE TABLE data(time_delta int, site text, "\
                "parameter text, units text, averagingperiod "\
                "text, reading real)")
    cur.execute("CREATE INDEX Idx3 ON data(time_delta, site, parameter)")
    conn.commit()
    conn.close()
