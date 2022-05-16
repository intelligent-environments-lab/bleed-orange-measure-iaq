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

import sys
import logging
import pathlib
import os

import pandas as pd
import numpy as np

from datetime import datetime

logger = logging.getLogger(__name__)
dir_path = pathlib.Path(__file__).resolve().parent
logging.basicConfig(filename=f'{dir_path}/data_purpleair.log', filemode='w', level=logging.INFO,
                    format='%(asctime)s: %(name)s (%(lineno)d) - %(levelname)s - %(message)s',datefmt='%m/%d/%y %H:%M:%S')

class Process:

    def __init__(self,pa_filename=None) -> None:
        """
        Processes data from a list of PurpleAir Devices

        Parameters
        ----------
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
        # import paths
        self.path_to_this_dir = f"{pathlib.Path(__file__).resolve().parent}"
        self.path_to_data = f"{pathlib.Path(__file__).resolve().parent.parent.parent}/data" # taking advantage of project filesystem
        
        if pa_filename is None: # look for meta data file
            try:
                meta = pd.read_csv(f"{self.path_to_data}/admin/purpleair_meta.csv")
                self.pa_list = list(meta["id"].values)
            except FileNotFoundError:
                logger.exception("No meta data available, creating empty list:")
                self.pa_list = []
        else: # assuming a str
            try: 
                id_file =  open(f"{self.path_to_data}/admin/{pa_filename}.txt")
                self.pa_list = id_file.read().split("\n")
            except FileNotFoundError:
                logger.exception("No text file available, creating empty list:")
                self.pa_list = []

if __name__ == '__main__':
    """ 
    Runs data processing scripts to turn raw data downloaded directly from devices into
        cleaned data ready to be analyzed (saved in processed).
    """