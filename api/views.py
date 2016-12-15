from django.shortcuts import render

from rest_framework import mixins, viewsets
from .models import Job
from .serializers import JobSerializer
# Create your views here.


class JobViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):

    """
    retrieve:
        Return a job instance.

    list:
        Return all jobs, ordered by most recently created.

    create:
        Create a new job.

    delete:
        Remove an existing job.

    partial_update:
        Update one or more fields on an existing job.

    update:
        Update a job.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer
