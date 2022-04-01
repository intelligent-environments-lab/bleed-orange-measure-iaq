import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm
import seaborn as sns

class AirThingsSummary:

    def __init__(self) -> None:
        pass

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


