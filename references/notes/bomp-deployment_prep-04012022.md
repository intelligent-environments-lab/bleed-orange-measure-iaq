# Preparation for Campus Deployment

## Updates from Angelina/Kyle

### Sensor Package
* We have 10 packages setup and ready for the wood sign
* Progress on wood sign
  * Is everyone trained? 
  * Need to secure funds for plywood purchase
  * Design has been finalized but we will need to see if the QR code actually works (resolution looked a bit iffy)

## Updates from Hagen

### AirThings Download Script: [source](https://github.com/intelligent-environments-lab/bleed-orange-measure-iaq/blob/master/src/data/make_airthings_dataset.py)
I created a script that we can use that sequentially connects to each available AirThings beacon, downloads available data, combines data into one DataFrame, and saves as a csv file. I included instructions on this repos [readme](https://github.com/intelligent-environments-lab/bleed-orange-measure-iaq/blob/master/README.md).

### Debugging Beacon+AirThings Connection
See [here](https://github.com/intelligent-environments-lab/bleed-orange-measure-iaq/blob/master/notebooks/1.0.0-hef-ecj_beta-data_summary_and_exploration.ipynb) (although the format is really bad).
* Primary errors seem to be because of:
  1. Tailscale: There were a lot of errors that seemed to stop a lot of other processes
  2. `BTLEDisconnectError`: Not exactly sure what this error entails, but it popped up on 3 of the RPi. After the error, the Beacon stopped connecting to the AirThings. 
* My solutions:
  * Update and upgrade so that the RPi OS and Tailscale are the latest versions
  * Include an error exception for `BTLEDisconnect` so that it is caught and hopefully circumvented.

### IEL Beta Test
All Beacons are powered on in the IELab so we can monitor the connection between Beacons and AirThings more closely. Devices tended to stay connected for the first few days in the field so we will let this test run until we are ready to deploy across campus (assuming there are no glaring issues). 
* An initial look at the performance is shown [here](https://github.com/intelligent-environments-lab/bleed-orange-measure-iaq/blob/master/notebooks/1.1.0-hef-iel_beta-data_summary_and_exploration.ipynb) (again, the formatting is off).
* Looks like we have one Beacon which is offline despite being connected to an outlet. 

## Tasks for this Week
* Design, cut, and include wood sign on all 10 sensor packages (Angelina/Kyle)
* Finalize the sensor packages (Angelina/Kyle)
* SSH into _all_ the RPi Beacons, change into the airthings-waveplus-beacon folder, and pull in updates (see next step too about which Beacons to update/upgrade so you don't have to SSH into a device twice):
```bash
cd airthings-waveplus-beacon
git pull
```
* SSH into the following RPi Beacons to update (`sudo apt-get update`) and upgrade (`sudo apt-get upgrade -y`) them:
  * 2002: 100.76.103.114
  * 2154: 100.89.151.128
  * 2168: 100.64.140.78
* Create _another_ RPi Beacon for Device 0905 (Angelina/Kyle)
* Continue to monitor the Beacon+AirThings beta test in the IELab to see if devices become disconnected (Hagen)
* Try downloading AirThings data using the `make_airthings_dataset` script after cloning the repo: [source](https://github.com/intelligent-environments-lab/bleed-orange-measure-iaq/blob/master/src/data/make_airthings_dataset.py) (Angelina _and_ Kyle)
