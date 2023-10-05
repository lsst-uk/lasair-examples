# A Marshall for Lasair filter output
Show lightcurve and cutouts from given Lasair topic
with option to build veto list (dont show me this object again),
as well as favourite list, each with a reason given. 
Stored on users own machine.

## Instructions:

- Find a Lasair filter whose results you want to inspect
- Make sure it is set to Kafka output
- Get the `topic_name` and the selected attributes you want to see from your filter

- `$ git clone https://github.com/lsst-uk/lasair-examples.git`
- `$ cd lasair-examples/notebooks/marshall`
- `$ pip3 install -r requirements.txt`
- Get your token from Lasair and make a file called `settings.py` with the single line
-    ```API_TOKEN = '8c97c954ddef90faa1f16866a12b046a504ab7e4'```
- `$ jupyter notebook`
- Select Marshall.ipynb and start it
- Modify `my_topic` and `showAttr` depending on your Lasair filter
- Choose Run / Run All Cells
- Check the "veto" and "fave" boxes to veto or favourite
- At the bottom pf the output click "Save veto/fave choices"
