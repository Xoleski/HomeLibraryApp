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
                        ForeignKeyConstraint, TIMESTAMP, CHAR)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import INTERVAL
from sqlalchemy.sql.functions import now

from .base import Base
from .types import FileType
from .storage import FileSystemStorage

__all__ = (
    "Base",
    "Article",
    "ArticleTag",
    "Category",
    "User",
    "Tag",
    "GeneralBook",
    "GeneralBookTag",
)


class ArticleTag(Base):
    __tablename__ = "article_tags"

    tag_id = Column(ForeignKey(
        "tags.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        primary_key=True
    )
    article_id = Column(ForeignKey(
        "articles.id", ondelete="RESTRICT", onupdate="CASCADE"),
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
    slug = Column(VARCHAR(length=128), nullable=False, unique=True)

    articles = relationship(argument="Article", back_populates="category")
    general_books = relationship(argument="GeneralBook", back_populates="category")

    def __str__(self) -> str:
        return self.name


class Tag(Base):
    __tablename__ = "tags"

    id = Column(INT, primary_key=True)
    name = Column(VARCHAR(length=32), nullable=False, unique=True)

    general_books = relationship(argument="GeneralBook", secondary=GeneralBookTag.__table__, back_populates="tags")
    articles = relationship(argument="Article", secondary=ArticleTag.__table__, back_populates="tags")

    def __str__(self) -> str:
        return self.name


class Article(Base):
    __tablename__ = "articles"

    id = Column(INT, primary_key=True)
    title = Column(VARCHAR(length=128), nullable=False)
    slug = Column(VARCHAR(length=128), nullable=False, unique=True)
    body = Column(VARCHAR, nullable=False)
    created_at = Column(TIMESTAMP, server_default="now", nullable=False)
    is_published = Column(BOOLEAN, server_default="false", nullable=False)
    picture = Column(FileType(storage=FileSystemStorage(upload_to="media")), nullable=True)
    category_id = Column(
        INT,
        ForeignKey(column=Category.id, ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False
    )

    category = relationship(argument=Category, back_populates="articles")
    tags = relationship(argument=Tag, secondary=ArticleTag.__table__, back_populates="articles")

    def __str__(self) -> str:
        return self.title



class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint(sqltext="length(email) >= 5"),
    )

    id = Column(INT, primary_key=True)
    email = Column(VARCHAR(length=128), nullable=False, unique=True)
    password = Column(CHAR(length=60), nullable=False)

    def __str__(self) -> str:
        return self.email


class GeneralBook(Base):
    __tablename__ = "general_books"

    id = Column(INT, primary_key=True)
    title = Column(VARCHAR(length=128), nullable=False)
    slug = Column(VARCHAR(length=128), nullable=False, unique=True)
    body = Column(VARCHAR, nullable=False)
    created_at = Column(TIMESTAMP, server_default="now", nullable=False)
    is_published = Column(BOOLEAN, server_default="false", nullable=False)
    picture = Column(FileType(storage=FileSystemStorage(upload_to="media")), nullable=True)
    category_id = Column(
        INT,
        ForeignKey(column=Category.id, ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False
    )

    category = relationship(argument=Category, back_populates="general_books")
    tags = relationship(argument=Tag, secondary=GeneralBookTag.__table__, back_populates="general_books")

    def __str__(self) -> str:
        return self.title

