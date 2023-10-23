import hashlib
from os import path, walk


def md5checksum(filename):
    # based on https://stackoverflow.com/a/3431838
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def iterate_dirs(init_path):
    for (root, dirnames, filenames) in walk(init_path):
        for filename in filenames:
            yield path.join(root, filename)
