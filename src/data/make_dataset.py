# -*- coding: utf-8 -*-
# ----------------------
# Make Dataset
#
# Imports and processes
# raw data from the 
# PurpleAir and AirThings
# sensors
# 
# Author: Hagen Fritz
# Date: 05/16/2022
# ----------------------

import sys
import logging
import pathlib
import os
import argparse

import pandas as pd
import numpy as np

from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

sys.path.append(pathlib.Path(__file__).resolve().parent.parent.parent.as_posix())
from src.data import purpleair_data_retriever as pdr

logger = logging.getLogger("make_dataset")
dir_path = pathlib.Path(__file__).resolve().parent
logging.basicConfig(filename=f'{dir_path}/dataset.log', filemode='w', level=logging.INFO,
                    format='%(asctime)s: %(name)s (%(lineno)d) - %(levelname)s - %(message)s',datefmt='%m/%d/%y %H:%M:%S')

class Process:

    def __init__(self,start_date,end_date) -> None:
        """
        Processes data from a list of PurpleAir Devices

        Parameters
        ----------
        start_date : str
            first day to consider for data processing in form "%Y%m%d" (inclusive)
        end_date : str
            last day to consider for data processing in form "%Y%m%d" (inclusive)

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
        path_to_meta : str
            location of the folder holding the data
        """
        # getting datetime from str
        self.start_date = datetime.strptime(start_date,"%Y%m%d")
        self.end_date = datetime.strptime(end_date,"%Y%m%d")

        # import paths
        self.path_to_this_dir = f"{pathlib.Path(__file__).resolve().parent}"
        self.path_to_data = f"{pathlib.Path(__file__).resolve().parent.parent.parent}/data"
        self.path_to_meta = f"{pathlib.Path(__file__).resolve().parent.parent.parent}/references/meta_data"

    def perform_quality_checks(self,data,params=["co2-ppm","voc-ppb",
        "pm1_mass-microgram_per_m3","pm1_mass-microgram_per_m3","pm1_mass-microgram_per_m3",
        "temperature_f","rh_percent"]):
        """
        Some processing and quality assurance checks
        
        Parameters
        ----------
        data : DataFrame
            data in need of processing with a "device" column

        Returns
        -------
        data_qc : DataFrame
            processed data
        """
        data_qc = pd.DataFrame()
        for device in data["device"].unique():
            data_device = data[data["device"] == device]
            for param in params:
                logger.info(f"Quality check: {param}")
                try:
                    data_device.loc[:,'z'] = abs(data_device.loc[:,param] - data_device.loc[:,param].mean()) / data_device.loc[:,param].std(ddof=0)
                    data_device.loc[data_device['z'] > 2.5, param] = np.nan
                except KeyError:
                    logger.warning(f"\tNo column {param} in DataFrame")

            logger.info("Dropping z-score column")
            data_device.drop(['z'],axis=1,inplace=True)
            
            data_qc = pd.concat([data_qc,data_device],axis=0)

        return data_qc

    def save(self,modality="airthings"):
        """
        Saves the class dataset to path

        Parameters
        ----------
        modality : str, default airthings
            which modality in ["airthings","purpleair"] we are saving
        """
        logger.info(f"Saving {modality} Dataset")
        try:
            data_start_date = datetime.strftime(min(self.processed.index).date(),"%Y%m%d")
            data_end_date = datetime.strftime(max(self.processed.index).date(),"%Y%m%d")
            self.processed.to_csv(f"{self.path_to_data}/processed/{modality}-data-{data_start_date}-{data_end_date}.csv")
            logger.info(f"\tSuccessfully saved to {self.path_to_data}/processed/{modality}-data-{data_start_date}-{data_end_date}")
        except AttributeError:
            logger.exception(f"\tNeed to make the {modality} dataset first")

