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

import pandas as pd

from datetime import datetime

class Process:
    """
    Processes data from a list of AirThings Devices
    """

    def __init__(self,start_date,end_date,ip_filename="airthings_ips") -> None:
        """
        Parameters
        ----------
        ip_addresses : list of str
            List of Tailscale IP addresses
        """
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

        """
        self.logger.info(f"downloading data from Device {ip_address}")
        os.system(f'scp -r -o ConnectTimeout=3 pi@{ip_address}:{path_to_raw} {self.path_to_data}/interim/')

    def make_dataset(self):
        """
        Combines data from AirThings Beacons
        """
        self.logger.info("generating dataset")
        if len(self.ips) > 0:
            for ip in self.ips:
                self.download(ip)

            combined = pd.DataFrame()
            for file in os.listdir(f"{self.path_to_data}/interim/DATA/"):
                if file[-1] == "v": # csV files
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

        Parameters
        ----------
        """
        self.logger.info("saving dataset")
        try:
            self.processed.to_csv(f"{self.path_to_data}/processed/airthings-data.csv")
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
    Sets up two loggers: a console and file logger 
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
        start_date = datetime(1900,1,1) # some random early date

    # End Date
    try:
       end_date = sys.argv[2]
    except IndexError:
        logger.warning("No end date specified")
        end_date = datetime(2200,1,1) # some random end date - if the project is still alive at this point, please erect a statue in my honor

    # Filename
    try:
        ip_filename = sys.argv[3]
    except IndexError:
        logger.warning("No file specified - looking for airthings_ips.txt")
        ip_filename="airthings_ips"

    processor = Process(start_date=start_date,end_date=end_date,ip_filename=ip_filename)
    processor.run()