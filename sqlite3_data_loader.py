"""Load data from pandas df to table. """

import sqlite3
import pandas as pd
from data_loader_functions import *

def add_to_data_table(df, con):
    df.to_sql('data', con=con, if_exists='append', index=False)
