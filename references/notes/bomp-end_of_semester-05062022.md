# Bleed Orange, Measure Purple Wrapping Up
There are a few tasks that we have started that we should aim to wrap up in the coming week:
* pariticipant report for beta testers
* storefront setup
* dashboard lite

## Pariticpant Reports
What is our current status with these reports? Here are the following components that we need:
* Weekly plots of:
  * [ ] PM2.5
  * [ ] CO2
  * [ ] TVOC
  * [ ] T
  * [ ] RH
* Summary statistics (min, mean/median, max) for the same parameters:
  * [ ] PM2.5
  * [ ] CO2
  * [ ] TVOC
  * [ ] T
  * [ ] RH

This should be plenty to provide. If there are any more nuanced analyses that the participants are interested in, I can provide those. As a final step, please make sure to upload the following:
* [ ] Raw or processed data [here](https://drive.google.com/drive/u/8/folders/1iAiC4hhnOPGEfKMHxhxPWt-GySQ3Aq0K)
* [ ] List of summary statistics in a text or related file [here](https://drive.google.com/drive/u/8/folders/1oiNoY5IT1z2-BR6m1OY11KTSDXgWRYMM)
* [ ] Figures [here](https://drive.google.com/drive/u/8/folders/1v1Pw-2a9R2mVqp5HKx2CYmXfwFcQ887I)

## Storefront Setup
How much did we manage to get to this week regarding the storefront? Here are the tasks we need to finish:
* Check-out form
  * [ ] Google form which includes _required_ questions regarding the persons:
    * EID
    * email
    * Length of purposed experiment (include some descriptive text mentioning that we restrict the length to 2 weeks)
    * IAQ parameters they are interested in (this should be a multi-select list which includes _only_ the parameters we can measure with our devices)
    * Number of devices they would like (should include some descriptive text that mentions we _typically_ only rent out a max of 2 devices at a time)
  * [ ] QR code that links to the form
  * Include on:
    * [ ] Zoltan's website
    * [ ] GitHub page
    * [ ] IELab physical location
* Device setup
  * [ ] Need to setup all the available indoor PAs (that work) on the IoT network
  * [ ] Need to purchase an additional 2 AirThings which we will connect to one hub
  * [ ] Provide 5 _working_ BEVO Beacons to the cause
* [ ] Calendar/Schedule using the iel.bomp email account which will be linked on the GitHub page
* [ ] Sign/monitor setup in the lab so passersby can scan and check out devices
* Wiki Update
  * [ ] Instructions on how to _properly_ use each of the devices
  * [ ] Detailed information regarding the topics above ^
  * [ ] Calendar 

## Dashboard
The dreaded dashboard. I think for the time-being we can create a lite version that is simply hosted on GitHub. We could have a master device that connects to each AirThings RPi and PurpleAir, pulls the data, pushes it to Github triggering a script to generate the figures which are displayed on the Wiki. Therefore we need to:
* [ ] Create a master device
* Create a script which is run on a timer to pull data from:
  * [ ] AirThings
  * [ ] Purple Air
* [ ] Schedule a push to Github from the master device
* [ ] Create the script that generates figures for the dashboard
* [ ] Create the dashboard landing page

# Other Updates

## AirThings RPi Connection
Still debugging this issue, but looks like it is something that others have been struggling with:
* [runs for 5 minutes and then dies](https://github.com/Airthings/waveplus-reader/issues/4)
* [Runs for X minutes and then dies contd...](https://github.com/Airthings/waveplus-reader/issues/14)

I am implementing some of the suggestions mentioned here, but below is a list of possible solutions:
* Remove and Re-insert batteries: not my favorite workaround, but people reported a lot of success with this
* Use the [Unofficial API](https://github.com/ztroop/wave-reader-utils) which might have built-in safeguards for this
* Include a ```disconnect()``` after reading the data
* Change the sampling period
