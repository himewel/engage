import os
import logging
from sys import argv

from streamers import CacheStreamer, ContextStreamer, RawStreamer

broker_server = os.getenv("BROKER_HOSTNAME")

logging.basicConfig(
    format="[%(levelname)s] %(name)s - %(message)s",
    level=logging.INFO,
)

if argv[1] == "raw_streamer":
    RawStreamer.create_factory(broker_server)
elif argv[1] == "context_streamer":
    ContextStreamer.create_factory(broker_server)
elif argv[1] == "cache_streamer":
    CacheStreamer.create_factory(broker_server)
