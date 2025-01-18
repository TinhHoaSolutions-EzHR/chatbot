from app.settings import Constants
from app.settings import Secrets
from app.settings.constants import CeleryPriority

## Region Broker configurations

# Message transport system that Celery uses to communicate between workers and tasks.
broker_url = f"{Constants.REDIS_SCHEME}://{Secrets.REDIS_HOST}:{Secrets.REDIS_PORT}/{Constants.REDIS_DB_NUMBER_CELERY}"

# Set to True to ensure Celery retries connecting to the broker if the initial attempt fails during startup.
broker_connection_retry_on_startup = True

# Defines the maximum number of connections that Celery can open to the broker.
broker_pool_limit = Constants.CELERY_BROKER_POOL_LIMIT

## Redis Broker configurations

broker_transport_options = {
    # Each priority level defines the order in which tasks should be processed.
    "priority_steps": list(range(len(CeleryPriority))),
    # Specifies the separator used in Redis keys for queues.
    "sep": Constants.CELERY_SEPARATOR,
    # Queues are processed based on task priority.
    "queue_order_strategy": "priority",
    # Set to True so Celery retries broker operations if a timeout occurs.
    "retry_on_timeout": True,
    # Specifies the interval (in seconds) for health checks to ensure Redis connections are alive.
    "health_check_interval": Constants.REDIS_HEALTH_CHECK_INTERVAL,
    # Enable and configure TCP keep-alive to maintain persistent connections to Redis.
    "socket_keepalive": True,
}

## Redis Result Backend configurations

# Enables TCP keep-alive for Redis connections.
redis_socket_keepalive = True

# Set to True so Celery retries operations if a timeout occurs.
redis_retry_on_timeout = True

# Sets the interval (in seconds) for performing health checks on the Redis result backend.
redis_backend_health_check_interval = Constants.REDIS_HEALTH_CHECK_INTERVAL

# Defines the default priority for tasks.
task_default_priority = CeleryPriority.MEDIUM

# When True, the task acknowledgment is sent only after the task is fully processed.
task_acks_late = True

# When True, Celery tracks the state when a task starts.
task_track_started = True

# When False, Celery stores task results in the backend.
task_ignore_result = False

## Region Task Result Backend configurations

# Defines the URL for the result backend
result_backend = f"{Constants.REDIS_SCHEME}://{Secrets.REDIS_HOST}:{Secrets.REDIS_PORT}/{Constants.REDIS_DB_NUMBER_CELERY_RESULT_BACKEND}"

# Specifies the expiration time (in seconds) for task results
result_expires = Constants.CELERY_RESULT_EXPIRES

## Celery worker configurations

# Defines the number of concurrent worker threads/processes.
worker_concurrency = Constants.CELERY_WORKER_CONCURRENCY

# Specifies the type of pool to use for concurrency. "threads" indicates a thread-based concurrency model.
worker_pool = Constants.CELERY_WORKER_POOL

# Defines how many tasks a worker prefetches at a time.
worker_prefetch_multiplier = Constants.CELERY_WORKER_PREFETCH_MULTIPLIER
