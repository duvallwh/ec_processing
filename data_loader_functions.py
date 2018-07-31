"""
Group of functions to be used to format data to be loaded into a
sqlite3 data base. The aim of these functions is to 
"""

import pandas as pd
import numpy as np

ORIGIN = pd.datetime(2018,1,1)

def time_delta(time_stamp):
    return (time_stamp - ORIGIN
            )/np.timedelta64(1,'s')

def format_dates(df, hour_offset=None, date_col=None):
    """Removes offset if necessary from df 'date' column"""

    if date_col:
        date_name = date_col
    else:
        date_name='date'

    df['date'] = df[date_name].apply(lambda x: x.tz_localize(None))
    if hour_offset:
        df['date'] = df['date'] - pd.DateOffset(hours=hour_offset)

    df['time_delta'] = df['date'].apply(time_delta)
        
    return df

def sql_loader_shape(df, site, averagingperiod, units_map):
    """Used to put dataframe into correct shape.
    missing units as they need to be mapped after data is melted"""
    df['site'] = site
    df['averagingperiod'] = averagingperiod
    df = pd.melt(df, id_vars=['date', 'time_delta', 'site', 'averagingperiod'],
                   var_name='parameter', value_name='reading')
    df['units'] = df['parameter'].map(units_map)
    return df

def organize_df(df):
    """Puts df columns in correct order to be loaded into sqlite3 db."""
    return df[['time_delta', 'site', 'parameter',
                 'units', 'averagingperiod', 'reading']]

def from_seconds(seconds):
    return ORIGIN + pd.to_timedelta(seconds, unit='s')

import unittest

class data_loader_functionsTest(unittest.TestCase):

    def test_from_seconds(self):
        test_date = pd.datetime(2018, 1, 1)
        x = from_seconds(0)
        self.assertEqual(test_date, x)

if __name__=="__main__":
    unittest.main()
