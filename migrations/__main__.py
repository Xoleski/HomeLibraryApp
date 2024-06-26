from alembic.config import Config
from alembic.command import check, upgrade, revision
from alembic.util import AutogenerateDiffsDetected

config = Config("alembic.ini")

if __name__ == '__main__':
    upgrade(config=config, revision="head")
    try:
        check(config=config)
    except AutogenerateDiffsDetected:
        revision(config=config, autogenerate=True)
        upgrade(config=config, revision="head")




