from django.shortcuts import render, get_object_or_404

# Create your views here.


from .models import Job


def dashboard(request):
    return render(request, 'jobs/index.html')
