"""Loads and parses data from zipped Valarm file in standard
format"""
import zipfile
import os
import pandas as pd

class ValarmReader(object):
    def __init__(self, file_path):
        self.file_path = file_path

        ## NEEDS TO BE UPDATED #################################################

        self.unit1_map = {'AMB_TEMP_C': 'temp', 'REL_HUMID': 'rh',
                          'BAR_PRESS': 'bp', 'USER_1': 'piv_v',
                          'TEMP_1': 'sensor_temp', 'VOLT_1': 'ox_we',
                          'VOLT_2': 'ox_ae', 'VOLT_3': 'no2_we',
                          'VOLT_4': 'no2_ae', 'VOLT_5': 'no_we',
                          'VOLT_6': 'no_ae', 'VOLT_7': 'sensor_input_voltage',
                          'VOLT_8': 'system_voltage'} 

        self.unit2_map = {'AMB_TEMP_C': 'temp', 'REL_HUMID': 'rh',
                          'BAR_PRESS': 'bp', 'USER_1': 'piv_v',
                          'TEMP_1': 'sensor_temp', 'VOLT_1': 'ox_we',
                          'VOLT_2': 'ox_ae', 'VOLT_3': 'no2_we',
                          'VOLT_4': 'no2_ae', 'VOLT_5': 'no_we',
                          'VOLT_6': 'no_ae', 'VOLT_7': 'sensor_input_voltage',
                          'VOLT_8': 'system_voltage'}

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
        dat.index = dat['TIME']
        dat.index = dat.index.tz_localize('UTC').tz_convert('US/Pacific')
        dat = dat.rename(columns=unit_map)
        dat = dat[list(unit_map.values())]
        dat['site'] = site
        return dat        

###### to be moved ######

import unittest
#make sure to import os once this section is split out of the file
#import os 

class ValarmReaderTest(unittest.TestCase):

    def setUp(self):
        print("Creating a new valarm file parser...")
        test_file_folder = "C:/Users/duvallwh/Downloads"
        test_file = "valarm-data_AQM_SanAntonio_02_2018-06-30_17.00.00"\
                    "-to-2018-07-26_16.59.01.zip"
        test_file_path = os.path.join(test_file_folder, test_file)
        self.vfp = val_obj = ValarmReader(test_file_path)

    def tearDown(self):
        print("Destroying the valarm file parser...")
        self.vfp = None           

    def test_determine_sensor(self):
        self.assertEqual("val_site_2", self.vfp._determine_sensor())

    def test_open_file(self):
        self.assertTrue(type(self.vfp._open_file()) == pd.core.frame.DataFrame)

    def test_load_data(self):
        self.assertTrue(type(self.vfp.load_data()) == pd.core.frame.DataFrame)

if __name__=="__main__":
    unittest.main()
        
