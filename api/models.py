from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.


class Job(models.Model):
    """Class describing a job"""

    # The currently available types of a job are:
    TYPES = (
        ('hello', 'hello'),
        ('mytask', 'mytask'),
    )

    # The list of states that a job can assume
    STATUSES = (
        ('pending', 'pending'),
        ('started', 'started'),
        ('finished', 'finished'),
        ('failed', 'failed'),
    )

    type = models.CharField(choices=TYPES, max_length=20)
    status = models.CharField(choices=STATUSES, max_length=20)

    created_at = models.DateTimeField(default=timezone.now, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    argument = models.PositiveIntegerField()
    result = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        """Save the model and schedule the job if it is in pending state"""

        super(Job, self).save(*args, **kwargs)
        if self.status == 'pending':
            from jobs.tasks import JOB_MAPPING
            job = JOB_MAPPING[self.type]
            job.delay(job_id=self.id, n=self.argument)
