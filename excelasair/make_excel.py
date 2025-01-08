import settings
from util import run

# Uncomment one of these or put in your own
myTopic     = 'lasair_2Lightweight'
myTopic     = 'lasair_2Zooniverse'
myTopic     = 'lasair_855BBBfastriser'

# The group_id is like a bookmark: 
# the kafka server remembers the last alert it gave you.
groupId     = 'roysgroupid991'

lasairUrl     = "https://lasair-ztf.lsst.ac.uk/"
kafkaServer = 'kafka.lsst.ac.uk:9092'

run(
    settings.API_TOKEN, 
    kafkaServer, 
    groupId, 
    myTopic, 
    maxAlerts=50, 
    cellSize=1.25
)
