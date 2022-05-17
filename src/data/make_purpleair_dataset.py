# -*- coding: utf-8 -*-
# ----------------------
# Make AirThings Dataset
#
# Imports and processes
# raw data from the 
# PurpleAir sensors
# 
# Author: Hagen Fritz
# Date: 05/13/2022
# ----------------------

from ast import parse
from cmath import inf
from operator import index
import sys
import logging
import pathlib
import os
import argparse

import pandas as pd
import numpy as np

from datetime import datetime

sys.path.append(pathlib.Path(__file__).resolve().parent.parent.parent.as_posix())
from src.data import purpleair_data_retriever as pdr

logger = logging.getLogger(__name__)
dir_path = pathlib.Path(__file__).resolve().parent
logging.basicConfig(filename=f'{dir_path}/data_purpleair.log', filemode='w', level=logging.INFO,
                    format='%(asctime)s: %(name)s (%(lineno)d) - %(levelname)s - %(message)s',datefmt='%m/%d/%y %H:%M:%S')

class Process:

    def __init__(self,start_date,end_date,pa_filename=None) -> None:
        """
        Processes data from a list of PurpleAir Devices

        Parameters
        ----------
        start_date : str
            first day to consider for data processing in form "%Y%m%d" (inclusive)
        end_date : str
            last day to consider for data processing in form "%Y%m%d" (inclusive)
        pa_filename : str, default None
            name of file to read the PA ID names from.
            Default None indicates to look for meta data file

        Creates
        -------
        start_date : str
            first day to consider for data processing in form "%Y%m%d" (inclusive)
        end_date : str
            last day to consider for data processing in form "%Y%m%d" (inclusive)
        path_to_this_dir : str
            location of the folder this script is located in
        path_to_data : str
            location of the folder holding the data
        pa_list : list of str
            list of purple air device IDs
        """
        # getting datetime from str
        self.start_date = datetime.strptime(start_date,"%Y%m%d")
        self.end_date = datetime.strptime(end_date,"%Y%m%d")

        # import paths
        self.path_to_this_dir = f"{pathlib.Path(__file__).resolve().parent}"
        self.path_to_data = f"{pathlib.Path(__file__).resolve().parent.parent.parent}/data"
        self.path_to_meta = f"{pathlib.Path(__file__).resolve().parent.parent.parent}/references/meta_data"
        
        if pa_filename is None: # look for meta data file
            try:
                meta = pd.read_csv(f"{self.path_to_meta}/purpleair_meta.csv")
                self.pa_list = list(meta["id"].values)
            except FileNotFoundError:
                logger.exception("No meta data available, creating empty list:")
                self.pa_list = []
        else: # assuming a str
            try: 
                id_file =  open(f"{self.path_to_meta}/{pa_filename}.txt")
                self.pa_list = id_file.read().split("\n")
            except FileNotFoundError:
                logger.exception("No text file available, creating empty list:")
                self.pa_list = []

    def download(self):
        """
        Downloads data from the PurpleAirs using the BOMP source code 
        """
        # getting new str from datetime
        start_str = datetime.strftime(self.start_date,"%Y-%m-%d")
        end_str = datetime.strftime(self.end_date,"%Y-%m-%d")

        # downloading data
        pdr.main(start=start_str, end=end_str, channel='primaryA', save_location='data/interim/purpleair')

    def make_dataset(self):
        """
        Combines raw data from the purple air devices
        """
        combined = pd.DataFrame()
        for file in os.listdir(f"{self.path_to_data}/interim/purpleair/"):
            if file.endswith("v"):
                temp = pd.read_csv(f"{self.path_to_data}/interim/purpleair/{file}",index_col=0,parse_dates=True,infer_datetime_format=True)
                temp.rename(columns={
                    "PM1.0_CF1_ug/m3":"pm1_mass-microgram_per_m3",
                    "PM2.5_CF1_ug/m3":"pm2p5_mass-microgram_per_m3",
                    "PM10.0_CF1_ug/m3":"pm10_mass-microgram_per_m3",
                    "Temperature_F":"temperature_f",
                    "Humidity_%":"rh_percent"},
                    inplace=True)
                temp_filtered = temp.copy()[["pm1_mass-microgram_per_m3","pm2p5_mass-microgram_per_m3","pm10_mass-microgram_per_m3","temperature_f","rh_percent"]]
                temp_filtered["device"] = file.split(" ")[0]
                combined = pd.concat([combined,temp_filtered],axis=0)

        return combined

if __name__ == '__main__':
    """ 
    Runs data processing scripts to turn raw data downloaded directly from devices into
        cleaned data ready to be analyzed (saved in processed).
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', help="start date in format %Y%m%d", default="19000101", type=str)
    parser.add_argument('-e', help="end date in format %Y%m%d", default="22000101", type=str)
    #parser.add_argument('-f', help="filename to find IP addresses for devices", default="airthings_ips", type=str)
    args = parser.parse_args()

    processor = Process(start_date=args.s,end_date=args.e,ip_filename=args.f)
    processor.run()