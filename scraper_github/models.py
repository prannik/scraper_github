from sqlalchemy import INTEGER, TEXT, Column, String, create_engine
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import URLType

from scraper_github import settings

DeclarativeBase = declarative_base()


def db_connect() -> Engine:
    return create_engine(URL(**settings.DATABASE))


def create_items_table(engine: Engine):
    DeclarativeBase.metadata.create_all(engine)


class RepItems(DeclarativeBase):
    __tablename__ = "github_repository"

    author = Column('author', String, )
    title = Column('title', String, primary_key=True)
    about = Column('about', TEXT)
    url = Column('url', URLType)
    stars = Column('stars', INTEGER)
    forks = Column('forks', INTEGER)
    watching = Column('watching', INTEGER)
    commits = Column('commits', INTEGER)
    last_commits = Column('last_commits', JSONB)
    releases = Column('releases', INTEGER)
    last_releases = Column('last_releases', JSONB)
