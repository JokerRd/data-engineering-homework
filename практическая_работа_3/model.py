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


@dataclass
class PhoneInformation:
    id: int | None = None
    model: str | None = None
    screen_size_inch: float | None = None
    memory_storage_gb: int | None = None
    price_rub: int | None = None
    bonus: int | None = None
    processor: str | None = None
    ram_gb: int | None = None
    count_sim: int | None = None
    matrix: str | None = None
    resolution: str | None = None
    size_camera_mp: int | None = None
    acc_mah: str | None = None


@dataclass
class StarInformation:
    name: str | None = None
    constellation: str | None = None
    spectral_class: str | None = None
    radius: int | None = None
    rotation_day: float | None = None
    age_b_years: float | None = None
    distance_m_km: float | None = None
    absolute_magnitude_m_km: float | None = None


@dataclass
class ClothingInformation:
    id: int | None = None
    name: str | None = None
    category: str | None = None
    size: str | None = None
    color: str | None = None
    material: str | None = None
    price: int | None = None
    rating: float | None = None
    reviews: int | None = None
    new: bool | None = None
    exclusive: bool | None = None
    sporty: bool | None = None


@dataclass
class JigsawInformation:
    name: str | None = None
    price: int | None = None
    type: str | None = None
    power_wt: int | None = None
    net_weight: float | None = None
    max_cutting_thickness_wood_mm: int | None = None
    max_cutting_thickness_metal_mm: int | None = None
    pendulum_stroke: bool | None = None
    handle_shape: str | None = None
    saw_stroke_mm: int | None = None


@dataclass
class AngleGrinderInformation:
    name: str | None = None
    price: int | None = None
    rating: int | None = None
    power_wt: int | None = None
    disk_diameter_mm: int | None = None
    rpm: str | None = None
    maintaining_constant_rpm_under_load: bool | None = None
    connect_vacuum_cleaner: bool | None = None
    smooth_start: bool | None = None
    net_weight: float | None = None


class DataEncoder(json.JSONEncoder):
    def default(self, obj):
        return vars(obj)
