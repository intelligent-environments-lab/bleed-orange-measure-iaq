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

import sys
import logging
import pathlib
import os
import argparse

import pandas as pd
import numpy as np

from datetime import datetime

logger = logging.getLogger(__name__)
dir_path = pathlib.Path(__file__).resolve().parent
logging.basicConfig(filename=f'{dir_path}/data_airthings.log', filemode='w', level=logging.INFO,
                    format='%(asctime)s: %(name)s (%(lineno)d) - %(levelname)s - %(message)s',datefmt='%m/%d/%y %H:%M:%S')

class Process:
    """
    Processes data from a list of AirThings Devices
    """

    def __init__(self,start_date,end_date,ip_filename=None) -> None:
        """
        Parameters
        ----------
        start_date : str
            first day to consider for data processing in form "%Y%m%d" (inclusive)
        end_date : str
            last day to consider for data processing in form "%Y%m%d" (inclusive)
        ip_filename : str, None
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
        self.path_to_meta = f"{pathlib.Path(__file__).resolve().parent.parent.parent}/references/meta_data" 
        
        # IP Addresses
        if ip_filename is None:
            try:
                meta = pd.read_csv(f"{self.path_to_meta}/airthings_meta.csv")
                self.ips = list(meta["ip_address"].values)
            except FileNotFoundError:
                logger.exception("No meta data available, creating empty list:")
                self.ips = []
        else: # assuming an str
            try:
                ip_file =  open(f"{self.path_to_meta}/{ip_filename}.txt")
                self.ips = ip_file.read().split("\n")
            except FileNotFoundError:
                logger.exception(f"no {ip_filename}.txt found - please create this file in the same directory")
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
        logger.info(f"downloading data from Device {ip_address}")
        os.system(f'scp -r -o ConnectTimeout=3 pi@{ip_address}:{path_to_raw} {self.path_to_data}/interim/')

    def perform_quality_checks(self,data,params=["rh","temperature","co2","voc"]):
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
                data_device.loc[:,'z'] = abs(data_device.loc[:,param] - data_device.loc[:,param].mean()) / data_device.loc[:,param].std(ddof=0)
                data_device.loc[data_device['z'] > 2.5, param] = np.nan

            data_device.drop(['z'],axis=1,inplace=True)
            
            data_qc = pd.concat([data_qc,data_device],axis=0)

        return data_qc

    def make_dataset(self):
        """
        Combines data from AirThings Beacons

        Creates
        -------
        processed : DataFrame
            data from each AirThings Beacon
        """
        logger.info("generating dataset")
        if len(self.ips) > 0:
            for ip in self.ips:
                self.download(ip)

            combined = pd.DataFrame()
            logger.info("Importing files:")
            for file in os.listdir(f"{self.path_to_data}/interim/DATA/"):
                if file[-1] == "v": # csV files
                    file_date = datetime.strptime(f"{file.split('-')[1]}{file.split('-')[2]}{file.split('-')[3].split('.')[0]}","%Y%m%d")
                    if file_date >= self.start_date and file_date <= self.end_date:
                        device = file.split("-")[0]
                        logger.info(f"\t{file}")
                        temp = pd.read_csv(f"{self.path_to_data}/interim/DATA/{file}",parse_dates=["timestamp"],infer_datetime_format=True)
                        temp["device"] = device

                        combined = pd.concat([combined,temp],axis=0)

            # processing
            combined.sort_values(["device","timestamp"],inplace=True)
            combined.set_index("timestamp",inplace=True)
            # saving processed data as class object
            self.processed = self.perform_quality_checks(combined)
            # deleting interim data
            os.system(f"rm -r {self.path_to_data}/interim/DATA/")
        else:
            logging.error("No IP addresses to read from")

    def save(self):
        """
        Saves the class dataset to path
        """
        logger.info("saving dataset")
        try:
            data_start_date = datetime.strftime(min(self.processed.index).date(),"%Y%m%d")
            data_end_date = datetime.strftime(max(self.processed.index).date(),"%Y%m%d")
            self.processed.to_csv(f"{self.path_to_data}/processed/airthings-data-{data_start_date}-{data_end_date}.csv")
        except AttributeError:
            logger.exception("need to make the dataset first")

    def run(self):
        """
        Runner for the Process class
        """
        self.make_dataset()
        self.save()

if __name__ == '__main__':
    """ 
    Runs data processing scripts to turn raw data downloaded directly from devices into
        cleaned data ready to be analyzed (saved in processed).
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', help="start date in format %Y%m%d", default="19000101", type=str)
    parser.add_argument('-e', help="end date in format %Y%m%d", default="22000101", type=str)
    parser.add_argument('-f', help="filename to find IP addresses for devices", default="airthings_ips", type=str)
    args = parser.parse_args()

    processor = Process(start_date=args.s,end_date=args.e,ip_filename=args.f)
    processor.run()