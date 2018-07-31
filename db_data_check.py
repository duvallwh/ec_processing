"""Check for data in database then load data into database"""
import sqlite3
import pandas as pd
from data_loader_functions import *

def data_check_query(site, beginging_date, end_date):
    """Function assumes that all parameters have been loaded one day at a time.
    Need to write code for first day and last day corner cases"""

    begining_time_delta = time_delta(beginging_date)
    end_time_delta = time_delta(end_date)

    query = ("SELECT * FROM data WHERE date > " +
            str(begining_time_delta) +
            " AND WHERE date < " +
            str(end_time_delta) +
            " AND WHERE site = " +
            site)

    return query

def check_data(con, site, first_day, last_day):

    if first_day != pd.Timestamp:
        try:
            first_day = pd.to_datetime(first_day)
        except:
            return "bad 'first_day' parameter"
    if last_day != pd.Timestamp:
        try:
            last_day = pd.to_datetime(last_day)
        except:
            return "bad 'first_day' parameter"

    if first_day.month == last_day.month:
        list_of_days = []

    else:
        month_range = range(first_day.month, last_day.month + 1)
    
        



import unittest

class db_data_checkTest(unittest.TestCase):

    def test_check_query(self):
        test_query = 'SELECT * FROM data WHERE date > 0.0 AND WHERE date < 86400.0 AND WHERE site = site'
        test_begining_date = 
        test_end_date = 

