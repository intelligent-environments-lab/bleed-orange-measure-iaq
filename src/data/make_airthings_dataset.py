# -*- coding: utf-8 -*-
# ----------------------
# Make AirThings Dataset
#
# Imports and processes
# raw data from the 
# AirThings Beacons
# 
# Author: Hagen Fritz
# Date: 03/29/2022
# ----------------------

from importlib.resources import path
import sys
import logging
import pathlib
import os
from tracemalloc import start

import pandas as pd
import numpy as np

from datetime import datetime

class Process:
    """
    Processes data from a list of AirThings Devices
    """

    def __init__(self,start_date,end_date,ip_filename="airthings_ips") -> None:
        """
        Parameters
        ----------
        start_date : str
            first day to consider for data processing in form "%Y%m%d" (inclusive)
        end_date : str
            last day to consider for data processing in form "%Y%m%d" (inclusive)
        ip_filename : str, default "airthings_ips"
            filename to find the list of IP addresses

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
        logger : logging Handler
            logging Handler used for debugging/monitoring
        ips : list of str
            IP addresses of devices to consider
        """
        # dates
        self.start_date = datetime.strptime(start_date,"%Y%m%d")
        self.end_date = datetime.strptime(end_date,"%Y%m%d")

        # import paths
        self.path_to_this_dir = f"{pathlib.Path(__file__).resolve().parent}"
        self.path_to_data = f"{pathlib.Path(__file__).resolve().parent.parent.parent}/data" # taking advantage of project filesystem
        
        # logging
        self.logger = setup_logging() if not logging.getLogger().hasHandlers() else logging.getLogger()
        self.logger.info('making final data set from raw data')
        
        # IP Addresses
        try:
            ip_file =  open(f"{self.path_to_this_dir}/{ip_filename}.txt")
            self.ips = ip_file.read().split("\n")
        except FileNotFoundError:
            self.logger.exception(f"no {ip_filename}.txt found - please create this file in the same directory")
            self.ips = []

    def download(self,ip_address,path_to_raw="/home/pi/DATA/"):
        """
        Downloads data from an individual AirThings Beacon

        Parameters
        ----------
        ip_address : str
            Tailscale IP address for an AirThings Beacon
        path_to_raw : str, default /home/pi/DATA/
            location of the data on the AirThings Beacon

        Returns
        -------
        <void>
        """
        self.logger.info(f"downloading data from Device {ip_address}")
        os.system(f'scp -r -o ConnectTimeout=3 pi@{ip_address}:{path_to_raw} {self.path_to_data}/interim/')

    def make_dataset(self):
        """
        Combines data from AirThings Beacons

        Creates
        -------
        processed : DataFrame
            data from each AirThings Beacon
        """
        self.logger.info("generating dataset")
        if len(self.ips) > 0:
            for ip in self.ips:
                self.download(ip)

            combined = pd.DataFrame()
            for file in os.listdir(f"{self.path_to_data}/interim/DATA/"):
                if file[-1] == "v": # csV files
                    file_date = datetime.strptime(f"{file.split('-')[1]}{file.split('-')[2]}{file.split('-')[3].split('.')[0]}","%Y%m%d")
                    if file_date >= self.start_date and file_date <= self.end_date:
                        device = file.split("-")[0]
                        temp = pd.read_csv(f"{self.path_to_data}/interim/DATA/{file}",parse_dates=["timestamp"],infer_datetime_format=True)
                        temp["device"] = device

                        combined = combined.append(temp)

            # processing
            combined.sort_values(["device","timestamp"],inplace=True)
            combined.set_index("timestamp",inplace=True)
            # saving processed data as class object
            self.processed = combined
            # deleting interim data
            os.system(f"rm -r {self.path_to_data}/interim/DATA/")
        else:
            logging.error("No IP addresses to read from")

    def save(self):
        """
        Saves the class dataset to path
        """
        self.logger.info("saving dataset")
        try:
            data_start_date = datetime.strftime(min(self.processed.index).date(),"%Y%m%d")
            data_end_date = datetime.strftime(max(self.processed.index).date(),"%Y%m%d")
            self.processed.to_csv(f"{self.path_to_data}/processed/airthings-data-{data_start_date}-{data_end_date}.csv")
        except AttributeError:
            self.logger.exception("need to make the dataset first")

    def run(self):
        """
        Runner for the Process class
        """
        self.make_dataset()
        self.save()

def setup_logging():
    """
    Sets up logger
    """
    # Create a custom logger
    logger = logging.getLogger(__name__)
    dir_path = pathlib.Path(__file__).resolve().parent
    logging.basicConfig(filename=f'{dir_path}/data_airthings.log', filemode='w', level=logging.INFO,
                        format='%(asctime)s: %(name)s (%(lineno)d) - %(levelname)s - %(message)s',datefmt='%m/%d/%y %H:%M:%S')

    return logger

if __name__ == '__main__':
    """ 
    Runs data processing scripts to turn raw data downloaded directly from devices into
        cleaned data ready to be analyzed (saved in processed).
    """
    logger = setup_logging()

    # Start date
    try:
        start_date = sys.argv[1]
    except IndexError:
        logger.warning("No start date specified")
        start_date = "19000101" # some random early date

    # End Date
    try:
       end_date = sys.argv[2]
    except IndexError:
        logger.warning("No end date specified")
        end_date = "22000101" # some random end date - if the project is still alive at this point, please erect a statue in my honor

    # Filename
    try:
        ip_filename = sys.argv[3]
    except IndexError:
        logger.warning("No file specified - looking for airthings_ips.txt")
        ip_filename="airthings_ips"

    processor = Process(start_date=start_date,end_date=end_date,ip_filename=ip_filename)
    processor.run()