import json
from dataclasses import dataclass, field
from functools import cached_property
from typing import Dict


@dataclass(frozen=True)
class MemoryUsage:
    disk: int
    ram: int

    @cached_property
    def disk_kb(self) -> float:
        return round(self.disk / 1024, 2)

    @cached_property
    def disk_mb(self) -> float:
        return round(self.disk_kb / 1024, 2)

    @cached_property
    def ram_kb(self) -> float:
        return round(self.ram / 1024, 2)

    @cached_property
    def ram_mb(self) -> float:
        return round(self.ram_kb / 1024, 2)

    @property
    def all_attributes(self):
        return dict(vars(self), disk_kb=self.disk_kb, ram_kb=self.ram_kb, disk_mb=self.disk_mb, ram_mb=self.ram_mb)


@dataclass(frozen=True)
class ColumnAnalysis:
    ram: int
    ram_fraction_of_total: float
    type: str

    @cached_property
    def ram_kb(self) -> float:
        return round(self.ram / 1024, 2)

    @cached_property
    def ram_mb(self) -> float:
        return round(self.ram_kb / 1024, 2)

    @cached_property
    def ram_percent_of_total(self) -> str:
        return f"{self.ram_fraction_of_total * 100:.2f}% of total"

    @property
    def all_attributes(self):
        return dict(vars(self), ram_kb=self.ram_kb, ram_mb=self.ram_mb, ram_percent_of_total=self.ram_percent_of_total)


@dataclass
class DataAnalysis:
    comment: str
    total: MemoryUsage
    columns: dict[str, ColumnAnalysis]


class DataAnalysisEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, MemoryUsage):
            return obj.all_attributes
        if isinstance(obj, ColumnAnalysis):
            return obj.all_attributes
        if isinstance(obj, Dict):
            return obj
        return vars(obj)
