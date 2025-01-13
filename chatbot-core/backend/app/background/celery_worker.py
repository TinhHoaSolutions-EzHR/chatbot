from celery import Celery

# Initialize Celery
app = Celery(
    "worker",
    broker="redis://cache:6379/0",
    backend="redis://cache:6379/1",
)

app.conf.task_track_started = True
app.conf.task_ignore_result = False

# Auto-discover tasks
app.autodiscover_tasks(["app.background.tasks.indexing"])
