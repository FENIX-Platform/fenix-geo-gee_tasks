from __future__ import absolute_import
import time
import json
import logging
import requests

from gee_tasks.celery import app
from .models import Job as Job
from api.models import Job as JobApi
from channels import Channel
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from jobs.management.commands import schedule_download


log = logging.getLogger(__name__)


@app.task
def sec3(job_id, reply_channel):
    # time sleep represent some long running process
    time.sleep(3)
    # Change task status to completed
    job = Job.objects.get(pk=job_id)
    log.debug("Running job_name=%s", job.name)

    job.status = "completed"
    job.save()

    # Send status update back to browser client
    if reply_channel is not None:
        Channel(reply_channel).send({
            "text": json.dumps({
                "action": "completed",
                "job_id": job.id,
                "job_name": job.name,
                "job_status": job.status,
            })
        })


@app.task
def mytask(job_id, reply_channel, input):
    log.info("Start task")
    # i.e. time to wait for gee processing
    time.sleep(10)
    print "downloading with requests"
    # url = input
    url = 'http://www.blog.pythonlibrary.org/wp-content/uploads/2012/06/wxDbViewer.zip'
    r = requests.get(url)
    with open("code3.zip", "wb") as code:
        code.write(r.content)
        result = code.fileno()
        log.info("Task finished: result = %i" % result)

    # Change task status to completed
    job = JobApi.objects.get(pk=job_id)
    log.debug("Running job_name=%s", job.name)

    job.status = "finished"
    job.save()

    # Send status update back to browser client
    if reply_channel is not None:
        Channel(reply_channel).send({
            "text": json.dumps({
                "action": "completed",
                "job_id": job.id,
                "job_name": job.name,
                "job_status": job.status,
                "download_file": input,
            })
        })


@app.task
def hello():
    return "Hello GEE"


# Define the task to be run in the celerybeat
@app.task
def download():
    cmd = schedule_download.Command()
    options = {}
    cmd.handle(**options)


TASK_MAPPING = {
    'hello': hello,
    'mytask': mytask
}
