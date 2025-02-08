import os
from typing import Dict
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.databases.mssql import get_db_session
from app.models.agent import Agent
from app.models.user import User
from app.utils.api.helpers import get_logger
from app.utils.api.helpers import load_yaml
from app.utils.user.uuid import generate_uuid

logger = get_logger(__name__)


class DatabaseSeeder:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        # Store reference ids for relationships
        self._reference_ids: Dict[str, UUID] = {}
        self.seed_config_dir = os.getenv("SEED_CONFIG_DIR", "/app/data/seeds")

    def _get_reference_id(self, model_name: str, identifier: str) -> Optional[UUID]:
        """
        Get a UUID for a specific model name and identifier.

        Args:
            model_name (str): Model name (e.g. User, Agent)
            identifier (str): Unique identifier within that model

        Returns:
            Optional[UUID]: UUID of the model
        """
        seed_key = f"{model_name}:{identifier}"
        return generate_uuid(seed_key)

    def _get_or_create(self, model_class: BaseModel, identifier: str, **kwargs):
        """
        Get an existing record or create it if it doesn't exist.
        Returns a tuple of (instance, created) where created is a boolean indicating
        if a new instance was created.
        """
        record_id = self._get_reference_id(model_class.__name__, identifier)
        instance = self.db_session.query(model_class).filter(model_class.id == record_id).first()

        if instance:
            logger.info(f"{model_class.__name__} already exists: {instance}")
        else:
            instance = model_class(id=record_id, **kwargs)
            self.db_session.add(instance)
            logger.info(f"Created {model_class.__name__}: {instance}")

    def seed_factory(self, model_class: BaseModel, filename: str, identifier: str):
        """
        Seed data into the database for a specific model.
        Read from the filename and create a record in the database.
        """
        data = load_yaml(os.path.join(self.seed_config_dir, filename))
        data = data.get(filename.split(".")[0], [])
        logger.debug(f"Seeding {model_class.__name__} with {data}")

        for record_data in data:
            record_identifier = record_data.get(identifier)
            self._get_or_create(model_class, record_identifier, **record_data)

    def run(self):
        # If the file users.yaml exists, seed with that file
        if "users.yaml" in os.listdir(self.seed_config_dir):
            self.seed_factory(User, "users.yaml", "email")
        self.db_session.flush()

        # If the file agents.yaml exist, seed with that file
        if "agents.yaml" in os.listdir(self.seed_config_dir):
            self.seed_factory(Agent, "agents.yaml", "name")
        self.db_session.flush()

        self.db_session.commit()


def seed_db():
    """
    Seed the database with the initial data.
    Steps:
    1. Load the directory from env SEED_CONFIG_DIR
    2. Initialize the SeedConfiguration object
    3. Call the seed_factory function with the SeedConfiguration object
    """
    db_session = next(get_db_session())
    try:
        seeder = DatabaseSeeder(db_session)
        seeder.run()
    except Exception as e:
        logger.warning(f"Error seeding the database: {e}", exc_info=True)
        db_session.rollback()
    finally:
        db_session.close()
