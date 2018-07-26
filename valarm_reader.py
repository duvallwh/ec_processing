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

    def determine_sensor(self):
        if "SanAntonio_01" in self.file_path:
            return "val_site_1"
        
        elif "SanAntonio_02" in self.file_path:
            return "val_site_2"

        else:
            return "bad_file_name"
        
    def open_file(self):
        pass

    def parse_data(self):
        pass

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

    def test_determine_sensor(self):
        self.assertEqual("val_site_2", self.vfp.determine_sensor())

    def test_open_file(self):
        self.assertTrue(type(self.vfp.open_file()) == pd.core.frame.DataFrame)

    def tearDown(self):
        print("Destroying the valarm file parser...")
        self.vfp = None           

if __name__=="__main__":
    unittest.main()
        
