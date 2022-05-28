import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm
import seaborn as sns
import pathlib

class Dashboard:

    def __init__(self) -> None:
        """
        """
        self.path_to_figures = f"{pathlib.Path(__file__).resolve().parent.parent.parent}/reports/figures"
        self.path_to_top = f"{pathlib.Path(__file__).resolve().parent.parent.parent}"

    def timeseries_individual(self,data,device,param,id_col="kit_no",show=True,save=False,subdir=""):
        """
        Produces the basic timeseries plot

        Parameters
        ----------
        data : DataFrame
            data indexed by datetime
        device : str
            identifier for the specific device
        param : str
            the parameter to plot
        id_col : str, default "device"
            the column to parase out devices by
        show : boolean, default True
            whether to show the heatmap or not
        save : boolean, default False
            whether to save the heatmap or not
        subdir : str, default ""
            subdirectory in reports/figures/ to save the figure
        """
        data_device = data[data[id_col] == device]
        _, ax = plt.subplots(figsize=(12,5))
        ax.plot(data_device.index,data_device[param],lw=2)
        # x-axis
        ax.set_xlabel("")
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        ax.xaxis.set_minor_locator(mdates.DayLocator(interval=7))
        ax.xaxis.set_minor_formatter(mdates.DateFormatter('%d'))
        ax.tick_params(axis='x', labelsize=12)
        ax.tick_params(axis='x', which="major",labelsize=14,pad=10)
        # y-axis
        ax.set_ylabel(f"{get_label(param)} ({get_units(param)})",fontsize=16)
        ax.tick_params(axis='y', labelsize=14)
        if get_limits(param) is not None:
            ax.set_ylimit(get_limits)
        # remainder
        for loc in ["top","right"]:
            ax.spines[loc].set_visible(False)

        if save:
            plt.savefig(f"{self.path_to_figures}{subdir}/timeseries-{device}-{param}",bbox_inches='tight')

        if show:
            plt.show()

        plt.close()

    def timeseries_aggregate(self,data,param,id_col="kit_no",show=True,save=False,subdir=""):
        """
        Produces the basic timeseries plot

        Parameters
        ----------
        data : DataFrame
            data indexed by datetime
        device : str
            identifier for the specific device
        param : str
            the parameter to plot
        id_col : str, default "device"
            the column to parase out devices by
        show : boolean, default True
            whether to show the heatmap or not
        save : boolean, default False
            whether to save the heatmap or not
        subdir : str, default ""
            subdirectory in reports/figures/ to save the figure
        """
        # meta data - can use either file since kit_no links the two files
        meta = pd.read_csv(f"{self.path_to_top}/references/meta_data/airthings_meta.csv")
        _, ax = plt.subplots(figsize=(12,5))
        cmap = cm.get_cmap('viridis')
        cmap = cmap(np.linspace(0, 1, len(data[id_col].unique())))
        for device, color in zip(data[id_col].unique(),cmap):
            data_device = data[data[id_col] == device]
            label = meta[meta[id_col] == device]["location"].values
            ax.scatter(data_device.index,data_device[param],s=2,color=color,label=label[0])

        # x-axis
        ax.set_xlabel("")
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        ax.xaxis.set_minor_locator(mdates.DayLocator(interval=7))
        ax.xaxis.set_minor_formatter(mdates.DateFormatter('%d'))
        ax.tick_params(axis='x', labelsize=12)
        ax.tick_params(axis='x', which="major",labelsize=14,pad=10)
        # y-axis
        ax.set_ylabel(f"{get_label(param)} ({get_units(param)})",fontsize=16)
        ax.tick_params(axis='y', labelsize=14)
        if get_limits(param) is not None:
            ax.set_ylimit(get_limits)
        # remainder
        ax.legend(loc="upper center",bbox_to_anchor=(0.5,-0.15),frameon=False,ncol=5)
        for loc in ["top","right"]:
            ax.spines[loc].set_visible(False)

        if save:
            plt.savefig(f"{self.path_to_figures}{subdir}/timeseries-aggregate-{param}",bbox_inches='tight')

        if show:
            plt.show()

        plt.close()

    def heatmap_individual(self,data,device,param,id_col="kit_no",show=True,save=False,subdir=""):
        """
        Plots weekly heatmap for the given sensor

        Parameters
        ----------
        data : DataFrame
            data indexed by datetime
        device : str
            identifier for the specific device
        param : str
            the parameter to plot
        id_col : str, default "device"
            the column to parase out devices by
        show : boolean, default True
            whether to show the heatmap or not
        save : boolean, default False
            whether to save the heatmap or not
        subdir : str, default ""
            subdirectory in reports/figures/ to save the figure
        """
        # getting device data
        temp = data[data[id_col] == device]
        temp_hourly = temp.resample("60T").mean()
        if len(temp_hourly.dropna(subset=[param])) > 0:
            # adding in time information
            temp_hourly["week"] = temp_hourly.index.isocalendar().week
            temp_hourly["day"] = temp_hourly.index.day_of_week
            temp_hourly["hour"] = temp_hourly.index.hour
            temp_hourly["counter"] = temp_hourly["day"]*24+temp_hourly["hour"]
            # pivoting and plotting
            pivoted = temp_hourly.pivot(index="week",columns="counter",values=param)
            _, ax = plt.subplots(figsize=(12,4))
            sns.heatmap(pivoted,ax=ax,cmap="viridis")
            # x-axis
            ax.set_xlabel("")
            ax.set_xticks(np.arange(0,168,6),minor=True)
            ax.set_xticks(np.arange(0,180,24),minor=False)
            ax.set_xticklabels(["Mon","Tues","Wed","Thurs","Fri","Sat","Sun","Mon"],rotation=0,ha="center",fontsize=14)
            # y-axis
            ax.set_ylabel("Week",fontsize=16)
            ylabels=[]
            for wk in temp_hourly["week"].unique():
                ylabels.append("")
            ax.set_yticklabels(ylabels)    

            if save:
                plt.savefig(f"{self.path_to_figures}{subdir}/heatmap-{device}-{param}",bbox_inches='tight')

            if show:
                plt.show()
                
            plt.close()

