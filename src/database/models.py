from sqlalchemy import (Column,
                        INT,
                        event,
                        BOOLEAN,
                        Table,
                        VARCHAR,
                        func,
                        ForeignKey,
                        CheckConstraint,
                        PrimaryKeyConstraint,
                        ForeignKeyConstraint,
                        TIMESTAMP,
                        CHAR)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import INTERVAL
from sqlalchemy.sql.functions import now

from .base import Base
from .types import FileType
from .storage import FileSystemStorage

from transliterate import translit


__all__ = (
    "Base",
    "BookPrivate",
    "BookPrivateTag",
    "Category",
    "User",
    "Tag",
    "GeneralBook",
    "GeneralBookTag",
)

import re
import unicodedata


def slugify(value, allow_unicode=False):
    # Transliterate Cyrillic to Latin
    value = translit(value, 'ru', reversed=True)

    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


class BookPrivateTag(Base):
    __tablename__ = "book_private_tags"

    tag_id = Column(ForeignKey(
        "tags.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        primary_key=True
    )
    book_private_id = Column(ForeignKey(
        "books_private.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        primary_key=True
    )


class GeneralBookTag(Base):
    __tablename__ = "general_books_tags"

    tag_id = Column(ForeignKey(
        "tags.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        primary_key=True
    )
    general_book_id = Column(ForeignKey(
        "general_books.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        primary_key=True
    )


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (
        CheckConstraint(sqltext="length(name) >= 2"),
    )

    id = Column(INT, primary_key=True)
    name = Column(VARCHAR(length=32), nullable=False, unique=True)
    slug = Column(VARCHAR(length=128), nullable=True)

    books_private = relationship(argument="BookPrivate", back_populates="category")
    general_books = relationship(argument="GeneralBook", back_populates="category")

    def __str__(self) -> str:
        return self.name

    def generate_slug(self):
        self.slug = slugify(self.name)
        print(self.slug)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(INT, primary_key=True)
    name = Column(VARCHAR(length=32), nullable=False, unique=True)

    general_books = relationship(argument="GeneralBook", secondary=GeneralBookTag.__table__, back_populates="tags_general")
    books_private = relationship(argument="BookPrivate", secondary=BookPrivateTag.__table__, back_populates="tags_private")

    def __str__(self) -> str:
        return self.name


class BookPrivate(Base):
    __tablename__ = "books_private"

    id = Column(INT, primary_key=True)
    title = Column(VARCHAR(length=128), nullable=False)
    slug = Column(VARCHAR(length=128), nullable=True)
    author = Column(VARCHAR(length=128), nullable=False)
    created_at = Column(TIMESTAMP, server_default="now()", nullable=False)
    is_published = Column(BOOLEAN, server_default="false", nullable=False)
    picture = Column(FileType(storage=FileSystemStorage(upload_to="media")), nullable=True, default='blank.png')
    category_id = Column(
        INT,
        ForeignKey(column=Category.id, ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False
    )
    general_book_id = Column(
        INT,
        ForeignKey(column="general_books.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=True
    )
    user_email = Column(
        VARCHAR(length=128),
        ForeignKey(column="users.email", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=True
    )

    general_book = relationship(argument="GeneralBook", back_populates="books_private")
    category = relationship(argument=Category, back_populates="books_private")
    tags_private = relationship(argument=Tag, secondary=BookPrivateTag.__table__, back_populates="books_private")
    user = relationship(argument="User", back_populates="books_private")

    def __str__(self) -> str:
        return self.title

    def generate_slug(self):
        self.slug = slugify(self.title)
        print(f"Generated slug: {self.slug}")


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint(sqltext="length(email) >= 5"),
    )

    id = Column(INT, primary_key=True)
    email = Column(VARCHAR(length=128), nullable=False, unique=True)
    password = Column(CHAR(length=60), nullable=False)

    books_private = relationship(argument=BookPrivate, back_populates="user")

    def __str__(self) -> str:
        return self.email


class GeneralBook(Base):
    __tablename__ = "general_books"

    id = Column(INT, primary_key=True)
    title = Column(VARCHAR(length=128), nullable=True)
    slug = Column(VARCHAR(length=128), nullable=False, unique=True)
    author = Column(VARCHAR(length=128), nullable=True)
    created_at = Column(TIMESTAMP, server_default="now()", nullable=False)
    is_published = Column(BOOLEAN, server_default="false", nullable=False)
    picture = Column(FileType(storage=FileSystemStorage(upload_to="media")), nullable=True, default='blank.png')
    category_id = Column(
        INT,
        ForeignKey(column=Category.id, ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False
    )

    books_private = relationship(argument=BookPrivate, back_populates="general_book")
    category = relationship(argument=Category, back_populates="general_books")
    tags_general = relationship(argument=Tag, secondary=GeneralBookTag.__table__, back_populates="general_books")

    def __str__(self) -> str:
        return self.title

    def generate_slug(self):
        self.slug = slugify(self.title)
        print(f"Generated slug: {self.slug}")
