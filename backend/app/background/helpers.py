import time
from contextlib import contextmanager

from pydantic import BaseModel
from pydantic import Field


class ProbeConfig(BaseModel):
    """
    Configuration for the readiness probe.
    """

    wait_interval: int = Field(5, ge=1, description="The interval to wait before retrying.")
    wait_limit: int = Field(60, ge=1, description="The maximum time to wait before giving up.")


@contextmanager
def timeout_context():
    """
    Context manager to handle timeouts when waiting for a resource to be available.
    """
    start_time = time.monotonic()
    yield lambda: time.monotonic() - start_time
