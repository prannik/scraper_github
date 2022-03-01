from sqlalchemy.orm import sessionmaker

from .models import RepItems, create_items_table, db_connect


class ScraperGithubPipeline:
    def __init__(self):
        engine = db_connect()
        create_items_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        instance = session.query(RepItems).filter_by(**item).one_or_none()
        if instance:
            return instance
        rep = RepItems(**item)

        try:
            session.add(rep)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
