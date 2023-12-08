from os import path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from const import MAIN_PATH
from db.models import File
from .models import Base
from ..utils import get_paths_redis, iterate_dirs, extension_from_name


def get_engine():
    return create_engine("sqlite:///db.sqlite", echo=True)


def create_db():
    Base.metadata.create_all(get_engine())


def save_to_sqlite():
    engine = get_engine()
    r = get_paths_redis()
    paging = 0
    to_session_files = []
    for filepath in iterate_dirs(MAIN_PATH):
        _, name = path.split(filepath)
        extension = extension_from_name(name)
        paging += 1
        checksum = r.get(filepath)
        to_session_files.append(
            {'name': name, 'extension': extension, 'path': filepath, 'md5sum': checksum, 'clean': True})
        if paging == 100:
            with Session(engine) as session:
                session.add_all(
                    [File(**file_data) for file_data in to_session_files])
                session.commit()
            to_session_files.clear()
            paging = 0

