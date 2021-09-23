import os
from sys import argv

from streamers import RawStreamer, JoinUsersStreamer, TrustedStreamer

broker_server = os.getenv("BROKER_HOSTNAME")

if argv[1] == "raw_streamer":
    RawStreamer.create_factory(broker_server)
elif argv[1] == "trusted_streamer":
    TrustedStreamer.create_factory()
elif argv[1] == "join_users_streamer":
    JoinUsersStreamer.create_factory()