class AirThingsSummary():

    def __init__(self) -> None:
        super().__init__()

    def plot_data_availability(self, data, params=["temperature","rh","co2","voc"]):
        """
        Plots the availability of data from each of the provided parameters

        Parameters
        ----------
        data : DataFrame
            timeseries data from specific device
        params : list of str, default ["temprature","rh","co2","voc"]
            parameters within data to check availability of
        """
        data_short = data[params]
        n_nan = []
        for i in range(len(data_short)):
            n_nan.append(len(params) - data_short.iloc[i,:].isnull().sum())

        data_short["params_available"] = n_nan
        cmap = cm.get_cmap("coolwarm_r")

        _, ax = plt.subplots(figsize=(16,len(params)))
        for n_avail in range(len(params)+1):
            data_n = data_short[data_short["params_available"] == n_avail]
            ax.scatter(data_n.index,[n_avail]*len(data_n),s=5,marker="s",color=cmap(n_avail/len(params)))

        # x-axis
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        ax.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
        ax.xaxis.set_minor_formatter(mdates.DateFormatter('%d'))
        # y-axis
        ax.set_yticks(np.arange(len(params)+1))
        ax.set_ylabel("Number of Variables",fontsize=16)
        # remainder
        ax.tick_params(labelsize=12)
        ax.tick_params(axis="x",which='major', pad=15, labelsize=14)
        for loc in ["top","right"]:
            ax.spines[loc].set_visible(False)

        plt.show()
        plt.close()

def get_label(param):
    """Gets the formated label for the param"""
    try:
        param = param.split("-")[0] # removing units
    except Exception as e:
        pass
    if param == "co2":
        return "CO$_2$"
    elif param == "co":
        return "CO"
    elif param == "pm2p5_mass" or param == "pm2p5_number" or param == "pm2p5":
        return "PM$_{2.5}$"
    elif param == "pm10_mass" or param == "pm10_number" or param == "pm10":
        return "PM$_{10}$"
    elif param in ["tvoc","voc"]:
        return "TVOC"
    elif param == "temperature_c" or param == "temperature":
        return "T"
    elif param == "rh":
        return "RH"
    else:
        return ""

def get_units(param):
    """Gets the formated label for the param"""
    try:
        param = param.split("-")[0] # removing units
    except Exception as e:
        pass
    
    if param == "co2":
        return "ppm"
    elif param == "co":
        return "ppb"
    elif param in ["pm1_mass","pm2p5_mass","pm10_mass"]:
        return "$\mu$g/m$^3$"
    elif param == "pm2p5_number":
        return "#/dL"
    elif param in ["tvoc","voc"]:
        return "ppb"
    elif param in ["temperature_c","temperature","temperature-c"]:
        return "$^\circ$C"
    elif param == "rh":
        return "%"
    else:
        return ""

def get_limits(param):
    """Gets the typical axis units for a given parameter"""
    try:
        param = param.split("-")[0] # removing units
    except Exception as e:
        pass

    if param in ["temperature_c","temperature"]:
        return [15,35]
    elif param == "rh":
        return [20,70]
    else:
        return None
