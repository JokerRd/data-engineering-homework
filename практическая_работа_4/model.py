import datetime
import json
from dataclasses import dataclass

from практическая_работа_4.db_model import House, ReviewHouse, Song, Phone, Club, ClubGame, Player



@dataclass
class StatInformation:
    name_field: str
    sum: int
    mean: float
    min: int
    max: int

@dataclass
class OnlyStatInformation:
    count: int
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
    sorted_data: list
    filtered_data: list
    stat: StatInformation
    frequency: FrequencyInformation


class DataEncoder(json.JSONEncoder):
    def default(self, obj):
        if (isinstance(obj, House) or isinstance(obj, ReviewHouse)
                or isinstance(obj, Song) or isinstance(obj, Phone) or isinstance(obj, Club)
                or isinstance(obj, ClubGame) or isinstance(obj, Player)):
            return obj.to_dict()
        print(obj)
        if isinstance(obj, datetime.date):
            return str(obj)
        dict_obj = dict(vars(obj))
        new_dict = {}
        for key, value in dict_obj.items():
            if value is not None:
                new_dict[key] = value
        return new_dict
