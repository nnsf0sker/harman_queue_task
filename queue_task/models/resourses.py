from dataclasses import dataclass


@dataclass(frozen=True)
class Resources:
    ram: int
    cpu_cores: int
    gpu_count: int
