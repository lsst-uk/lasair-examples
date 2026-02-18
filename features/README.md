## Introduction to Lasair Object Features

These notebooks explain some of the value Lasair adds to each Rubin alert.
The first thing to do is get a Lasair account 
(here)[https://lasair.lsst.ac.uk/register/], and log in, then click on your 
name at the top right, and choose “My Profile”. The API key is shown there.
```
cp settings_template.py settings.py
```
then edit `settings.py` and put your API key instead of the dummy.

### 1_whatIsAnObject.ipynb
Here we see the three main data objects that arrive from Rubin: 
A single `diaObject`, together with several `diaSource` and several `diaForcedSource`. The notebook makes a lightcurve plot, then shows  list of (a) a subset of t
he `diaObject` attributes and (b) the features computed by Lasair: all these 
attributes are available to Lasair users to build filters using SQL.

### 2_sherlock.ipynb
The Sherlock system classifies each Lasair alert based on its location in the sky,
finding previously catalogued objects such as variable stars and host galaxy.

### 3_meanChange.ipynb
This simple feature is to filter out lightcurves with a significant change in brightness. It lumps together all 6 wavebands into new and old, then uses 
Student's t-test to decide if the mean flux has changed. There are two versions of 
the feature: one compares the last 10 days to the previous 10 days; the other compares
the last 20 days to the previous 20 days.

### 4_milky_way.ipynb
Calculation of the extinction E(B-V) and the galactic latitude.

### 5_revisit.ipynb
The Rubin cadence includes the same object in different wavebands only ~30 minutes
apart, so it is possible to separate rapid brightening from colour. While the
actual colour is reported (eg magnitude difference is 0.99 between filters g and r),
this is also converted to an effective temperature using the blackbody model.

### 6_bazinBlackBody.ipynb
For alerts with a Sherlock host galaxy, a two-dimensional fit is made in
both time and wavelength to look for fast risers and discern their colour.
Two models are tried: blackbody in wavelength times exponential in flux (linear in 
magnitude) and blackbody times Bazin in flux (exponential rise and exponential
fall).

### 7_periodFinder.ipynb
The conditional entropy method is used to discover 
any periodicity in a long lightcurve. The period and its relability is reported.
