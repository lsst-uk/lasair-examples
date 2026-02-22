For more information see [Lasair documentation on Python notebooks](https://lasair.readthedocs.io/en/main/core_functions/python-notebooks.html)


### Requirements
* lasair
* numpy
* matplotlib
* requests
* astropy
* pandas


### Grab your Lasair API token
Get your Lasair token before you start. You can log into [Lasair](https://lasair.lsst.ac.uk) and click "My Profile"
at top right. Or use the command-line below.
```bash
curl --data "username=myusername&password=***********" https://lasair-ztf.lsst.ac.uk/api/auth-token/
```
Make a file called settings.py within the `API_ztf` and `API_lsst` direcotries with a line like: `API_TOKEN = '0123456789abcdefxxxxxxxxxxxxxxxxxxxxxxxx'`

### shell tools:
curl

### API Tokens (must be obtained beforehand - temporary ones used here)
Lasair API token, TNS API token (the latter only for the TDE candidate notebook)