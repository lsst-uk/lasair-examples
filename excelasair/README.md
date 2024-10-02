# Excelasair
## An Excel-based eyeballing tool for Lasair output

Prerequisites
- Download the [lasair-examples](https://github.com/lsst-uk/lasair-examples) from github.
- `cd excelasair` and `mkdir img`
- Use pip3 to install matplotlib, requests, numpy, astropy, xlswriter, Pillow
- Get your Lasair API token from the top-right of the Lasair web page.
- Write to `lasair-help@mlist.is.ed.ac.uk` and ask to be in the "powerapi" group.
- Make a file `settings.py` with the line `API_TOKEN = 'xxxx`` where xxxx is your token.
- Find the topic name of your active filter (Inactove filters do not have such a name). On the page for your filter, it will say something like "The filter is streamed via kafka with the topic name lasair_2Zooniverse."
- Choose a `groupId`. There is [a video explaining groupId](https://youtu.be/HJneKr1EhmY).
- Edit the program `make_excel.py` with these last two

Each time you run the program, it makes a new spreadsheet with the date as part of the filename, fetching all the results of your filter since last time the program was run with the same `groupId`.
Therefore you can run the program each day, or every few days, to get the latest results. The Excel file can be imported to Microsoft365 or GoogleSheets to add and comment on the filter output, and to share with colleagues.
