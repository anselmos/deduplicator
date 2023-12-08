import hashlib
import pickle
import contextlib
from os import path, walk, remove

import redis

from const import DUPLICATES_PATH
from images import find_image_date, find_image_dir


def get_paths_redis():
    return redis.Redis(host='localhost', port=6379, decode_responses=True, db=0)


def get_md5sum_redis():
    return redis.Redis(host='localhost', port=6379, decode_responses=True, db=1)


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


def extension_from_name(name):
    extension = name.split(".")
    if len(extension) > 0:
        extension = extension[-1]
    return extension


def find_duplicates(extensions):
    r = get_paths_redis()
    r2 = get_md5sum_redis()
    found_all_not_in_clean_files = {}
    duplicated = {}
    item_nb = 0
    count = r.dbsize()
    for duplicate_key in r.scan_iter(DUPLICATES_PATH + "*"):
        procentage_complete = (item_nb / count) * 100
        item_nb += 1
        print(procentage_complete)
        key_main_path, key_name = path.split(duplicate_key)
        key_extension = extension_from_name(key_name)
        if key_extension not in extensions:
            continue
        key_md5sum = r.get(duplicate_key)
        clean_key = r2.get(key_md5sum)
        if clean_key or duplicate_key == clean_key:
            try:
                duplicated[clean_key].append(duplicate_key)
            except:
                duplicated[clean_key] = [duplicate_key]
        else:
            try:
                found_all_not_in_clean_files[key_main_path].append(duplicate_key)
            except:
                found_all_not_in_clean_files[key_main_path] = [duplicate_key]
    with open('not_in_clean.pkl', 'wb') as f:  # open a text file
        pickle.dump(found_all_not_in_clean_files, f)  # serialize the list

    with open('duplicated.pkl', 'wb') as f:  # open a text file
        pickle.dump(duplicated, f)  # serialize the list


def remove_file(filepath):
    with contextlib.suppress(FileNotFoundError):
        remove(filepath)


def remove_duplicated():
    with open('duplicated.pkl', 'rb') as f:  # open a text file
        duplicated = pickle.load(f)  # serialize the list

    for duplicated_paths in duplicated.values():
        for duplicated_path in duplicated_paths:
            remove_file(duplicated_path)


def move_not_duplicated():
    # todo:
    #  make a json file with paths.
    #  recognize image date.
    #  move file to date-dir in clean dir
    r = get_paths_redis()
    with open('not_in_clean.pkl', 'rb') as f:  # open a text file
        found_all_not_in_clean_files = pickle.load(f)  # serialize the list

    with open('md5sum_to_paths.pkl', 'rb') as f:  # open a text file
        md5sum_to_paths = pickle.load(f)  # serialize the list
    count_all = 0
    # for directory in found_all_not_in_clean_files.keys():
    #     print(directory)
    # exit()
    for directory, file_paths in found_all_not_in_clean_files.items():
        count_all += len(file_paths)
        for file_path in file_paths:
            duplicate_paths = md5sum_to_paths.get(r.get(file_path))
            # if len(duplicate_paths)> 3:
            #     print(file_path, duplicate_paths)
            file_name = path.split(file_path)[1]
            if file_name.split(".")[1] in ["AVI", "RAF"]:
                continue
            found_date = find_image_date(file_name, file_path)
            if found_date:
                # Found date, now find dir:
                found_move_dir = find_image_dir(file_path, found_date)
                # find any additional paths of this file:
                # TODO!!!
                # Create a txt file with all paths:

                # create_description_file(file_path, duplicate_paths)
                # print(file_path, paths, found_date)
                # exit()
                # TODO ADD moved image into "clean" get_paths_redis and get_md5sum_redis
            # else:
            #     print(file_path)

    print(count_all)
