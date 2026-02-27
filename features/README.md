## Introduction to Lasair Object Features

These notebooks explain some of the value Lasair adds to each Rubin alert.

You will need to clone this git repo and get an Lasair account and API key.
See [the documentation](https://lasair-lsst.readthedocs.io/en/develop/core_functions/python-notebooks.html)
for more details.

### bazinBlackBody.ipynb
For alerts with a Sherlock host galaxy, a two-dimensional fit is made in
both time and wavelength to look for fast risers and discern their colour.
There are several notebooks in the directory.

### jump.ipynb
This simple feature is to filter out lightcurves with a significant change in brightness. 
The mean and standard deviation are computed from the time between 70 days ago
and 10 days ago.
Then the difference between the latest flux and the mean is divided by the standard deviation:
this is `jump1`.
The same is computed for the other 5 flux bands: this is `jump2`.
If there is a true jump in brightness, we can expect both `jump1` and `jump2` to be
larger than several sigma.

### milky_way.ipynb
Calculation of the extinction E(B-V) and the galactic latitude.
To run this notebook, you will need to install the `dustmaps` package
that puts a 64 Mbyte file on your system.

### pair_analysis.ipynb
The Rubin cadence includes the same object in different wavebands only ~30 minutes
apart, so it is possible to separate rapid brightening from colour. While the
actual colour is reported (eg magnitude difference is 0.99 between filters g and r),
this is also converted to an effective temperature using the blackbody model.

### sherlock_feature.ipynb
The Sherlock system classifies each Lasair alert based on its location in the sky,
finding previously catalogued objects such as variable stars and host galaxy.
In this notebook, we see all the crossmatches that sherlock finds, and 
plots them in position relative to the original alert.
