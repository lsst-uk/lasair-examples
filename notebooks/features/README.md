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
A single `diaObject`, together with several `diaSource` and several `diaForcedSou
rce`. The notebook makes a lightcurve plot, then shows  list of (a) a subset of t
he `diaObject` attributes and (b) the features computed by Lasair: all these 
attributes are available to Lasair users to build filters using SQL.

### 2_sherlock.ipynb

### 3_meanChange.ipynb

### 4_extinction.ipynb

### 5_revisit.ipynb

### 6_bazinBlackBody.ipynb

### 8_periodFinder.ipynb
