from config import MAX_RAM
from config import MAX_CPU_CORES
from config import MAX_GPU_CORES

from queue_task.models.resourses import Resources
from queue_task.models.task import Task
from queue_task.task_queue import TaskQueue


MIN_RESOURCES = Resources(
    ram=0,
    cpu_cores=0,
    gpu_count=0,
)

MAX_RESOURCES = Resources(
    ram=MAX_RAM,
    cpu_cores=MAX_CPU_CORES,
    gpu_count=MAX_GPU_CORES,
)


def test_task_queue():
    task_queue = TaskQueue(1024, 1024, 1024)

    top_task = Task(0, 2, Resources(ram=1, cpu_cores=1, gpu_count=1), "", "")
    mid_task = Task(0, 1, Resources(ram=1, cpu_cores=1, gpu_count=1), "", "")
    low_task = Task(0, 0, Resources(ram=1, cpu_cores=1, gpu_count=1), "", "")

    task_queue.add_task(top_task)
    task_queue.add_task(mid_task)
    task_queue.add_task(low_task)

    assert task_queue.get_task(MAX_RESOURCES) == top_task
    assert task_queue.get_task(MAX_RESOURCES) == mid_task
    assert task_queue.get_task(MAX_RESOURCES) == low_task


def test_task_queue_empty():
    task_queue = TaskQueue(max_ram=MAX_RAM, max_cpu_cores=MAX_CPU_CORES, max_gpu_cores=MAX_GPU_CORES)
    assert task_queue.get_task(MAX_RESOURCES) is None


def test_task_queue_with_not_enough_resources():
    task_queue = TaskQueue(max_ram=MAX_RAM, max_cpu_cores=MAX_CPU_CORES, max_gpu_cores=MAX_GPU_CORES)

    task = Task(0, 1, Resources(ram=1, cpu_cores=1, gpu_count=1), "", "")
    task_queue.add_task(task)

    assert task_queue.get_task(MIN_RESOURCES) is None
