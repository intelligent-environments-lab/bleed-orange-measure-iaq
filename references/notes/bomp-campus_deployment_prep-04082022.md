# Preparation for Campus Deployment
Getting things in order to rollout our devices

## Updates

### Dashboard Help
Looks like UT facilities is _not_ interested in hosting our data. I spoke with Kingsley and he thinks that we can create a relatively simple dashboard. The idea is:
1. Upload data to Github each day
2. Through Github Actions (will have to look into this), update our visualizations and display them. 

We could even most the dashboard on the Wiki if we wanted to since the static images would just be overwritten. 

### AirThings + RPi Beacons
We still seem to be encountering issues:
1. 7/10 of our devices disconnected from WiFi on 04/06 at various times in the afternoon around 4:00 pm
2. Device 1961 went offline earlier on 04/01
3. Device 0905 does not let me connect to it - was SSH enabled?
4. Device 2601 is still connected, but stopped providing data on 04/06 around 5:15 am. The device encountered an error that I _thought_ I had fixed. I updated the code and restarted the device, but data are still not coming in. 

### Data Download Updates
Did anyone try to use the `make_airthings_dataset.py` script? 

### Sensor Box Setup
* Progress on metal cage setup?
* Progress on laser cutting?
* Number of fully completed packages?

### Deployment
I want us to deploy again to ECJ and EER to provide another test of our fully-outfitted sensor packages. Once we have at least two packages ready and the software is working, I will contact the building owners and we can setup as early as next week. We only need to run this test for about a week to make sure things are working. The sooner the better since the semester is coming to a close. 

## Next Steps

* Debug beacons (Hagen)
* Finalize sensor packages (Angelina/Kyle)
* Update Wiki page (Hagen)
* Begin deployment (Hagen/Angelina/Kyle)
* Begin developing data upload pipelin (Hagen)
