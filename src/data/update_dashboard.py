# -*- coding: utf-8 -*-
# ----------------------
# Make AirThings Dataset
#
# Import data from
# AirThings and
# PurpleAir, creates
# figures, and pushes
# them to Github
# 
# Author: Hagen Fritz
# Date: 05/13/2022
# ----------------------

import sys
import logging
import pathlib
import os
import argparse

import pandas as pd
import numpy as np

from datetime import datetime, timedelta
import time
import warnings
warnings.filterwarnings("ignore")

sys.path.append(pathlib.Path(__file__).resolve().parent.parent.parent.as_posix())
from src.data import make_dataset
from src.visualization import visualize

logger = logging.getLogger("make_dashboard")
dir_path = pathlib.Path(__file__).resolve().parent
logging.basicConfig(filename=f'{dir_path}/dashboard_gen.log', filemode='w', level=logging.INFO,
                    format='%(asctime)s: %(name)s (%(lineno)d) - %(levelname)s - %(message)s',datefmt='%m/%d/%y %H:%M:%S')

class Data:

    def __init__(self,start_date,end_date,resample_rate) -> None:
        """
        Gets data from the AirThings and PurpleAir Devices

        Parameters
        ----------
        start_date : str
            first date to consider in the format of "yyyymmdd"
        end_date : str
            final date to soncider in the format of "yyyymmdd"
        resample_rate : int
            rate to resample the data to in minutes

        Creates
        -------
        start_date : str
            first date to consider in the format of "yyyymmdd"
        end_date : str
            final date to soncider in the format of "yyyymmdd"
        resample_rate : int
            rate to resample the data to in minutes
        """
        # import paths
        self.path_to_this_dir = f"{pathlib.Path(__file__).resolve().parent}"
        self.path_to_data = f"{pathlib.Path(__file__).resolve().parent.parent.parent}/data"
        self.meta_data = f"{pathlib.Path(__file__).resolve().parent.parent.parent}/references/meta_data"

        # dates
        self.start_date = start_date#datetime.strptime(start_date,"%Y%m%d")
        self.end_date = end_date#datetime.strptime(end_date,"%Y%m%d")

        self.resample_rate = resample_rate

    def get_airthings(self):
        """
        Gets the airthings data
        """
        at_processor = make_dataset.AirThings(start_date=self.start_date,end_date=self.end_date)
        at_processor.make_dataset()
        at_processor.perform_quality_checks(at_processor.processed)
        # reampling
        data_resampled = pd.DataFrame()
        for device in at_processor.processed["device"].unique():
            data_device = at_processor.processed[at_processor.processed["device"] == device]
            data_device_resampled = data_device.resample(f"{self.resample_rate}T").mean()
            
            data_device_resampled["device"] = device
            data_resampled = pd.concat([data_resampled,data_device_resampled],axis=0)

        # adding in meta data
        meta_at = pd.read_csv(f"{self.meta_data}/airthings_meta.csv")
        # converting both id columns to numerical
        meta_at["mac_address"] = pd.to_numeric(meta_at["mac_address"])
        data_resampled["device"] = pd.to_numeric(data_resampled["device"])
        self.data_at = data_resampled.merge(right=meta_at,left_on=["device"],right_on=["mac_address"],how="left")
        self.data_at["timestamp"] = data_resampled.index
        self.data_at.set_index("timestamp",inplace=True)
        self.data_at.to_csv(f"{self.path_to_data}/interim/airthings-dashboard.csv")

    def get_purpleair(self):
        """
        Gets the purpleair data
        """
        pa_processor = make_dataset.PurpleAir(start_date=self.start_date,end_date=self.end_date)
        pa_processor.make_dataset()
        pa_processor.perform_quality_checks(pa_processor.processed)
        # reampling
        data_resampled = pd.DataFrame()
        if "device" in pa_processor.processed.columns:
            for device in pa_processor.processed["device"].unique():
                data_device = pa_processor.processed[pa_processor.processed["device"] == device]
                data_device_resampled = data_device.resample(f"{self.resample_rate}T").mean()
                
                data_device_resampled["device"] = device
                data_resampled = pd.concat([data_resampled,data_device_resampled],axis=0)

            # adding in meta data
            meta_pa = pd.read_csv(f"{self.meta_data}/purpleair_meta.csv")
            # converting both id columns to numerical
            self.data_pa = data_resampled.merge(right=meta_pa,left_on=["device"],right_on=["id"],how="left")
            self.data_pa["timestamp"] = data_resampled.index
            self.data_pa.set_index("timestamp",inplace=True)
            self.data_pa.to_csv(f"{self.path_to_data}/interim/purpleair-dashboard.csv")
        else:
            logger.warning(f"No 'device' in processed dataset - likely the DataFrame is empty: {len(pa_processor.processed)}")
            # not creating an data_pa object because we catch the AttributeError later

    def merge_data(self):
        """
        Merges data from both devices
        """
        try:
            # timezone aware indices and resetting for merge
            logger.info("Localizing Datasets")
            self.data_at.index = self.data_at.index.tz_localize("US/Central")
            self.data_at.reset_index(inplace=True)
            self.data_pa = self.data_pa.copy().tz_convert('US/Central')
            self.data_pa.reset_index(inplace=True)
            logger.info("Merging AirThings and PurpleAir Datasets")
            self.data = self.data_at.merge(right=self.data_pa,on=["kit_no","timestamp"],how="outer",suffixes=["-airthings","-purpleair"])
            self.data.set_index("timestamp",inplace=True)
        except AttributeError:
            logger.exception("Missing processed data:")
            # saving the aggregate data as either AirThings or Purple Air - whichever is available
            try:
                logger.warning("Aggregate data from AirThings ONLY")
                self.data = self.data_at.set_index("timestamp")
            except AttributeError: # no AirThings data
                logger.warning("Aggregate data from PurpleAir ONLY")
                self.data = self.data_pa.set_index("timestamp")

        self.data.to_csv(f"{self.path_to_data}/interim/data-dashboard.csv")

    def run(self):
        """
        Runs the data ingress process
        """
        self.get_airthings()
        self.get_purpleair()
        self.merge_data()

