import json, lasair
ra = 295.744446
de = 12.083441

Llsst = lasair.lasair_client('b5fdcda4b8416f95466147c2514422589b7a3693',
    endpoint='https://lasair-lsst.lsst.ac.uk/api')
sherl = Llsst.sherlock_position(ra, de, lite=False)
print(json.dumps(sherl['classifications'], indent=2))

Lztf = lasair.lasair_client('8c97c954ddef90faa1f16866a12b046a504ab7e4', 
    endpoint='https://lasair-ztf.lsst.ac.uk/api')
sherl = Lztf.sherlock_position(ra, de, lite=False)
print(json.dumps(sherl['classifications'], indent=2))

