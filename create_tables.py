import sqlite3

def make_table(location):
    conn = sqlite3.connect(location)
    cur = conn.cursor()
    cur.execute("create table data(date date, time_delta int, site text, "\
                "parameter text, units text, averagingperiod "\
                "text, reading real)")
    conn.commit()
    conn.close()
