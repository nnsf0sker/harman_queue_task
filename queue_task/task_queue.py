from dataclasses import dataclass


@dataclass
class Resources:
    ram: int
    cpu_cores: int
    gpu_count: int


@dataclass
class Task:
    id: int
    priority: int
    resources: Resources
    content: str
    result: str


class TaskQueue:
    def add_task(self):
        pass

    def get_task(self, available_resources: Resources) -> Task:
        pass
