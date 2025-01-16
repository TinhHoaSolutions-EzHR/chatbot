from app.settings import Constants
from app.settings import Secrets
from app.settings.constants import CeleryPriority

# Region Broker configurations
broker_url = f"{Constants.REDIS_SCHEME}://{Secrets.REDIS_HOST}:{Secrets.REDIS_PORT}/{Constants.REDIS_DB_NUMBER_CELERY}"
broker_connection_retry_on_startup = True
broker_pool_limit = Constants.CELERY_BROKER_POOL_LIMIT

# Redis Broker configurations
broker_transport_options = {
    "priority_steps": list(range(len(CeleryPriority))),
    "sep": Constants.CELERY_SEPARATOR,
    "queue_order_strategy": "priority",
    "retry_on_timeout": True,
    "health_check_interval": Constants.REDIS_HEALTH_CHECK_INTERVAL,
    "socket_keepalive": True,
    "socket_keepalive_options": Constants.REDIS_SOCKET_KEEPALIVE_OPTIONS,
}

# Redis Result Backend configurations
redis_socket_keepalive = True
redis_retry_on_timeout = True
redis_backend_health_check_interval = Constants.REDIS_HEALTH_CHECK_INTERVAL
task_default_priority = CeleryPriority.MEDIUM
task_acks_late = True
task_track_started = True
task_ignore_result = False

# Region Task Result Backend configurations
result_backend = f"{Constants.REDIS_SCHEME}://{Secrets.REDIS_HOST}:{Secrets.REDIS_PORT}/{Constants.REDIS_DB_NUMBER_CELERY_RESULT_BACKEND}"
result_expires = Constants.CELERY_RESULT_EXPIRES

# Celery worker configurations
worker_concurrency = 4
worker_pool = "threads"
worker_prefetch_multiplier = 1
