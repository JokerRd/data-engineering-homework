import json
from dataclasses import dataclass


@dataclass
class StatInformation:
    name_field: str
    sum: int
    mean: float
    min: int
    max: int


@dataclass
class FrequencyInformation:
    name_field: str
    frequency_by_name: dict[str, int]


@dataclass
class DataInformation:
    raw_data: list
    sorted_data: list
    filtered_data: list
    stat: StatInformation
    frequency: FrequencyInformation


@dataclass
class ChessInformation:
    type: str | None = None
    tournament: str | None = None
    city: str | None = None
    date: str | None = None
    round_count: int | None = None
    time_control: str | None = None
    min_rating: int | None = None
    url_img: str | None = None
    rating: float | None = None
    count_view: int | None = None


class DataEncoder(json.JSONEncoder):
    def default(self, obj):
        return vars(obj)
