from django.db import models
from model_utils import Choices
from datetime import datetime
from django.utils import timezone
import requests
import funcy
from huey.contrib.djhuey import db_task


RETRY_ERRORS = [
    requests.exceptions.ReadTimeout,
    requests.exceptions.Timeout,
    requests.exceptions.ConnectionError
]


class Job(models.Model):

    STATUS = Choices(
        ('Q', 'QUEUED', 'QUEUED'),
        ('C', 'COMPLETE', 'COMPLETE'),
        ('P', 'PROCESSING', 'PROCESSING'),
        ('F', 'FAILED', 'FAILED')
    )

    id = models.BigAutoField(primary_key=True)
    url = models.URLField(db_index=True)
    result = models.TextField(null=True)
    status = models.CharField(max_length=1, choices=STATUS)
    time_created = models.DateTimeField()
    time_updated = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        now = datetime.now(tz=timezone.utc)
        if not self.pk:
            self.time_created = now if self.time_created is None else self.time_created
        self.time_updated = now if self.time_updated is None else self.time_updated
        super(Job, self).save(*args, **kwargs)


@db_task()
def process_job(job_id):
    job = Job.objects.get(id=job_id)
    job.status = Job.STATUS.PROCESSING
    job.save()
    output = get_request(job.url)
    if output is None:
        job.status = Job.STATUS.FAILED
    else:
        job.result = output
        job.status = Job.STATUS.COMPLETE
    job.save()


@funcy.retry(5, errors=RETRY_ERRORS, timeout=lambda a: (a * 0.2) ** 2)
def get_request(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.content
