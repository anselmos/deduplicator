from typing import Optional
from sqlalchemy import String, Text, Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    """ Base used for tables generation."""
    pass


class File(Base):
    __tablename__ = "files"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    extension: Mapped[str] = mapped_column(String(255))
    path: Mapped[str] = mapped_column(Text)
    md5sum: Mapped[str] = mapped_column(String(255))
    clean: Mapped[bool] = mapped_column(Boolean)
    duplication_paths: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"path={self.path!r} md5: {self.md5sum}"
