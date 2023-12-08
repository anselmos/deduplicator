"""
This is the main module of Deduplicator.
"""
import logging
import pickle

from utils import find_duplicates, iterate_dirs, md5checksum, get_paths_redis, get_md5sum_redis, remove_duplicated

logging.disable(logging.WARNING)


def cache_to_redis_by_md5(path):
    """ Caches MD5sum in redis for quicker retrieval of files later-on."""
    r = get_paths_redis()
    r.flushdb()
    for filepath in iterate_dirs(path):
        checksum = md5checksum(filepath)
        r.set(filepath, checksum)


def cache_md5sum_as_key(path):
    r = get_md5sum_redis()
    r.flushdb()
    for filepath in iterate_dirs(path):
        checksum = md5checksum(filepath)
        r.set(checksum, filepath)


def dict_md5_sum_as_key():
    r = get_paths_redis()
    md5sum_to_paths = {}
    for file_path in r.scan_iter("*"):
        md5check = r.get(file_path)
        try:
            md5sum_to_paths[md5check].append(file_path)
        except:
            md5sum_to_paths[md5check] = [file_path]

    with open('md5sum_to_paths.pkl', 'wb') as f:  # open a text file
        pickle.dump(md5sum_to_paths, f)  # serialize the list


def main():
    # cache_md5sum_as_key(MAIN_PATH)
    # cache_to_redis_by_md5(MAIN_PATH)
    # cache_to_redis_by_md5(DUPLICATES_PATH)
    # dict_md5_sum_as_key()
    # find_duplicates(["jpg", "JPG", "png", "PNG", "jpeg", "JPEG", "bmp", "BMP", "AVI", "RAF", "MP4", "MOV", "avi", "3gp", "mov"])
    remove_duplicated()

if __name__ == "__main__":
    main()
