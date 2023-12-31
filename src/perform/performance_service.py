import time
from typing import Optional

from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from bot_aukerman import Performance,\
        BotPerformer,\
        HumanPerformer

from .models import Performance as PerformanceModel
from .service import Service

class PerformanceService(Service):
    performance: Optional[Performance]
    performance_model: Optional[PerformanceModel]
    # channel_layer: Optional[object]

    def __init__(self):
        super().__init__('PerformanceService')
        self.performance = None
        self.performance_model = None

    def start(self, performance_model: PerformanceModel):
        if self.running == True:
            return

        #@REVISIT weird architecture
        self.performance_model = performance_model

        # Create a Performance
        # model_config = {
        #     "model": "gpt2-large",
        #     "use_cuda": True, #@REVISIT!
        #     "max_context_length": 200, #@REVISIT!
        #     # "model": "gpt2"
        #     # "model": "gpt4all-7B-unfiltered", "engine": "llamacpp"
        #     # "model": "text-ada-001", "engine": "openai",
        #     # "engine": "openai",
        # }

        # performance = Performance(model_config = model_config,
        #                           resume_from_log = False)

        performance = Performance(resume_from_log = False)

        # Add characters
        for character in self.performance_model.characters.all():
            # If character is human
            if(character.performer == 'human'):
                character = HumanPerformer(
                    character_name=character.name,
                    character_desc=character.description,
                )

            # Otherwise, assume `performer` is a model name
            #@REVISIT architecture
            else:
                #@REVISIT architecture
                match character.performer:
                    case 'gpt2' | 'gpt2-medium' | 'gpt2-large':
                        model_config = {
                            "model": character.performer,
                            "use_cuda": True, #@REVISIT!
                            "max_context_length": 200, #@REVISIT!
                        }

                        character = BotPerformer(
                            character_name=character.name,
                            character_desc=character.description,
                            model_config=model_config,
                        )

                    case 'text-davinci-003' | 'gpt-3.5-turbo':
                        model_config = {
                            "model": character.performer,
                            "engine": "openai",
                            #@REVISIT naming:
                            "api_env_var": "OPENAI_API_KEY",
                        }

                        character = BotPerformer(
                            character_name=character.name,
                            character_desc=character.description,
                            model_config=model_config,
                        )

                    case _:
                        raise Exception(
                            f"Unknown performer type {character.performer}"
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

                # Communicate dialogue to client
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    "new_dialogue",
                    {
                        "type": "dialogue.message",
                    }
                )

                # Generate dialogue for bot character(s)
                bot_dialogue = self.generate_dialogue()

                # Communicate dialogue to client
                async_to_sync(channel_layer.group_send)(
                    "new_dialogue",
                    {
                        "type": "dialogue.message",
                    }
                )

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

        # Add dialogue to database
        self.add_components(bot_dialogue)

        # Perform dialogue
        self.performance.perform_components(bot_dialogue)

        return bot_dialogue

    def interrupt(self):
        self.performance.interrupt()

    #@REVISIT architecture; scaffolding
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
