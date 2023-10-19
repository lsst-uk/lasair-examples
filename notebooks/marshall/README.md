# A Marshall for Lasair filter output
![Screenshot](marshall/marshall_screenshot.png)
Show lightcurve and cutouts from given Lasair topic
with option to build veto list (dont show me this object again),
as well as favourite list, each with a reason given. 
Stored on users own machine.
**NOTE**: This notebook connects to the Lasair Kafka service on port 9092. 
If you are on a restricted network such as eduroam, that port may be blocked, 
and a VPN will be necessary.

## Instructions:

- Find a Lasair filter whose results you want to inspect
- Make sure it is set to Kafka output
- Get the `topic_name` and the selected attributes you want to see from your filter

- `$ git clone https://github.com/lsst-uk/lasair-examples.git`
- `$ cd lasair-examples/notebooks/marshall`
- `$ pip3 install -r requirements.txt`
- Get your token from Lasair and make a file called `settings.py` with the single line
    -    ```API_TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'```
    - where the XXX is your own token
- `$ jupyter notebook`
- Select Marshall.ipynb and start it
- Modify `my_topic` and `group_id` and `showAttr` as written in the notebook
- Choose Run / Run All Cells
- Check the "veto" and "fave" boxes to veto or favourite
- At the bottom pf the output click "Save veto/fave choices"

