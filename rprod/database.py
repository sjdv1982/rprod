from concurrent.futures import ThreadPoolExecutor
import functools
import os

if "SEAMLESS_DATABASE_IP" not in os.environ:
    os.environ["SEAMLESS_DATABASE_IP"] = "localhost"
if "SEAMLESS_DATABASE_PORT" not in os.environ:
    os.environ["SEAMLESS_DATABASE_PORT"] = "5522"

# TODO: local mode database ("rprod --database")

from seamless import database_cache, database_sink

database_cache.connect()
database_sink.connect()


def set_buffer(checksum, buffer):
    database_sink.set_buffer(checksum, buffer, persistent=False)


def need_buffer(checksum):
    return not database_sink.has_buffer(checksum)


def has_buffer(checksum):
    return database_cache.has_buffer(checksum)


_ = None  # STUB
