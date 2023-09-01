from django.shortcuts import render
from django.http import HttpResponse

from .performance_service import PerformanceService

service = PerformanceService()

def index(request):
    return render(request, "perform/index.html")

def add_character(request):
    return render(request, "perform/_add_character.html")

def delete_character(request, character_id):
    # Return empty 200
    return HttpResponse()

def start_performance(request):
    print("Starting performance")

    #@REVISIT is passing request.POST a good idea?
    service.start(request.POST)

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
