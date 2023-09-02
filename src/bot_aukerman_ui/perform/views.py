from django.shortcuts import render
from django.http import HttpResponse

from .performance_service import PerformanceService
from .models import Performance as PerformanceModel

service = PerformanceService()

def index(request):
    return render(request, "perform/index.html", {
        "performances": PerformanceModel.objects.all()
    })

def performance(request, performance_id):
    return render(request, "perform/performance.html")

def add_character(request):
    return render(request, "perform/_add_character.html")

def delete_character(request, character_id):
    # Return empty 200
    return HttpResponse()

def create_performance(request):
    # If GET request
    if request.method == "GET":
        return render(request, "perform/new_performance.html")
    elif request.method == "POST":
        #@REVISIT is passing request.POST a good idea?
        service.start_new(request.POST)
        return get_performance_status(request)

def get_performance_status(request):
    print("Getting performance status")

    status = service.get_status()

    return render(request, "perform/_performance_status.html", {
        "script": status["script"],
        "characters": status["characters"],
    })

def toggle_microphone(self):
    print("Toggling microphone")

    assert(service.performance is not None)

    # Toggle microphone
    service.performance.toggle_microphone_listen()

    #@REVISIT
    return HttpResponse("On" if service.performance.is_listening else "Off")
