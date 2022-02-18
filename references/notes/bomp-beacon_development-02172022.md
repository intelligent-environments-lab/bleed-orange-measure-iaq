# AirThings Beacon Development
Now that we have our network of 9 devices set up in ECJ, we can focus on configuring the hardware and software for the AirThings Beacons.

## Hardware
I documented the process to configure the RPi in the Wiki of this repository: https://github.com/intelligent-environments-lab/bleed-orange-measure-iaq/wiki/AirThings-Beacon. Please use this document to set up the remaining 9 RPi devices corresponding the other 9 AirThings devices. The biggest issue is going to be finding SD cards which we should be able to borrow from other, out-dated projects.

## Software
There are two primary software components I wanted to chat about: Tailscale and the waveplus-reader.py.

### Connecting with Tailscale
1. To start, you will need to download and install [Tailscale](https://tailscale.com/download) to your computer. I am not sure how the interface looks on a PC, so we will want to look together. 
2. Open up the command line prompt or whatever solution that Angelina was able to find. 
3. On Tailscale, find the IP address associated with the device you want to connect with.
4. Back on the command line, type:

```bash
ssh pi@xxx.xx.xxx
```

replacing the "x"s with the corresponding numbers (it might also not be in the same format). 
5. You should be connected and see that the username changes to something like `pi@raspberrypi`

We will use a good part of the meeting to debug any issues with y'all connecting. 

### Reading and Saving Data 
We will borrow a lot of the code from the BEVO IAQ repository, specifically the [`main.py`](https://github.com/intelligent-environments-lab/bevo_iaq/blob/master/bevobeacon-iaq/main.py) script but simplify it down to our needs.  We will want to combine the `waveplus-reader.py` code with chunks from this [snippet](https://github.com/intelligent-environments-lab/bevo_iaq/blob/a70fa10d603bfab9fdb492cefe0a8aa6a215a29f/bevobeacon-iaq/main.py#L54-L139) of code from the BEVO IAQ into one script. Here are my thoughts which we will go over in more detail during the meeting:
* Put the [`try-except`](https://github.com/intelligent-environments-lab/airthings-waveplus-beacon/blob/6171066e33d1d08f997748fca2d425dbe1e654a8/read_waveplus.py#L178-L207) code in the `read_waveplus.py` script within an infinite loop
* Rather than [save the data as a json file](https://github.com/intelligent-environments-lab/airthings-waveplus-beacon/blob/6171066e33d1d08f997748fca2d425dbe1e654a8/read_waveplus.py#L204-L205), copy over code from the `main.py` script in the BEVO IAQ repository to save the data in a Pandas DataFrame which we can then [save/append to a daily csv](https://github.com/intelligent-environments-lab/bevo_iaq/blob/a70fa10d603bfab9fdb492cefe0a8aa6a215a29f/bevobeacon-iaq/main.py#L111-L121)

That should be it! We will also need to figure out a way to handle the serial number. I think the simplest idea is to just hard-code the number in for the correct RPi. The BEVO IAQ also has a way to update this parameter which we can borrow from as well but is best left for another day to discuss. 

## Next Steps
1. Continue to Monitor our 9 devices:
  * Angelina: AirThings Devices
  * Kyle: PurpleAirs
2. Setup the AirThings Beacon RPis following the documentation I provided
  * Let me know if there are any issues/incomplete documentation
3.  Decide if y'all would prefer to develop the Python script on your own time or schedule another meeting so we can tackle it together. 
