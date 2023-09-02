from django.shortcuts import render
from django.http import HttpResponse

from .performance_service import PerformanceService
from .models import \
        Performance as PerformanceModel,\
        Character

service = PerformanceService()

def index(request):
    return render(request, "perform/index.html", {
        "performances": PerformanceModel.objects.all()
    })

def performance(request, performance_id):
    return render(request, "perform/performance.html", {
        "performance": PerformanceModel.objects.get(id=performance_id)
    })

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
        POST = request.POST

        # For each character, create a BotPerformer
        character_names = POST.getlist("character_names[]")
        character_descs = POST.getlist("character_descriptions[]")

        # Create Character database entries
        characters: list[Character] = []
        for name, desc in zip(character_names, character_descs):
            character_model = Character(
                name=name,
                description=desc,
            )
            character_model.save()
            characters.append(character_model)

        # Add Performance to database
        performance_model = PerformanceModel(
            title=POST.get("performance_title"),

            #@REVISIT really we'd probably like to run this through
            #@ bot_aukerman.performance as we do in the service
            script=POST.get("context_script"),
        )
        performance_model.save()

        # Add Characters to Performance
        performance_model.characters.set(characters)
        performance_model.save()

        return HttpResponse(performance_model.id)

def start_performance(request, performance_id):
    print("Starting performance")

    performance_model = PerformanceModel.objects.get(id=performance_id)

    service.start(performance_model)

    return render(request, "perform/_performance_status.html", {
        "script": performance_model.script,
        # "characters": performance_model.characters.all(),
    })

def stop_performance(request, performance_id):
    print("Stopping performance")

    service.stop()

    return HttpResponse()

#@REVISIT rename to something like request_dialogue ?
def generate_dialogue(request, performance_id):
    print("Generating dialogue")

    service.generate_dialogue()

    return HttpResponse()

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
