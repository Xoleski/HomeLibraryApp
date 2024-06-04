from datetime import datetime

from sqlalchemy import (
    Column,
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
    CHAR
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import INTERVAL
from sqlalchemy.sql.functions import now

from src.database.base import Base
from src.database.types import FileType
from src.database.storage import FileSystemStorage
from src.utils.slugify import slugify

__all__ = [
    "Base",
    "BookPrivate",
    "BookPrivateTag",
    "Category",
    "GeneralBook",
    "GeneralBookTag",
    "User",
    "Tag",
]


class BookPrivateTag(Base):
    __tablename__ = "book_private_tags"

    tag_id = Column(
        ForeignKey(
            column="tags.id", ondelete="CASCADE", onupdate="CASCADE"
        ),
        nullable=False,
        primary_key=True
    )
    book_private_id = Column(
        ForeignKey(
            column="books_private.id", ondelete="CASCADE", onupdate="CASCADE"
        ),
        nullable=False,
        primary_key=True
    )


class GeneralBookTag(Base):
    __tablename__ = "general_books_tags"

    tag_id = Column(
        ForeignKey(
            column="tags.id", ondelete="CASCADE", onupdate="CASCADE"
        ),
        nullable=False,
        primary_key=True
    )
    general_book_id = Column(
        ForeignKey(
            column="general_books.id", ondelete="CASCADE", onupdate="CASCADE"
        ),
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


@event.listens_for(Category, 'before_insert')
def before_insert_listener(mapper, connection, target: Category):
    # target.to_lowercase()
    if not target.slug:
        target.slug = slugify(value=target.name)
        print(f"Generated slug: {target.slug}")


class Tag(Base):
    __tablename__ = "tags"
    __table_args__ = (
        CheckConstraint(sqltext="length(name) >= 2"),
    )

    id = Column(INT, primary_key=True)
    name = Column(VARCHAR(length=32), nullable=False, unique=True)

    general_books = relationship(
        argument="GeneralBook",
        secondary=GeneralBookTag.__table__,
        back_populates="tags_general"
    )
    books_private = relationship(
        argument="BookPrivate",
        secondary=BookPrivateTag.__table__,
        back_populates="tags_private"
    )

    def __str__(self) -> str:
        return self.name


class BookPrivate(Base):
    __tablename__ = "books_private"
    __table_args__ = (
        CheckConstraint(sqltext="length(title) >= 2"),
        CheckConstraint(sqltext="length(author) >= 2"),
    )

    id = Column(INT, primary_key=True)
    title = Column(VARCHAR(length=128), nullable=False)
    slug = Column(VARCHAR(length=128), nullable=False, unique=True)
    author = Column(VARCHAR(length=128), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now, server_default="now", nullable=False)
    is_published = Column(BOOLEAN, default=False, server_default="false", nullable=False)
    picture = Column(FileType(
        storage=FileSystemStorage(upload_to="media")),
        nullable=True,
        default='blank.png'
    )
    category_id = Column(
        INT,
        ForeignKey(column=Category.id, ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False
    )
    general_book_id = Column(
        INT,
        ForeignKey(column="general_books.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False
    )
    user_id = Column(
        INT,
        ForeignKey(column="users.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=True
    )

    general_book = relationship(argument="GeneralBook", back_populates="books_private")
    category = relationship(argument=Category, back_populates="books_private")
    tags_private = relationship(argument=Tag, secondary=BookPrivateTag.__table__, back_populates="books_private")
    user = relationship(argument="User", back_populates="books_private")

    def __str__(self) -> str:
        return self.title

    @property
    def user_email_(self) -> str:
        if self.user:
            return self.user.email


@event.listens_for(BookPrivate, 'before_insert')
def before_insert_listener(mapper, connection, target: BookPrivate):
    if not target.slug:
        target.slug = slugify(value=target.title)
        print(f"Generated slug: {target.slug}")


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
    __table_args__ = (
        CheckConstraint(sqltext="length(title) >= 2"),
        CheckConstraint(sqltext="length(author) >= 2"),
    )

    id = Column(INT, primary_key=True)
    title = Column(VARCHAR(length=128), nullable=False)
    slug = Column(VARCHAR(length=128), nullable=False, unique=True)
    author = Column(VARCHAR(length=128), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now, server_default="now", nullable=False)
    is_published = Column(BOOLEAN, default=False, server_default="false", nullable=False)
    picture = Column(FileType(
        storage=FileSystemStorage(upload_to="media")),
        nullable=True,
        default='blank.png'
    )
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


@event.listens_for(GeneralBook, 'before_insert')
def before_insert_listener(mapper, connection, target: GeneralBook):
    if not target.slug:
        target.slug = slugify(value=target.title)
        print(f"Generated slug: {target.slug}")
