from typing import Optional
from typing import Set

from queue_task.models.resourses import Resources
from queue_task.models.task import Task


class TaskQueue:
    def __init__(self, max_cpu_cores: int, max_gpu_cores: int, max_ram: int):
        self.ram_to_tasks = [set() for _ in range(max_ram + 1)]
        self.cpu_to_tasks = [set() for _ in range(max_cpu_cores + 1)]
        self.gpu_to_tasks = [set() for _ in range(max_gpu_cores + 1)]

    def add_task(self, task: Task):
        resources = task.resources
        self.ram_to_tasks[resources.ram].add(task)
        self.cpu_to_tasks[resources.cpu_cores].add(task)
        self.gpu_to_tasks[resources.gpu_count].add(task)

    def get_task(self, available_resources: Resources) -> Optional[Task]:
        available_ram = available_resources.ram
        available_cpu_cores = available_resources.cpu_cores
        available_gpu_count = available_resources.gpu_count
        found_tasks = set()
        found_tasks.update(self.get_task_by_ram(available_ram))
        found_tasks.update(self.get_task_by_cpu_cores(available_cpu_cores))
        found_tasks.update(self.get_task_by_gpu_count(available_gpu_count))
        if found_tasks:
            found_task = max(found_tasks, key=lambda task: task.priority)
            self.remove_task(found_task)
            return found_task

    def get_task_by_ram(self, available_ram: int) -> Set[Task]:
        found_tasks = set()
        for ram in range(available_ram + 1):
            tasks = self.ram_to_tasks[ram]
            found_tasks.update(tasks)
        return found_tasks

    def get_task_by_cpu_cores(self, available_cpu_cores: int) -> Set[Task]:
        found_tasks = set()
        for cpu_cores in range(available_cpu_cores + 1):
            tasks = self.cpu_to_tasks[cpu_cores]
            found_tasks.update(tasks)
        return found_tasks

    def get_task_by_gpu_count(self, available_gpu_count: int) -> Set[Task]:
        found_tasks = set()
        for ram in range(available_gpu_count + 1):
            tasks = self.gpu_to_tasks[ram]
            found_tasks.update(tasks)
        return found_tasks

    def remove_task(self, task: Task):
        task_ram = task.resources.ram
        task_cpu_cores = task.resources.cpu_cores
        task_gpu_count = task.resources.gpu_count
        self.ram_to_tasks[task_ram].remove(task)
        self.cpu_to_tasks[task_cpu_cores].remove(task)
        self.gpu_to_tasks[task_gpu_count].remove(task)
