from typing import Optional
from typing import Set

from queue_task.models.resourses import Resources
from queue_task.models.task import Task


class TaskQueue:
    def __init__(self, max_cpu_cores: int, max_gpu_cores: int, max_ram: int):
        """
        Create a queue for tasks with resource limitations
        :param max_cpu_cores: The maximum number of CPU cores that a queued task can require
        :param max_gpu_cores: Maximum GPUs that a queued task can require
        :param max_ram: The maximum amount of memory that a queued task can require
        """
        self.ram_to_tasks = [set() for _ in range(max_ram + 1)]
        self.cpu_to_tasks = [set() for _ in range(max_cpu_cores + 1)]
        self.gpu_to_tasks = [set() for _ in range(max_gpu_cores + 1)]

    def add_task(self, task: Task) -> None:
        """
        Add a task to the queue
        :param task: Task instance
        """
        resources = task.resources
        self.ram_to_tasks[resources.ram].add(task)
        self.cpu_to_tasks[resources.cpu_cores].add(task)
        self.gpu_to_tasks[resources.gpu_count].add(task)

    def get_task(self, available_resources: Resources) -> Optional[Task]:
        """
        Get a task from the queue that satisfies the constraints of the given resources
        :param available_resources: Limiting resources
        :return: Task satisfying resources if it exists in the queue, None otherwise
        """
        available_ram = available_resources.ram
        available_cpu_cores = available_resources.cpu_cores
        available_gpu_count = available_resources.gpu_count
        found_tasks = set()
        found_tasks.update(self._get_tasks_by_ram(available_ram))
        found_tasks.update(self._get_tasks_by_cpu_cores(available_cpu_cores))
        found_tasks.update(self._get_tasks_by_gpu_count(available_gpu_count))
        if found_tasks:
            found_task = max(found_tasks, key=lambda task: task.priority)
            self._remove_task(found_task)
            return found_task

    def _get_tasks_by_ram(self, available_ram: int) -> Set[Task]:
        """
        Get from the queue all tasks that require no more than the specified amount of RAM
        :param available_ram: Limit on the amount of RAM
        :return: A set with all tasks satisfying the constraint
        """
        found_tasks = set()
        for ram in range(available_ram + 1):
            tasks = self.ram_to_tasks[ram]
            found_tasks.update(tasks)
        return found_tasks

    def _get_tasks_by_cpu_cores(self, available_cpu_cores: int) -> Set[Task]:
        """
        Get from the queue all tasks that require no more than the specified number of CPU cores
        :param available_cpu_cores: Limit on the number of CPU cores
        :return: A set with all tasks satisfying the constraint
        """
        found_tasks = set()
        for cpu_cores in range(available_cpu_cores + 1):
            tasks = self.cpu_to_tasks[cpu_cores]
            found_tasks.update(tasks)
        return found_tasks

    def _get_tasks_by_gpu_count(self, available_gpu_count: int) -> Set[Task]:
        """
        Get from the queue all tasks that require no more than the specified number of GPUs
        :param available_gpu_count: Limit on the number of GPUs
        :return: A set with all tasks satisfying the constraint
        """
        found_tasks = set()
        for ram in range(available_gpu_count + 1):
            tasks = self.gpu_to_tasks[ram]
            found_tasks.update(tasks)
        return found_tasks

    def _remove_task(self, task: Task) -> None:
        """
        Remove a task from the queue if it exists
        :param task: The task to be removed
        """
        task_ram = task.resources.ram
        task_cpu_cores = task.resources.cpu_cores
        task_gpu_count = task.resources.gpu_count
        self.ram_to_tasks[task_ram].remove(task)
        self.cpu_to_tasks[task_cpu_cores].remove(task)
        self.gpu_to_tasks[task_gpu_count].remove(task)
