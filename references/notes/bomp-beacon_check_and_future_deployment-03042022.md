# AirThings Beacon Check
We have the AirThings Beacons in place on the third floor so we should try connecting to them to see what data are available. Below are the list of operating beacons:

* Device 1730 - 100.109.6.44 - ECJ 3.110 (Connected to Hub)
* Device 1961 - 100.121.113.29 - ECJ 3.406 (No Connection)
* Device 2307 - 100.74.234.86 - ECJ 3.116 (Connected to Hub)
* Device 2521 - 100.111.31.71 - ECJ 3.106 (Connected to Hub)

### Viewing Data
Each of us should connect to one of the Beacons listed below and view the data.
1. Log into the device: ```ssh pi@<ip_address>```
2. Move to the correct directory: ```cd DATA```
3. Look at what is available: ```ls```
4. From here, we should see at least 4 different files corresponding to T 03/01, W 03/02, Th 03/03, and F 03/04.
5. If the files exist, let's examine the Thursday file: ```sudo nano <filename>```

#### Outcome
From the three devices connected to the fifth floor hub, two are logging data via the RPi despite issues raised on the original Github repo that states connection to a hub intereferes with data collection. However, the third one is having trouble connecting to the RPi. The latest device, 2428, is _not_ connected to a hub but is also not connecting to the RPi. 

### Debugging Hub Connection
Interestingly, three of the devices recently synced with a hub even though we removed the hub on the third floor. Something I am curious about is whether these devices were originally connected to the fifth floor hub or reset their connection once we removed the hub on the third floor. We can try looking at the data for these three devices:
1. Look at the time series data for CO2 from Devices 1730, 2307, and 2521
2. Identify if there are any missing data around the time we removed the hub Tuesday 03/01 between 3:30 - 5:00 pm. 

#### Outcome
There were no breaks in the data meaning the AirThings immediately (within 5 minutes) connected to the fifth floor hub once the hub on the third floor was removed. 

# Brainstorming Building and Room Locations
Assuming all works well with the AirThings Beacons, we need to figure out which locations work best for our devices. The original proposal included these locations: 

![bomp_proposed_locations](https://user-images.githubusercontent.com/33231914/156771103-eb8ed4c8-4e7b-4b14-8ba8-5813a2de5b2e.png)

Updates to locations:
* Large (new): EER 1.1518
* Common (old): PCL 
* Common (new): WEL
