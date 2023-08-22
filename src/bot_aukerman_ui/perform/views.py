from django.shortcuts import render
from django.http import HttpResponse

from bot_aukerman import Performance, BotPerformer, HumanPerformer
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

    # Create a Performance
    model_config = {
        "model": "gpt2-large"
        # "model": "gpt2"
        # "model": "gpt4all-7B-unfiltered", "engine": "llamacpp"
        # "model": "text-ada-001", "engine": "openai",
        # "engine": "openai",
    }

    # For each character, create a BotPerformer
    character_names = request.POST.getlist("character_names[]")
    character_descs = request.POST.getlist("character_descriptions[]")

    performance = Performance(model_config = model_config,
                              resume_from_log = False)

    for character_name, character_desc in zip(character_names, character_descs):
        character = BotPerformer(
            character_name=character_name,
            character_desc=character_desc,
        )

        print(f"Adding character {character_name} with description {character_desc}")

        performance.add_performer(character)

    # Add a scene description
    scene_desc = request.POST.get("scene_description")
    print(f"Adding scene description {scene_desc}")
    performance.add_description(scene_desc)

    # Add any initial dialogue
    context = request.POST.get("context")
    print(f"Adding context {context}")
    performance.add_dialogue(context)

    # Add a human performer
    human = HumanPerformer(character_name="Cammy")
    performance.add_performer(human)

    # Start the performance
    print("Starting performance")

    service.start(performance)

    return HttpResponse('<div id="performance">Started...</div>')
