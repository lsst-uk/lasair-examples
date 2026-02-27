#!/usr/bin/env python3

"""
Kafka Consumer Script Template

Requires:
- lasair 

(everything else is standard python)

"""

from datetime import datetime
import json
from lasair import lasair_consumer, LasairError
import logging
from pathlib import Path
import os
import random # Only needed to randomise group_id which is a TUTORIAL ONLY shenanigan



# ###################################################################### #
#                                CONSTANTS                               #
# ###################################################################### #

# ---------------------------- CHANGE THESE :)  ------------------------ #

# INTPUT SET UP
# Number of alerts to poll from your kafka queue every time you "consume"
N_MESSAGES = 100

# Which Filter you want to listen to
TOPIC = "lasair_83lasair_tutorial_basic_stream"

# Your group_id which saves your position in the queue!
# TODO: You have to change this to something NOT RANDOM if you want to 
# don't want to start from the start of the queue every time. 
GROUP_ID     = "tutorial"+str(int(random.random()*10000000000)) # RANDOM ID

# Q&A: Why did you randomise it then?
# Because I am making you use the basic tutorial filter 
# If I also give you a set `test_group_id` then everyone who runs these 
# will be interfering with each other. 
# TODO: ASK GARETH IF THAT'S CORRECT OR IF I HAVE THIS WRONG

# OUTPUT DIRECTORY
OUTPUT_DIR = Path("/tmp/lasair_tutorial_output/") # Change this to your desired output directory

# ---------------------------------------------------------------------- #
# NOTE: the logging is extra ;) 
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    handlers=[logging.StreamHandler()])
logging.info("---- START --- ")
# ---------------------------------------------------------------------- #


# /////////////////////////// DO NOT TOUCH THIS \\\\\\\\\\\\\\\\\\\\\\\\\ #
# ////////////////// Unless you know what you're doing \\\\\\\\\\\\\\\\\\ #
#KAFKA_SERVER =lasair-lsst-kafka_pub.lsst.ac.uk:9092
# ENDPOINT = 'https://lasair.lsst.ac.uk/api'
KAFKA_SERVER = 'lasair-lsst-dev-kafka_pub.lsst.ac.uk:9092'
ENDPOINT = 'https://lasair-lsst-dev.lsst.ac.uk/api'

# ///////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ #



# ###################################################################### #
#                             MAIN CODE                                  #
# ###################################################################### #

# ######## CREATE OUR CONSUMER OBJECT ############### #

consumer = lasair_consumer(host=KAFKA_SERVER, 
                            group_id=GROUP_ID,
                            topic_in=TOPIC)


# ######## SET UP WHERE THE FILES WILL GO ########### #

# --------------- Change this If you Want ----------- #
# I like having my jsons named by date and time
# FEEL FREE TO CHANGE THIS 
stem = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
# --------------------------------------------------- #


OUTPUT_DIR.mkdir(parents=True, exist_ok=True) # Make sure the output directory exists
out_path = OUTPUT_DIR / f"{stem}.json" # with_suffix below REPLACES the .json
tmp_path = out_path.with_suffix(".jsn.tmp")  # <-- temporary while writing



# ######## POLL ONE MESSAGE AT A TIME ################ #

n = 0
first = True

# To ensure we don't leave out file open we work within a `with` scope
with open(tmp_path, "w", encoding="utf-8") as f:
    # first we write the opening square bracket for the json list
    f.write("[\n")
    while n < N_MESSAGES:
        msg = consumer.poll(timeout=20)
        if msg is None:
            break
        if msg.error():
            raise LasairError("Error while consuming message: {}".format(msg.error()))
            break
        # 2. If we make it here it means we have messages. 
        raw = msg.value()
        # msg.value() may be bytes or str depending on client
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8")

        # 3. Get the JSON data for our alert.
        result = json.loads(raw)
        
        # write comma before each object after the first
        if not first:
            f.write(",\n")
        first = False
        
        json.dump(result, f, indent=2, ensure_ascii=False)


        n += 1
    f.write("]\n")

# ###### POST-PROCESSING - HANDLING TEMP FILES ######## #
# If we ingested nothing we don't need a file, so we'll delete it
# If we DID ingest, we want to rename the file 
try:
    if first == True:
        # no messages received — remove the temp file if it exists
        if tmp_path.exists():
            tmp_path.unlink()
        logger.info("EMPTY Ran but no messages received — no file written.")
    else:
        # RENAMING
        # Atomically replace any existing final file with the tmp file
        os.replace(str(tmp_path), str(out_path))
        logger.info(f"Successfully wrote {n} messages to {out_path}")

except Exception as e:
    logger.exception("Error finalizing output file; temporary file left for inspection.")
    raise e