class AirThings(Process):

    def __init__(self, start_date, end_date) -> None:
        super().__init__(start_date, end_date)
        
        meta = pd.read_csv(f"{self.path_to_meta}/airthings_meta.csv")
        self.ips = list(meta["ip_address"].values)

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
        logger.info(f"Downloading data from Device {ip_address}")
        os.system(f'scp -r -o ConnectTimeout=3 pi@{ip_address}:{path_to_raw} {self.path_to_data}/interim/')
        for file in os.listdir(f"{self.path_to_data}/interim/DATA/"):
            logger.info(f"\t{file}")

    def make_dataset(self):
        """
        Combines data from AirThings Beacons

        Creates
        -------
        processed : DataFrame
            data from each AirThings Beacon
        """
        logger.info("Generating AirThings Dataset")
        if len(self.ips) > 0:
            for ip in self.ips:
                self.download(ip)

            combined = pd.DataFrame()
            logger.info("Importing files:")
            for file in os.listdir(f"{self.path_to_data}/interim/DATA/"):
                if file.endswith("v"): # csV files
                    file_date = datetime.strptime(f"{file.split('-')[1]}{file.split('-')[2]}{file.split('-')[3].split('.')[0]}","%Y%m%d")
                    logger.info(f"\tFile from: {file_date}")
                    if file_date >= self.start_date and file_date <= self.end_date:
                        device = file.split("-")[0]
                        logger.info(f"\t\tReading {file}")
                        temp = pd.read_csv(f"{self.path_to_data}/interim/DATA/{file}",parse_dates=["timestamp"],infer_datetime_format=True)
                        temp["device"] = device

                        combined = pd.concat([combined,temp],axis=0)

            logger.info(f"AirThings Data\n{combined.head()}")
            # saving processed as class object
            logger.info("Renaming AirThings columns")
            combined.rename(columns={"rh":"rh-percent","temperature":"temperature-c","pressure":"pressure-pa",
                "radon_acute":"radon_acute-units","radon_chronic":"radon_chronic-units","co2":"co2-ppm","voc":"voc-ppb"},
                inplace=True)
            logger.info("Sorting AirThings values by device and timestamp")
            combined.sort_values(["device","timestamp"],inplace=True)
            self.processed = combined.set_index("timestamp")
            # deleting interim data
            logger.warning("Deleting /interim/DATA/ directory")
            os.system(f"rm -r {self.path_to_data}/interim/DATA/")
        else:
            logger.warning("No IP addresses to read from")

    def run(self):
        """
        Runner for the Process class
        """
        self.make_dataset()
        self.perform_quality_checks(self.processed)
        self.save("airthings")

class PurpleAir(Process):

    def __init__(self, start_date, end_date) -> None:
        super().__init__(start_date, end_date)

    def download(self):
        """
        Downloads data from the PurpleAirs using the BOMP source code 
        """
        # getting new str from datetime
        start_str = datetime.strftime(self.start_date,"%Y-%m-%d")
        end_str = datetime.strftime(self.end_date,"%Y-%m-%d")

        # downloading data
        logger.info(f"Downloading data from PurpleAir Devices:")
        pdr.main(start=start_str, end=end_str, channel='primaryA', save_location='data/interim/purpleair')
        for file in os.listdir(f"{self.path_to_data}/interim/purpleair/"):
            logger.info(f"\t{file}")

    def make_dataset(self):
        """
        Combines raw data from the purple air devices
        """
        logger.info("Generating PurpleAir Dataset")
        combined = pd.DataFrame()
        for file in os.listdir(f"{self.path_to_data}/interim/purpleair/"):
            if file.endswith("v"):
                logger.info(f"\tReading {file}")
                temp = pd.read_csv(f"{self.path_to_data}/interim/purpleair/{file}",parse_dates=["created_at"],infer_datetime_format=True)
                temp.rename(columns={
                    "created_at":"timestamp",
                    "PM1.0_CF1_ug/m3":"pm1_mass-microgram_per_m3",
                    "PM2.5_CF1_ug/m3":"pm2p5_mass-microgram_per_m3",
                    "PM10.0_CF1_ug/m3":"pm10_mass-microgram_per_m3",
                    "Temperature_F":"temperature-f",
                    "Humidity_%":"rh-percent"},
                    inplace=True)
                temp_filtered = temp.copy()[["timestamp","pm1_mass-microgram_per_m3","pm2p5_mass-microgram_per_m3","pm10_mass-microgram_per_m3","temperature-f","rh-percent"]]
                temp_filtered["device"] = file.split(" ")[0]
                combined = pd.concat([combined,temp_filtered],axis=0)

        logger.info(f"Purple Air Data\n{combined.head()}")
        # creating class instance
        logger.info("Sorting PurpleAir values by device and timestamp")
        try:
            combined.sort_values(["device","timestamp"],inplace=True)
            self.processed = combined.set_index("timestamp")
        except KeyError:
            logger.exception(f"No data available (n={len(combined)}):")
            self.processed = pd.DataFrame() # setting as empty dataframe

    def run(self):
        """
        Runner for the Process class
        """
        self.make_dataset()
        self.perform_quality_checks(self.processed)
        self.save("purpleair")

def main(start_date="19000101",end_date="22000101"):
    """
    Imports, processes, and saves the data
    """
    at_processor = AirThings(start_date,end_date)
    at_processor.run()
    pa_processor = PurpleAir(start_date,end_date)
    pa_processor.run()

if __name__ == '__main__':
    """ 
    Runs data processing scripts to turn raw data downloaded directly from devices into
        cleaned data ready to be analyzed (saved in processed).
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', help="start date in format %Y%m%d", default="19000101", type=str)
    parser.add_argument('-e', help="end date in format %Y%m%d", default="22000101", type=str)
    args = parser.parse_args()

    main(start_date=args.s,end_date=args.e)