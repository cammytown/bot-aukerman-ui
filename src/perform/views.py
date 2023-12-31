import os
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .performance_service import PerformanceService
from .models import \
        Performance as PerformanceModel,\
        Character,\
        Scene

service = PerformanceService()

def index(request):
    return render(request, "perform/index.html", {
        "page": "index",
        "performances": PerformanceModel.objects.all()
    })

def settings(request):
    # Check if OpenAI API key env var is set
    openai_api_key = os.environ.get("OPENAI_API_KEY")

    return render(request, "perform/settings.html", {
        "page": "settings",
        "openai_api_key": openai_api_key,
    })

def performance(request, performance_id):
    return render(request, "perform/performance.html", {
        "page": "performance",
        "performance": PerformanceModel.objects.get(id=performance_id),
        "service": service, #@REVISIT
    })

def add_character(request):
    return render(request, "perform/_add_character.html")

def delete_character(request, character_id):
    # Return empty 200
    return HttpResponse()

def create_performance(request):
    # If GET request
    if request.method == "GET":
        return render(request, "perform/create_performance.html", {
            "page": "create_performance",
        })


    elif request.method == "POST":
        POST = request.POST

        scene_desc = POST.get("scene_description")

        # For each character, create a BotPerformer
        character_names = POST.getlist("character_names[]")
        character_descs = POST.getlist("character_descriptions[]")
        character_models = POST.getlist("character_performer_types[]")

        # Create Character database entries
        characters: list[Character] = []
        for name, desc, model in zip(character_names,
                                     character_descs,
                                     character_models):
            character_model = Character(
                name=name,
                description=desc,
                performer=model,
            )
            character_model.save()
            characters.append(character_model)

        # Create Scene database entry
        scene = Scene(description=scene_desc)
        scene.save()

        # Add Performance to database
        performance_model = PerformanceModel(
            title=POST.get("performance_title"),

            #@REVISIT really we'd probably like to run this through
            #@ bot_aukerman.performance as we do in the service
            script=POST.get("context_script"),
        )

        # Save (give Performance an id)
        performance_model.save()

        # Add Scene to Performance
        performance_model.scenes.add(scene)

        # Add Characters to Performance
        performance_model.characters.set(characters)

        performance_model.save()

        return redirect("performance", performance_id=performance_model.id)

def delete_performance(request, performance_id):
    print("Deleting performance")

    performance_model = PerformanceModel.objects.get(id=performance_id)
    performance_model.soft_delete()

    return HttpResponse("Deleted performance")

def start_performance(request, performance_id):
    print("Starting performance")

    performance_model = PerformanceModel.objects.get(id=performance_id)

    service.start(performance_model)

    return render(request, "perform/_performance_controls.html", {
        "performance": performance_model,
        "service": service, #@REVISIT
    })

def stop_performance(request, performance_id):
    print("Stopping performance")

    service.stop()

    return render(request, "perform/_performance_controls.html", {
        #@REVISIT hack
        "performance": PerformanceModel.objects.get(id=performance_id),
        "service": service, #@REVISIT
    })

#@REVISIT architecture
def get_script(request, performance_id):
    return render(request, "perform/_performance_script.html", {
        #@REVISIT hack (service might update it)
        "performance": PerformanceModel.objects.get(id=performance_id),
    })

def edit_script(request, performance_id):
    print("Editing script")

    if(request.method == "POST"):
        script_text = request.POST.get("script_text")

        # If service is not running
        if not service.running:
            # Update database
            performance_model = PerformanceModel.objects.get(id=performance_id)
            performance_model.script = script_text
            performance_model.save()

        # If service is running
        else:
            # Update script in service
            script = service.load_script_string(script_text)

    return get_script(request, performance_id)

#@REVISIT rename to something like request_dialogue ?
def generate_dialogue(request, performance_id):
    print("Generating dialogue")

    bot_dialogue = service.generate_dialogue()

    return get_script(request, performance_id)

def interrupt(request, performance_id):
    print("Interrupting")

    service.interrupt()

    return render(request, "perform/_performance_controls.html", {
        #@REVISIT hack
        "performance": PerformanceModel.objects.get(id=performance_id),
        "service": service, #@REVISIT
    })

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
