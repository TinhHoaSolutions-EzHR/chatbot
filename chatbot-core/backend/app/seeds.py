import os
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel

from app.databases.mssql import get_db_session
from app.models.agent import AgentRequest
from app.services.agent import AgentService
from app.utils.api.helpers import get_logger
from app.utils.api.helpers import load_yaml

logger = get_logger(__name__)


class SeedConfiguration(BaseModel):
    """
    Base class for seed configuration
    """

    agents: Optional[List[AgentRequest]] = None
    # users: Optional[List[User]] = None


def seed_factory(seed_config: SeedConfiguration, functions: Dict[str, callable]):
    """
    Seed the database with the initial data.
    Loop through the seed configuration and call the create functions.

    Args:
        seed_config (SeedConfiguration): Seed configuration
    """
    logger.info("Seeding the database with initial data")

    for field_name, _ in seed_config.model_fields.items():
        values = getattr(seed_config, field_name)

        if not values:
            continue

        if len(values) == 0:
            continue

        for value in values:
            # Call to the create function in the service layer
            # The create function should insert new records into the database
            # And return the error if any
            err = functions[field_name](value)  # BUG: missing user_id
            if err:
                logger.warning(f"Cannot seed {field_name} with value {value}")


def seed_db():
    """
    Seed the database with the initial data.
    Steps:
    1. Load the directory from env SEED_CONFIG_DIR
    2. Initialize the SeedConfiguration object
    3. Call the seed_factory function with the SeedConfiguration object
    """
    # The seedings dictionary is used to map the entity name to the seeding function
    # Usually is the create function in the repository layer
    db_session = next(get_db_session())
    functions = {
        "agents": AgentService(db_session=db_session).create_agent,
        # "users": UserRepository.create_user,
    }

    seed_config_dir = os.getenv("SEED_CONFIG_DIR")
    if not seed_config_dir:
        logger.warning("Environment SEED_CONFIG_DIR is not set, ignore seeding process")
        return

    # Read all files in the seed config directory, and load the seed config
    logger.info(f"Reading seed config from {seed_config_dir}")
    for file_name in os.listdir(seed_config_dir):
        if file_name.endswith(".yaml"):
            logger.info(f"Loading seed data from {file_name}")
            objects = load_yaml(os.path.join(seed_config_dir, file_name))
            config_partial = SeedConfiguration.model_validate(objects)
            seed_factory(config_partial, functions)

    db_session.close()
