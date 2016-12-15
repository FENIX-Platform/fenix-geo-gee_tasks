from django.shortcuts import render

from rest_framework import mixins, viewsets
from .models import Job
from .serializers import JobSerializer
# Create your views here.


class JobViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):

    """API endpoint that allows to view and create jobs"""
    queryset = Job.objects.all()
    serializer_class = JobSerializer
