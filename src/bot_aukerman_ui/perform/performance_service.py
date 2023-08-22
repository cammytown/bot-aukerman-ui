from typing import Optional
from bot_aukerman import Performance
from .service import Service

class PerformanceService(Service):
    performance: Optional[Performance]

    def __init__(self):
        super().__init__('PerformanceService')
        self.performance = None

    def start(self, performance):
        if self.running == True:
            raise Exception("PerformanceService is already running")

        assert performance is not None

        self.performance = performance
        super().start()

    def run(self):
        assert self.performance is not None

        self.performance.start()
