import os, lasair

if __name__ == "__main__":
    endpoint = 'https://api.lasair.lsst.ac.uk/api'
    diaObjectId = 313853517588594758
    topic_out = 'test_annotator'
 
    # Fake classification
    classification = 'apple'

    # JSON dictionary
    classdict = {'fruit': 'apple'}

    # Create Lasair client
    API_TOKEN = os.getenv('LASAIR_LSST_TOKEN')
    if API_TOKEN is None:
        print("No Token found")
    L = lasair.lasair_client(API_TOKEN, endpoint=endpoint)

    # Send the annotation
    L.annotate(
        topic_out, 
        diaObjectId, 
        classification,
        version='0.1', 
        explanation='a nice fruit', 
        classdict=classdict, 
        url='')
    print('success')
