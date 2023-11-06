from dataclasses import dataclass

from queue_task.models.resourses import Resources


@dataclass(frozen=True)
class Task:
    id: int
    priority: int
    resources: Resources
    content: str
    result: str
