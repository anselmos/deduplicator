from datetime import datetime
from PIL import Image, ExifTags, UnidentifiedImageError
from os import path, makedirs
import shutil

def read_image_exif_data(img):
    exif = {}
    try:
        exif_items = img._getexif()
    except AttributeError:
        exif_items = None
    if exif_items is not None:
        exif = {
            ExifTags.TAGS[k]: v
            for k, v in exif_items.items()
            if k in ExifTags.TAGS
        }
    return exif


def find_date_by_file_name(file_name):
    vid_name = file_name.split('VID_')
    if vid_name and len(vid_name) ==2:
        date_by_vid_name = vid_name[1].split(".")[0]
        return datetime.strptime(date_by_vid_name[:-3], '%Y%m%d_%H%M%S')
    pic_img_name = file_name.split("IMG_")
    if len(pic_img_name) > 1:
        return datetime.strptime(pic_img_name[1][:-7], '%Y%m%d_%H%M%S')
    return datetime.strptime(file_name[:15], '%Y%m%d_%H%M%S')

def find_image_date(file_name, file_path):
    found_date = None
    try:
        image_data = Image.open(file_path)
        exif = read_image_exif_data(image_data)
        if 'DateTime' in exif.keys():
            found_date = exif.get('DateTime')
        elif 'DateTimeOriginal' in exif.keys():
            found_date = exif.get('DateTimeOriginal')
    except (UnidentifiedImageError, OSError):
        pass
    if not found_date:
        try:
            found_date = find_date_by_file_name(file_name)
        except ValueError as val_err:
            # print("VALUE ERROR", val_err)
            pass
    if isinstance(found_date, str):
        try:
            return datetime.strptime(found_date, "%Y:%m:%d %H:%M:%S")
        except:
            print("FOUND DATE NOT CONVERTED:(", found_date)
            return None
    return found_date

def find_image_dir(file_path: str, image_date: datetime):
    main_dir, file_name = path.split(file_path)
    images_dir = path.split(main_dir)[-1]
    default_date_format = "%Y_%m_%d"
    default_date_formatted = image_date.strftime(default_date_format)
    format2 = "%Y-%m-%d"
    format1 = "%d_%m_%Y"
    if default_date_formatted in images_dir:
        return images_dir
    elif image_date.strftime(format1) in images_dir:
        return default_date_formatted + images_dir.split(image_date.strftime(format1))[1]
    elif image_date.strftime(format2) in images_dir:
        return default_date_formatted + images_dir.split(image_date.strftime(format2))[1]
    if default_date_formatted not in images_dir:
        return default_date_formatted + "_" + images_dir.replace(" ", "_")
    return default_date_formatted
    # TODO!!!

def create_description_file(file_path, paths):
    description_file = f"{file_path}.txt"
    with open(description_file, "w+") as fp:
        items_paths = "\n".join([f"{path}" for path in paths])
        fp.write(items_paths)

def copy_file_into_date_dir(file_src, year_dir, date_image, clean_path_dir, dry_run=False, dir_path=None, append_date_image_path=None, replace_dir=None):
    dir_path += f"/{year_dir}/{date_image}"
    if not replace_dir and append_date_image_path:
        dir_path += f"_{append_date_image_path}"
    if date_image == "":
        dir_path = f"{clean_path_dir}/NO_DATE/"
    if not path.exists(dir_path):
        if dry_run:
            print(f"Create dir: {dir_path}")
            print(f"Copy file: {file_src} into {dir_path}")
        else:
            makedirs(dir_path)

    if path.exists(dir_path):
        if not dry_run:
            try:
                shutil.copy(file_src, dir_path)
            except shutil.SameFileError as same_file_error:
                print("shutil.SameFileError", str(same_file_error))
    return dir_path