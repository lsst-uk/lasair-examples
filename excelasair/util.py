import requests, random, json, time
from datetime import datetime
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
import xlsxwriter

import astropy.io.fits as fits
from astropy.utils.data import download_file
from astropy.table import Table
from astropy.time import Time

from lasair import LasairError, lasair_consumer, lasair_client as lasair
lasairUrl = 'https://lasair-ztf.lsst.ac.uk'

####### PS1 image ###########
def getimages(ra,dec,filters="grizy"):
    """Query ps1filenames.py service to get a list of images

    ra, dec = position in degrees
    size = image size in pixels (0.25 arcsec/pixel)
    filters = string with filters to include
    Returns a table with the results
    """

    service = "https://ps1images.stsci.edu/cgi-bin/ps1filenames.py"
    url = f"{service}?ra={ra}&dec={dec}&filters={filters}"
    try:
        table = Table.read(url, format='ascii')
        return table
    except:
        print(f'Could not fetch URL {url}')
        return None

def geturl(ra, dec, size=240, output_size=None, filters="grizy", format="jpg", color=False):
    """Get URL for images in the table

    ra, dec = position in degrees
    size = extracted image size in pixels (0.25 arcsec/pixel)
    output_size = output (display) image size in pixels (default = size).
                  output_size has no effect for fits format images.
    filters = string with filters to include
    format = data format (options are "jpg", "png" or "fits")
    color = if True, creates a color image (only for jpg or png format).
            Default is return a list of URLs for single-filter grayscale images.
    Returns a string with the URL
    """

    if color and format == "fits":
        raise ValueError("color images are available only for jpg or png formats")
    if format not in ("jpg","png","fits"):
        raise ValueError("format must be one of jpg, png, fits")
    table = getimages(ra,dec,filters=filters)
    if not table:
        return None
    url = (f"https://ps1images.stsci.edu/cgi-bin/fitscut.cgi?"
           f"ra={ra}&dec={dec}&size={size}&format={format}")
    if output_size:
        url = url + "&output_size={}".format(output_size)
    # sort filters from red to blue
    flist = ["yzirg".find(x) for x in table['filter']]
    table = table[np.argsort(flist)]
    if color:
        if len(table) > 3:
            # pick 3 filters
            table = table[[0,len(table)//2,len(table)-1]]
        for i, param in enumerate(["red","green","blue"]):
            url = url + "&{}={}".format(param,table['filename'][i])
    else:
        urlbase = url + "&red="
        url = []
        for filename in table['filename']:
            url.append(urlbase+filename)
    return url

def getcolorim(ra, dec, size=240, output_size=None, filters="grizy", format="jpg"):
    """Get color image at a sky position

    ra, dec = position in degrees
    size = extracted image size in pixels (0.25 arcsec/pixel)
    output_size = output (display) image size in pixels (default = size).
                  output_size has no effect for fits format images.
    filters = string with filters to include
    format = data format (options are "jpg", "png")
    Returns the image
    """

    if format not in ("jpg","png"):
        raise ValueError("format must be jpg or png")
    url = geturl(ra,dec,size=size,filters=filters,output_size=output_size,format=format,color=True)
    try:
        r = requests.get(url)
        im = Image.open(BytesIO(r.content))
        return im
    except:
        print(f'PS1 image URL failed {url}')
        return None

def showPS1(filename, objectData, size):
    fig = plt.figure(frameon=False)
    fig.set_size_inches(size['cell_size'], size['cell_size'])
    ax = fig.add_subplot(111)
    ax = plt.Axes(fig, [0., 0., size['cell_size'], size['cell_size']])
    ax.set_axis_off()
    fig.add_axes(ax)

    cim = getcolorim(
        objectData['ramean'], objectData['decmean'],
        size=300,
        filters="grz")
    if cim:
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.imshow(cim, origin="upper")
        ax.set_title('Pan-STARRS')
    plt.savefig(filename, dpi=72)

########## show cutout images #############
def show_fits(filename, url_tem, title, size):
    fig = plt.figure(frameon=False)
    fig.set_size_inches(size['cell_size'], size['cell_size'])
    ax = fig.add_subplot(111)
    ax = plt.Axes(fig, [0., 0., size['cell_size'], size['cell_size']])
    ax.set_axis_off()
    fig.add_axes(ax)
    try:
        image_file = download_file(url_tem, cache=True )
        hdu_list = fits.open(image_file, ignore_missing_simple=True)
        image_data = hdu_list[0].data
    except:
        return

    minid = np.min(image_data)
    maxid = np.max(image_data)

    image_data = (image_data - minid + 1)/(maxid-minid)
    image_data = np.log(image_data)
    ax.imshow(image_data, cmap='gray', aspect='auto')
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_title(title)
    plt.savefig(filename, dpi=72)

######## make lightcurve image #######
def make_lightcurve(filename, candidates, size):
    jdnow         = Time.now().jd
    last_candidate = None
    for c in candidates:
        if not 'candid' in c: continue
        last_candidate = c
        break

    colourFromFid = {1:'green', 2:'red', 3:'blue'}
    plt.rcParams.update({'font.size': 6})
    dpi = 72
    w = 3*size['cell_size']
    h = 1*size['cell_size']
    fig, ax=plt.subplots(figsize=(w*dpi,h*dpi), dpi=dpi)
    fig.set_size_inches(w, h)
    for c in candidates:
        if not 'candid' in c:
            continue
        if not last_candidate:
            last_candidate = c
        if 'isdiffpos' in c:
            if c['isdiffpos']=='t':
                ax.errorbar(c['jd']-jdnow,c['magpsf'],c['sigmapsf'],
                    color=colourFromFid[c['fid']])
#                    fmt='o',color=colourFromFid[c['fid']])
    ax.invert_yaxis()
    ax.set_xlabel('Days ago')
    ax.set_xlim(right=0)
    plt.savefig(filename, dpi=dpi)

######### build the excel spreadsheet ##############
def pprint(var):
    if type(var) is float: return('%3f' % var)
    return(str(var))

def make_header(worksheet, nrow, filter_row, xlsxformat, renderImages, size):
    types = []
    ncol = 0

    for key,value in filter_row.items():
        worksheet.write(nrow, ncol, key, xlsxformat)
        types.append(type(value).__name__)
        ncol += 1

    worksheet.write(nrow, ncol, 'TNS name', xlsxformat)
    types.append('string')
    ncol += 1
    worksheet.write(nrow, ncol, 'TNS type', xlsxformat)
    types.append('string')
    ncol += 1
    worksheet.set_column_pixels(0, ncol-1, size['fieldwidth'])

    if renderImages:
        worksheet.write(nrow, ncol, 'Lightcurve', xlsxformat)
        worksheet.set_column_pixels(ncol, ncol, size['lcwidth'])
        types.append('image')
        ncol += 1

        worksheet.set_column_pixels(ncol, ncol+3, size['cutoutwidth'])
        worksheet.write(nrow, ncol, 'Template', xlsxformat)
        types.append('image')
        ncol += 1
        worksheet.write(nrow, ncol, 'Science', xlsxformat)
        types.append('image')
        ncol += 1
        worksheet.write(nrow, ncol, 'Pan-STARRS', xlsxformat)
        types.append('image')
        ncol += 1
    return types

def handle_filter_row(worksheet, nrow, columns, filter_row, objectData, xlsxformat, renderImages, size):
    ncol = 0
    jdnow         = Time.now().jd
    objectId      = filter_row['objectId']

    #### attributes from the SELECT of the filter
    for key,value in filter_row.items():
        worksheet.write(nrow, ncol, str(value), xlsxformat)
        ncol += 1

    #### TNS entries  #####
    candidates    = objectData['candidates']
    last_candidate = None
    for c in candidates:
        if not 'candid' in c: continue
        last_candidate = c
        break
    t = Time(last_candidate['jd'], format='jd')
    iso = t.to_value('iso', subfmt='date_hm')
    if 'TNS' in objectData:
        tns = objectData['TNS']
        if 'tns_name' in tns: 
            worksheet.write(nrow, ncol, tns['tns_name'], xlsxformat)
        ncol += 1
        if 'type' in tns:
            worksheet.write(nrow, ncol, tns['type'], xlsxformat)
        ncol += 1
    else:
        ncol += 2

    rowkey = '%04d' % nrow

    #### lightcurve ####
    filename = 'img/lightcurve'    + rowkey + '.png'
    make_lightcurve(filename, candidates, size)
    worksheet.insert_image(nrow, ncol, filename)
    ncol += 1

    # Image cutouts if available
    if renderImages:
        if "image_urls" in last_candidate:
            filename = 'img/template'    + rowkey + '.png'
            show_fits(filename, last_candidate["image_urls"]["Template"], 'Template', size)
            worksheet.insert_image(nrow, ncol, filename)
            ncol += 1

            filename = 'img/science'    + rowkey + '.png'
            show_fits(filename, last_candidate["image_urls"]["Science"], 'Science', size)
            worksheet.insert_image(nrow, ncol, filename)
            ncol += 1
        else:
            ncol += 2

        # PS1 image
        filename = 'img/pannstarrs'    + rowkey + '.png'
        showPS1(filename, objectData['objectData'], size)
        worksheet.insert_image(nrow, ncol, filename)
        ncol += 1

def group_id_to_end(kafka_server, group_id, my_topic):
    consumer = lasair_consumer(kafka_server, group_id, my_topic)
    print('Connected to Kafka')

    n = 0
    while 1:
        msg = consumer.poll(timeout=20)
        if msg is None:
            break
        if msg.error():
            print(str(msg.error()))
            break
        n += 1
    consumer.close()
    print("%d alerts skipped, no more in queue" % n)

def run(token, kafka_server, group_id, my_topic, \
    excelFile=None, maxAlerts=10, renderImages=True, cellSize=1):

    if not excelFile:
        date = datetime.today().strftime('%Y%m%d')
        excelFile = '%s_%s.xlsx' % (my_topic, date)
    
    L = lasair(token, endpoint=lasairUrl+'/api')
    consumer = lasair_consumer(kafka_server, group_id, my_topic)
    print('Connected to Kafka')

    n = 0
    filter_row_list = []
    while n < maxAlerts:
        msg = consumer.poll(timeout=20)
        if msg is None:
            break
        if msg.error():
            print(str(msg.error()))
            break
        filter_row = json.loads(msg.value())
        filter_row_list.append(filter_row)
        n += 1
    consumer.close()
    print('%d filter data fetched' % len(filter_row_list))

    objectIdList = [fr['objectId'] for fr in filter_row_list]

    print('Fetching', objectIdList)
    if len(objectIdList) == 0:
        print('No more records to fetch')
        return

    t = time.time()
    try:
        objectDataList    = L.objects(','.join(objectIdList))
    except LasairError as e:
        print('Exception from Lasair API: %s' % str(e))
        return
    print('%d object data fetched in %.0f seconds' % \
        (len(objectDataList), (time.time() - t)))

    nrow = 0
    workbook = None
    for i_filter_row in range(len(filter_row_list)):
        filter_row  = filter_row_list[i_filter_row]
        objectData  = objectDataList [i_filter_row]

        if i_filter_row == 0:
            size = {}
            size['cell_size']   = cellSize
            size['rowheight']   = 80*cellSize
            size['fieldwidth']  = 80*cellSize
            size['lcwidth']     = 50 + 250*cellSize
            size['cutoutwidth'] = 100*cellSize
            workbook = xlsxwriter.Workbook(excelFile)
            xlsxformat=workbook.add_format()
            xlsxformat.set_align('center')
            xlsxformat.set_align('vcenter')
            worksheet = workbook.add_worksheet()
            worksheet.set_default_row(size['rowheight'])
            types = make_header(worksheet, nrow, filter_row, xlsxformat, renderImages, size)
            nrow += 1

        objectId = filter_row['objectId']
        handle_filter_row(worksheet, nrow, types, \
            filter_row, objectData, xlsxformat, renderImages, size)
        nrow += 1

    print(f'Converted {n} cells to excel')
    if workbook:
        workbook.close()
