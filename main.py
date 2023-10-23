"""
This is the main module of Deduplicator.
"""
import redis
from utils import iterate_dirs, md5checksum

MAIN_PATH = "/home/anselmos/Pictures"


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
