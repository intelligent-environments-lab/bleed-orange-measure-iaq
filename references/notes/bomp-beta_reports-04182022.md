# Reports for Beta Deployment
Get some summary statistics and visualizations in order for the 5th floor participants 

## Analyses to Report
The subsections below outline some of the items I think we should include. Some general information:
* Sensor Kit Deployment: 02/10 - 03/10
* Three spaces to consider:
  * 5.302 (Leite)
  * 5.438 (Faust)
  * 5.430 (Novoselac)

The first step will be to download the data from these three spaces from both device types. 

### Weekly Profile and Summary
Since our devices were out for 28 days, I think it makes sense to summarize the weekly measurements with visuals and statistics:
1. Generate 4 time series plots for each week:
  * CO2 from AirThings
  * TVOC from AirThings
  * T/RH (on one plot with dual y-axis) from AirThings
  * PM2.5 from PurpleAir (make sure it is ug/m3 and not AQI)
2. Calculate the following statistics for each of the 5 parameters with _and_ without weekends included i.e. we would have two of each metric below for weekday and for week:
  * minimum
  * mean
  * median
  * max
3. Save figures and summary stats to file and share with Hagen

### Occupancy Detection
The CO2 concentrations are going to be sensitive to when the professors are in the space as well as the TVOC sensor. I am thinking we develop a model that can detect when professors are in their offices by first manually inspecting the data, labeling clearly occupied periods, then creating a machine learning model that detects the remaining periods. While a neat exercise, this analysis would also help normalize some of the measurements since professors might be occupying their spaces for different amounts of time. 
1. Using CO2 data, manually inspect profiles from the pervious analysis to find periods that are _clearly_:
  * occupied
  * unoccupied
2. For each participant's dataset, create a new column called "occupied" and for the time periods you identified, input 1 for each timestamp/row the office is occupied and 0 for each timestamp/row the office is unoccupied
3. Save augmented datasets and share with Hagen

### Single Office Space Comparison
We should compare the measurements in one office to the aggregated measurements from the other two office spaces on that floor:
* Leite to Faust+Novoselac
* Faust to Leite+Novoselac
* Novoselac to Faust+Leite

We can easily compare summary statistics but I am thinking it would be neat to include a figure that compares the distributions of values. A simple visual would be split violin plots for each parameter where one side of the violin is the office in question and the other side contains the aggregated measurements.
1. For each device type, we need to combine data from each office space into one dataset so we would have:
  * AirThings dataset which includes CO2, TVOC, T, and RH data from the three office spaces from 02/10 - 03/10
  * PurpleAir dataset which includes PM2.5, T, and RH data from the three office spaces from 02/10 - 03/10
2. Save and share new datasets with Hagen
