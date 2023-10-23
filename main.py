"""
This is the main module of Deduplicator.
"""
import redis
import os
from dotenv import load_dotenv
from utils import iterate_dirs, md5checksum

load_dotenv()

MAIN_PATH = os.getenv('MAIN_PATH')


def main():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    for filepath in iterate_dirs(MAIN_PATH):
        checksum = md5checksum(filepath)

        found_file = r.get(checksum)
        if found_file and filepath != found_file:
            # TODO - push this into sqlite/second redis/ same redis with different key?.
            print("found duplicate, ORG: =>", found_file, "DUPLICATE: => ", filepath)
        else:
            r.set(checksum, filepath)


if __name__ == "__main__":
    main()
