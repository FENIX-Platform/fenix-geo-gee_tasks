from __future__ import absolute_import
import time
import json
import logging
import requests

from gee_tasks.celery import app
from .models import Job
from channels import Channel
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger


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


# A periodic task that will run every minute (the symbol "*" means every)
# @periodic_task(
#     run_every=(crontab(minute='*/1')),
#     name="mytask",
#     ignore_result=True
# )
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
                "download_file": input,
            })
        })


def hello():
    return "Hello GEE"


TASK_MAPPING = {
    'hello': hello,
    'mytask': mytask
}
