import json
import logging
from channels import Channel
from channels.sessions import channel_session
from .models import Job as Job
from api.models import Job as JobApi
from .tasks import sec3, mytask
from gee_tasks.celery import app

log = logging.getLogger(__name__)


@channel_session
def ws_connect(message):
    message.reply_channel.send({
        "text": json.dumps({
            "action": "reply_channel",
            "reply_channel": message.reply_channel.name,
        })
    })


@channel_session
def ws_receive(message):
    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("ws message isn't json text=%s", message['text'])
        return

    if data:
        log.debug("ws message has reply_channel=%s", message['reply_channel'])
        reply_channel = message.reply_channel.name

        if data['action'] == "start_sec3":
            start_sec3(data, reply_channel)

        if data['action'] == "start_mytask":
            myinput = 'http://www.blog.pythonlibrary.org/wp-content/uploads/2012/06/wxDbViewer.zip'
            start_mytask(data, reply_channel, myinput)


def start_sec3(data, reply_channel):
    log.debug("job Name=%s", data['job_name'])
    # Save model to our database
    job = Job(
        name=data['job_name'],
        status="started",
    )
    job.save()

    # Start long running task here (using Celery)
    sec3_task = sec3.delay(job.id, reply_channel)

    # Store the celery task id into the database if we wanted to
    # do things like cancel the task in the future
    job.celery_id = sec3_task.id
    job.save()

    # Tell client task has been started
    Channel(reply_channel).send({
        "text": json.dumps({
            "action": "started",
            "job_id": job.id,
            "job_name": job.name,
            "job_status": job.status,
        })
    })


def start_mytask(data, reply_channel, input):
    log.debug("job Name=%s", data['job_name'])
    # Save model to our database
    job = JobApi(
        name=data['job_name'],
        status="started",
    )
    job.save()

    # Start long running task here (using Celery)
    mytask_task = mytask.delay(job.id, reply_channel, input)

    # Store the celery task id into the database if we wanted to
    # do things like cancel the task in the future
    job.celery_id = mytask_task.id
    job.save()

    # Tell client task has been started
    Channel(reply_channel).send({
        "text": json.dumps({
            "action": "started",
            "job_id": job.id,
            "job_name": job.name,
            "job_status": job.status,
            "download_file": input,
        })
    })
