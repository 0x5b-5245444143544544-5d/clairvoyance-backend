import logging

import dataset
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import config

log = logging.getLogger(__name__)

class Database:
    def __init__(self) -> None:
        self.host = config.db_host
        self.database = config.db_name
        self.user = config.db_user
        self.password = config.db_pass

        if not all([self.host, self.database, self.user, self.password]):
            log.error("One or more database connection variables are missing, exiting...")
            raise SystemExit

        self.url = f"mysql://{self.user}:{self.password}@{self.host}/{self.database}"
        self.setup()

    def get(self) -> dataset.Database:
        """
        Returns the dataset database object.
        """
        return dataset.connect(url=self.url)

    def setup(self) -> None:
        """
        Sets up the tables.
        """
        engine = create_engine(self.url)
        if not database_exists(engine.url):
            create_database(engine.url)

        db = self.get()

        if "temperature" not in db:
            temperature = db.create_table("temperature")
            temperature.create_column("timestamp", db.types.integer)
            temperature.create_column("temperature", db.types.float)

        db.commit()
        db.close()
