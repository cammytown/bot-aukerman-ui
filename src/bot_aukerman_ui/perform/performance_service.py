import time
from typing import Optional
from bot_aukerman import Performance, BotPerformer, HumanPerformer
from .models import Performance as PerformanceModel, Character
from .service import Service

class PerformanceService(Service):
    performance: Optional[Performance]

    def __init__(self):
        super().__init__('PerformanceService')
        self.performance = None

    #@REVISIT naming
    def start_new(self, POST):
        # Create a Performance
        model_config = {
            "model": "gpt2-large"
            # "model": "gpt2"
            # "model": "gpt4all-7B-unfiltered", "engine": "llamacpp"
            # "model": "text-ada-001", "engine": "openai",
            # "engine": "openai",
        }

        # For each character, create a BotPerformer
        character_names = POST.getlist("character_names[]")
        character_descs = POST.getlist("character_descriptions[]")

        performance = Performance(model_config = model_config,
                                  resume_from_log = False)

        for char_name, char_desc in zip(character_names, character_descs):
            character = BotPerformer(
                character_name=char_name,
                character_desc=char_desc,
            )

            print(f"Adding character {char_name} with description {char_desc}")

            performance.add_performer(character)

        # Add a scene description
        scene_desc = POST.get("scene_description")
        print(f"Adding scene description {scene_desc}")
        performance.add_description(scene_desc)

        # Add any initial dialogue
        context = POST.get("context")
        print(f"Adding context {context}")
        performance.add_dialogue(context)

        # Add a human performer
        human = HumanPerformer(character_name="Cammy")
        performance.add_performer(human)


        if self.running == True:
            raise Exception("PerformanceService is already running")

        assert performance is not None

        self.performance = performance

        # Create Character database entries
        characters: list[Character] = []
        for performer in performance.performers.values():
            character_model = Character(
                name=performer.character_name,
                description=performer.character_desc,
            )
            character_model.save()
            characters.append(character_model)

        # Add Performance to database
        performance_model = PerformanceModel(
            script=performance.get_script(),
        )
        performance_model.save()

        # Add Characters to Performance
        performance_model.characters.set(characters)
        performance_model.save()

        super().start_new()

    def run(self):
        assert self.performance is not None

        # Get Performance database entry
        #@REVISIT this seems ugly; store model as property of this class?
        performance_model = PerformanceModel.objects.last()

        self.performance.start_audio()

        while self.running:
            components = self.performance.update_audio()

            if components:
                new_dialogue = ""

                # Convert components to string
                #@REVISIT should we just run performance.get_script() again?
                for component in components:
                    new_dialogue += component.to_str()
                    new_dialogue += "\n\n"

                # Add Dialogue to database
                performance_model.script += new_dialogue
                performance_model.save()

                # Add Dialogue to database
                # performance_model = PerformanceModel.objects.last()
                # performance_model.script += components["dialogue"]
                # performance_model.save()

            # Sleep briefly
            time.sleep(0.1)


    def get_status(self):
        # Get Performance database entry
        performance_model = PerformanceModel.objects.last()

        return {
            "script": performance_model.script,
            "characters": performance_model.characters,
        }
