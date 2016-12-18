import json
from django.core.management.base import BaseCommand

from channels import Channel, channel_layers


class Command(BaseCommand):

    help = 'Schedule a task to be performed'

    def handle(self, *args, **options):
        # Note the channel name is what is defined in
        # the routing.py file and I am explicitly getting
        # the "default" channel (defined in settings.py)
        c = Channel('websocket.receive',
                    channel_layer=channel_layers['default'])
        # I expect no data with this, but a dict is required
        c.send({
            "text": json.dumps({
                "action": "start_mytask",
                "job_name": "download",
            }),
            "reply_channel": "websocket.send!xxxxxxxxxxxx",
        })
