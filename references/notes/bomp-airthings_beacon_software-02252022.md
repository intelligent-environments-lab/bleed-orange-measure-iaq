# AirThings Beacon Software
With a large majority of the hardware ready, we can try tackling the software aspects of the AirThings Beacon. 

## AirThings Update - Angelina
* Are devices still up and running?
* Anything interesting you have noticed from just glancing at the dasboard?

## PurpleAir Update - Kyle
* Are devices still up and running?
* Anything interesting you have noticed?

## Hardware Update
* Where are we on RPi setup?
* Any issues to report out?

## Software Development

### Reading and Saving Data 
We will borrow a lot of the code from the BEVO IAQ repository, specifically the [`main.py`](https://github.com/intelligent-environments-lab/bevo_iaq/blob/master/bevobeacon-iaq/main.py) script but simplify it down to our needs.  We will want to combine the `waveplus-reader.py` code with chunks from this [snippet](https://github.com/intelligent-environments-lab/bevo_iaq/blob/a70fa10d603bfab9fdb492cefe0a8aa6a215a29f/bevobeacon-iaq/main.py#L54-L139) of code from the BEVO IAQ into one script. Here are my thoughts which we will go over in more detail during the meeting:
* Put the [`try-except`](https://github.com/intelligent-environments-lab/airthings-waveplus-beacon/blob/6171066e33d1d08f997748fca2d425dbe1e654a8/read_waveplus.py#L178-L207) code in the `read_waveplus.py` script within an infinite loop
* Rather than [save the data as a json file](https://github.com/intelligent-environments-lab/airthings-waveplus-beacon/blob/6171066e33d1d08f997748fca2d425dbe1e654a8/read_waveplus.py#L204-L205), copy over code from the `main.py` script in the BEVO IAQ repository to save the data in a Pandas DataFrame which we can then [save/append to a daily csv](https://github.com/intelligent-environments-lab/bevo_iaq/blob/a70fa10d603bfab9fdb492cefe0a8aa6a215a29f/bevobeacon-iaq/main.py#L111-L121)

That should be it! We will also need to figure out a way to handle the serial number. I think the simplest idea is to just hard-code the number in for the correct RPi. The BEVO IAQ also has a way to update this parameter which we can borrow from as well but is best left for another day to discuss. 

## Next Steps
1. Continue to Monitor our 9 devices:
  * Angelina: AirThings
  * Kyle: PurpleAirs
2. Debug/finalize code for Beacons
  * See if this needs to be another group effort
3. Update software on each RPi from Github
4. Setup the AirThings Beacons next to locations on the third floor for a beta test.


