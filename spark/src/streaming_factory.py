import os
from sys import argv

from streamers import RawStreamer

broker_server = os.getenv("BROKER_HOSTNAME")

if argv[1] == "raw_streamer":
    RawStreamer.create_factory(broker_server)
