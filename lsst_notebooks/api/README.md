## Introduction to Lasair Object Features

These notebooks explain some of the value Lasair adds to each Rubin alert.

You will need to clone this git repo and get an Lasair account and API key.
See [the documentation](https://lasair-lsst.readthedocs.io/en/develop/core_functions/python-notebooks.html)
for more details.

### cone.ipynb
The cone search method of the API finds objects within a cone, 
i.e. a point in the sky and radius in arcseconds. 
It can return:
- A count of the number in the cone
- The nearest of those in the cone
- All of those in the cone

### object.ipynb
For a given object, identified by its `diaObjectId`, the `object` API call has two additional arguments:
- `lasair_added`: True if you want the attributes that Lasair computes the attributes in the 
[schema](https://lasair.lsst.ac.uk/schema/), as well as the Sherlock association, TNS crossmatch,
and links to all the image cutouts.
- `lite` True if you want the simplified version that is usually sufficient, or False if
you want the large number of attributes that Rubin has supplied.

### query.ipynb
This notebook runs a Lasair filter using three strings: `selected`, 'tables', and 'conditions', as
in the web interface. In this case we just fina a few objects thta have a Sherlock host association.

### sherlock_api.ipynb
Demonstrates the two Sherlock calls: one by `diaObjectId` and the other by sky position ra, dec.

### watchlist.ipynb
This notebook runs a Lasair filter that includes a watchlist.
