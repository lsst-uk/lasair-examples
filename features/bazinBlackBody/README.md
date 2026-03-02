## Introduction to Lasair Object Features

These notebooks explain some of the value Lasair adds to each Rubin alert.

You will need to clone this git repo and get an Lasair account and API key.
See [the documentation](https://lasair-lsst.readthedocs.io/en/develop/core_functions/python-notebooks.html)
for more details.

### introduction.ipynb
Start here to see what precisely this code it doing.
It is fitting a 2D surface to the lightcurve, with time in one dimension and wavelength in the other.
The fit to the flux can be either exponential in time (linear in magnitude), 
or with a Bazin explosion model -- exponential rise in flux then exponential fall.

### example.ipynb
This notebook reads a simulated supernova lightcurve from a file, then fits it and plots the result.

### synthetic.ipynb
This notebook creates a BazinBlackbody lightcurve surface, then fits it and plots the result.

### api_plot_lsst.ipynb
This notebook runs the fit for an arbitrary object in the Lasair database.
To see the result for another object, change the 2nd last line of the notebook where it says
`diaObjectId = ...` to the `diaObjectId` of your chosen object.