class Figures:

    def __init__(self) -> None:
        """
        Creates the figures from the provided data
        """
        # import paths
        self.path_to_this_dir = f"{pathlib.Path(__file__).resolve().parent}"
        self.path_to_data = f"{pathlib.Path(__file__).resolve().parent.parent.parent}/data"

        self.data = pd.read_csv(f"{self.path_to_data}/interim/data-dashboard.csv",
            index_col=0,parse_dates=True,infer_datetime_format=True)
        
    def generate_timeseries(self,params=["co2-ppm","voc-ppb","pm2p5_mass-microgram_per_m3","temperature-c","rh-percent-airthings"]):
        """
        Generates the timeseries figures

        Parameters
        ----------
        params : list of str
            parameters to generate timeseries for
        """
        ts_gen = visualize.Dashboard()
        logger.info("Generating aggregate timeseries for:")
        for param in params:
            logger.info(f"\t{param}")
            if param in self.data.columns:
                ts_gen.timeseries_aggregate(self.data,param=param,show=False,save=True,subdir="/dashboard")
            else:
                logger.info(f"{param} not in DataFrame")

    def generate_heatmaps(self,params=["co2-ppm","voc-ppb","pm2p5_mass-microgram_per_m3","temperature-c","rh-percent-airthings"]):
        """
        Generates the timeseries figures

        Parameters
        ----------
        params : list of str
            parameters to generate timeseries for
        """
        ts_gen = visualize.Dashboard()
        logger.info("Generating heatmap for:")
        for param in params:
            logger.info(f"\t{param}")
            if param in self.data.columns:
                for device in self.data["kit_no"].unique():
                    logger.info(f"\t\t{device}")
                    ts_gen.heatmap_individual(self.data,id_col="kit_no",device=device,param=param,show=False,save=True,subdir="/dashboard")
            else:
                logger.info(f"{param} not in DataFrame")


def main(period=60,resample_rate=15,update_period=15):
    """
    Ingresses the data, generates the figures, and pushes them to Github

    Parameters
    ----------
    period : int, default 60
        number of days to plot
    resample_rate : int, default 15
        frequency to resample data to in minutes
    """
    starttime = time.time()  # Used for preventing time drift
    while True:
        start_time = time.time()  # Used for evaluating scan cycle time performance
        # Ingressing
        # ----------
        ## Getting the import dates
        end_date = datetime.now()
        end_date_str = datetime.strftime(end_date,"%Y%m%d")
        start_date = end_date - timedelta(days=period)
        start_date_str = datetime.strftime(start_date,"%Y%m%d")
        ## generating and saving datasets
        ingress = Data(start_date=start_date_str,end_date=end_date_str,resample_rate=resample_rate)
        ingress.run()
        # Figure Gen
        # ----------
        vis = Figures()
        ## timeseries figures
        vis.generate_timeseries()
        vis.generate_heatmaps()
        # Pushing to GH
        # -------------
        path_to_push = f"{pathlib.Path(__file__).resolve().parent.parent.parent}/reports/figures/dashboard/"
        current_time = datetime.strftime(datetime.now(),"%m/%d %H:%M")
        try:
            os.system(f'git add {path_to_push}* && git commit -m "figure update {current_time}" && git push')
        except Exception as e:
            logger.exception("Error:")

        # Report cycle time for performance evaluation by user
        elapsed_time = time.time() - start_time
        logger.info(f"Cycle Time: {elapsed_time} \n\n")

        # Make sure that interval between scans is exact
        time.sleep(update_period*60.0 - ((time.time() - starttime) % (update_period*60.0)))

if __name__ == '__main__':
    """ 
    Generates the figures used in the dashboard
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', help="number of days of data to show", default=60, type=int)
    parser.add_argument('-r', help="resample rate in minutes", default=15, type=int)
    parser.add_argument('-q', help="data query rate in minutes", default=5, type=int)
    args = parser.parse_args()

    main(period=args.d,resample_rate=args.r,update_period=args.q)
