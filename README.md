[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://www.gnu.org/licenses/mit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![GitHub top language](https://img.shields.io/github/languages/top/intelligent-environments-lab/bleed-orange-measure-iaq)

# Bleed Orange Measure IAQ

Data and analysis relateted to the Bleed Orange, Measure IAQ campaign at the University of Texas at Austin. This project is funded by the Green Fund Iniative conducted by UT's Office of Sustainability. For more information regarding the project, please visit the [Wiki](https://github.com/intelligent-environments-lab/bleed-orange-measure-iaq/wiki) page. 

# Using this Repository
This project's repository contains important software regarding connecting to, downloading, and analyzing data from the project's two commercial indoor air quality (IAQ) sensors: AirThings Wave Plus and Purple Air Indoor PM monitors. To use these software effectively, we recommend cloning the repository to your own machine since many of the scripts rely on the file strcuture that we have created. 

## Downloading Data
We have developed a few scripts to aid in downloading data from our devices (or yours for that matter) to your local machine. 

### AirThings
Initially, we relied on the GUI provided by having an AirThings Business account, but we learned that we could use Raspberry Pis (RPis) to connect to the AirThings devices via bluetooth (BT) and query, pull, and store data. We could then leverage our knowledge of using RPis for other projects (see [BEVO Beacon](https://github.com/intelligent-environments-lab/bevo_iaq)) and UT's ubiquitious IoT network to access those data from anywhere. For more detail, visit our other Github project on the [AirThings Beacon](https://github.com/intelligent-environments-lab/airthings-waveplus-beacon). 

The [source code](https://github.com/intelligent-environments-lab/bleed-orange-measure-iaq/blob/master/src/data/make_airthings_dataset.py) for downloading data from AirThings is simple to use assuming you have set up/have access to the IP addresses of the AirThings Beacons. 

1. Start by editing the [airthings_ips.txt](https://github.com/intelligent-environments-lab/bleed-orange-measure-iaq/blob/master/src/data/airthings_ips.txt) file where each line refers to an AirThings Beacon IP address. We connect each of our AirThings Beacons to our [Tailscale](https://tailscale.com) account which is a _free_ VPN service and provides static IP addresses for each of our devices. 

2. From the command line, run the script with:

```bash
python3 make_airthings_dataset.py **options
```

We have three options that can be specified:
* `start_date`: a string of numbers in the format of `%m%d%Y` specifying the first day you want to consider for data download (inclusive)
* `end_date`: a string of numbers in the format of `%m%d%Y` specifying the last day you want to consider for data download (inclusive)
* `filename`: text file to look for containing IP addresses if the default `airthings_ips` is not desired. This option is useful if you want to partition your devies into different groups based on floor, building, etc. 

3. Check for your data in `/data/processed/`!

Data will be downloaded from each device, temporarily stored in the `/data/interim/` directory, processed, combined, and saved. 

### Purple Air
More info to come, but check out our _very_ similar project that measures _outdoor_ particulate matter pollution on campus: [Bleed Orange, Measure Purple](https://github.com/intelligent-environments-lab/bleed-orange-measure-purple). 

1. Start by determining your Thingspeak APi keys by using this link and updating the latitude and longitude fields so that you create a rectangle around your devices:
```
https://www.purpleair.com/json?exclude=true&nwlat=<northwest_corner_latitude>&selat=<southeast_corner_latitude>&nwlng=<northwest_corner_longitude>&selng=<southeat_corner_longitude>
```

The resulting URL will show you a json-like result for all devices in that rectangle. Find your devices and update the [thingspeak_keys.json] with your devices information.

---
<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
