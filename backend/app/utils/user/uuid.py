import uuid
from uuid import NAMESPACE_DNS
from uuid import UUID


def generate_uuid(seed_key: str, namespace_uuid: UUID = NAMESPACE_DNS) -> UUID:
    """
    Generate a determiistic UUID based on a seed key.

    Args:
        seed_key (str): Seed key to generate the UUID
        namespace_uuid (UUID, optional): Namespace UUID. Defaults to NAMESPACE_DNS.

    Returns:
        UUID: A UUID that will the the same every time for the same seed key
    """
    return uuid.uuid5(namespace_uuid, seed_key)
