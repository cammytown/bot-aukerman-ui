import time
from typing import Optional
from bot_aukerman import Performance,\
        BotPerformer,\
        HumanPerformer

from .models import Performance as PerformanceModel
from .service import Service

class PerformanceService(Service):
    performance: Optional[Performance]
    performance_model: Optional[PerformanceModel]

    def __init__(self):
        super().__init__('PerformanceService')
        self.performance = None

    def start(self, performance_model: PerformanceModel):
        if self.running == True:
            return

        #@REVISIT weird architecture
        self.performance_model = performance_model

        # Create a Performance
        model_config = {
            "model": "gpt2-large",
            "use_cuda": True, #@REVISIT!
            "max_context_length": 200, #@REVISIT!

            # "model": "gpt2"
            # "model": "gpt4all-7B-unfiltered", "engine": "llamacpp"
            # "model": "text-ada-001", "engine": "openai",
            # "engine": "openai",
        }

        performance = Performance(model_config = model_config,
                                  resume_from_log = False)

        # Add characters
        for character in self.performance_model.characters.all():
            character = BotPerformer(
                character_name=character.name,
                character_desc=character.description,
            )

            performance.add_performer(character)

        # # Add a scene description
        # scene_desc = POST.get("scene_description")
        # print(f"Adding scene description {scene_desc}")
        # performance.add_description(scene_desc)

        # # Add any initial dialogue
        # context = POST.get("context")
        # print(f"Adding context {context}")
        # performance.add_dialogue(context)

        performance.load_script_string(self.performance_model.script)

        # Add a human performer
        human = HumanPerformer(character_name="Cammy")
        performance.add_performer(human)

        self.performance = performance

        # assert self.performance is not None
        # assert self.performance_model is not None

        self.performance.start_audio()

        super().start()

    def run(self):
        while self.running:
            components = self.performance.update_audio()

            # If there was dialogue from Speech-to-Text
            if components:
                # Add dialogue to database
                self.add_components(components)

                # Generate dialogue for bot character(s)
                bot_dialogue = self.generate_dialogue()

            # Sleep briefly
            time.sleep(0.1)

        # self.performance.stop_audio()

    def load_script_string(self, script_str: str):
        assert self.performance is not None

        # Load script into performance
        #@TODO this will reset the context of all chatbots. If the script is 
        # edited at a point in the script that precedes the maximum context
        # of the chatbots, there is no reason to reset their context. Whether
        # this is handled here and/or performance and/or llmber is TBD.
        self.performance.load_script_string(script_str)

        # Get interpreted script
        script = self.performance.get_script()

        # Update database
        self.performance_model.script = script
        self.performance_model.save()

        return script

    def generate_dialogue(self) -> list:
        # Generate dialogue for bot characters
        bot_dialogue = self.performance.generate_dialogue(1)

        # Perform dialogue
        self.performance.perform_components(bot_dialogue)

        # Add dialogue to database
        self.add_components(bot_dialogue)

        return bot_dialogue

    def add_components(self, components: list):
        new_dialogue: str = ""

        # # Convert components to string
        # #@REVISIT should we just run performance.get_script() again?
        # for component in components:
        #     new_dialogue += "\n\n"
        #     new_dialogue += component.to_str()

        # # Add Dialogue to database
        # self.performance_model.script += new_dialogue

        self.performance_model.script = self.performance.get_script()
        self.performance_model.save()

        print(f"New dialogue: {new_dialogue}")

    def get_status(self):
        if self.performance_model is None:
            return {}

        return {
            "script": self.performance_model.script,
            "characters": self.performance_model.characters,
        }
