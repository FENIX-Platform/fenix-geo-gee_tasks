=================
What is GEE tasks
=================

GEE tasks is a workflow manager for executing tasks and processing
in Google Earth Engine and then getting back the result locally.
It is a simple Django app that is using Channels for scheduling jobs
asyncronously into a Celery application and monitoring their status
through a web API.
The status of each job can be monitored through the websocket channel
in a dashboard page.

Quick start
-----------

1. Add "gee_tasks" to your INSTALLED_APPS setting like this::

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'gee_tasks',
        'jobs',
        'api',
        #etc
    )
    
2. In your settings.py or local_settings.py file, add a CELERYBEAT_SCHEDULE
   setting to specify when Celery should run jobs tasks::

.. code-block:: python

    from celery.schedules import crontab
    CELERYBEAT_SCHEDULE = {
        'mytask-every-1minute': {
            'task': 'jobs.tasks.download',
            'schedule': crontab(minute='*/1'),
        },
    }

3. In your settings or local_settings file, add the configuration of Channels for
   using a REDIS back-end:

.. code-block:: python

    # Channels settings
	CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "asgi_redis.RedisChannelLayer",  # use redis backend
            "CONFIG": {
                "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],  # set redis address
            },
            "ROUTING": "gee_tasks.routing.channel_routing",  # load routing from our routing.py file
        },
    }

How to run/debug
----------------

Start the Celery process with DEBUG logging:

.. code-block:: console

    celery worker -A gee_tasks -l debug -B

Start the Django application as usual in your virtual environment:

.. code-block:: console

    python manage.py runserver

Access the Dashboard and API
----------------------------

Dashboard - `Dashboard`_ 

.. _Dashboard: http://localhost:8000/dashboard/

API page:

`DjangoRestFramework`_ 

.. _DjangoRestFramework: http://localhost:8000/api/

`Swagger`_ 

.. _Swagger: http://localhost:8000/api/docs/