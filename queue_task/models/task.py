from dataclasses import dataclass

from queue_task.models.resourses import Resources


@dataclass
class Task:
    id: int
    priority: int
    resources: Resources
    content: str
    result: str

    def __hash__(self):
        return self.id
