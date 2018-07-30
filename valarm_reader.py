"""Loads and parses data from zipped Valarm file in standard
format"""
import zipfile
import os
import pandas as pd
from data_loader_functions import *

class ValarmReader(object):
    def __init__(self, file_path):
        self.file_path = file_path
        
        self.unit1_map = {'AMB_TEMP_C': 'temp', 'REL_HUMID': 'rh',
                          'BAR_PRESS': 'bp', 'USER_1': 'piv_v',
                          'TEMP_1': 'sensor_temp', 'VOLT_1': 'ox_we',
                          'VOLT_2': 'ox_ae', 'VOLT_3': 'no_we',
                          'VOLT_4': 'no_ae', 'VOLT_5': 'no2_we',
                          'VOLT_6': 'no2_ae', 'VOLT_7': 'sensor_input_voltage',
                          'VOLT_8': 'system_voltage', 'TIME':'date'} 

        self.unit2_map = {'AMB_TEMP_C': 'temp', 'REL_HUMID': 'rh',
                          'BAR_PRESS': 'bp', 'VOLT_1': 'no_we',
                          'VOLT_2': 'no_ae', 'VOLT_3': 'no2_we',
                          'VOLT_4': 'no2_ae', 'VOLT_5': 'ox_we',
                          'VOLT_6': 'ox_ae', 'TEMP_1': 'sensor_temp',
                          'TIME':'date'}

        self.valarm_parameter_units_map = {'temp':'deg_C', 'rh':'percent', 'bp':'m_bars',
                                      'piv_v':'V', 'sensor_temp':'deg_C', 'ox_we':'V',
                                      'ox_ae':'V', 'no_we':'V', 'no_ae':'V', 'no2_we':'V',
                                      'no2_ae':'V', 'sensor_input_voltage':'deg_C',
                                      'system_voltage':'deg_C'}

    def _determine_sensor(self):
        """
        Determines which of two Valarm sensors using file_path.
        """
        
        if "SanAntonio_01" in self.file_path:
            return "val_site_1"
        
        elif "SanAntonio_02" in self.file_path:
            return "val_site_2"

        else:
            return "bad_file_name"
        
    def _open_file(self):
        """
        opens zipped valarm file and loads into pandas dataframe
        """

        zf = zipfile.ZipFile(self.file_path, 'r')
        return pd.read_csv(zf.open(str(zf.namelist()[0])),
                          parse_dates=['TIME'])
    
    def load_data(self):
        """
        returns data stored in zipped file listed in file_path
        """
        site = self._determine_sensor()
        if site == "val_site_1":
            unit_map = self.unit1_map
        elif site == "val_site_2":
            unit_map = self.unit2_map
        else:
            return 'Could not load data'

        dat = self._open_file()
        
        dat.rename(columns=unit_map, inplace = True)
        
        dat = dat[list(unit_map.values())]
        dat = format_dates(dat, hour_offset=7)
        dat = sql_loader_shape(dat, site=site, averagingperiod='spot',
                               units_map=self.valarm_parameter_units_map)
        dat = organize_df(dat)
        
        return dat        

###### to be moved ######

import unittest
#make sure to import os once this section is split out of the file
#import os 

class ValarmReaderTest(unittest.TestCase):

    def setUp(self):
        test_file_folder = "C:/Users/William/Downloads"
        test_file = "valarm-data_AQM_SanAntonio_02_2018-07-21_"\
                    "17.00.00-to-2018-07-29_16.59.01.zip"
        test_file_path = os.path.join(test_file_folder, test_file)
        self.vfp = ValarmReader(test_file_path)

    def tearDown(self):
        self.vfp = None           

    def test_determine_sensor(self):
        self.assertEqual("val_site_2", self.vfp._determine_sensor())

    def test_open_file(self):
        self.assertTrue(type(self.vfp._open_file()) == pd.core.frame.DataFrame)

    def test_load_data(self):
        self.assertTrue(type(self.vfp.load_data()) == pd.core.frame.DataFrame)

    def test_date_min(self):
        val_obj = self.vfp.load_data()
        date_min = val_obj['date'].min()
        self.assertEqual(pd.Timestamp('2018-07-22 00:01:11'), date_min)

    def test_time_delta(self):
        val_obj = self.vfp.load_data()
        time_delta_min = val_obj['time_delta'].min()
        self.assertEqual(time_delta_min, 17452871.0)

if __name__=="__main__":
    unittest.main()
        
