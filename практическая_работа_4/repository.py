from практическая_работа_4.db_model import House, ReviewHouse, Song, Phone
from sqlalchemy.orm import Session
from sqlalchemy import select, text, func


class HouseRepository:

    def __init__(self, engine):
        self.engine = engine

    def save_all(self, house_list: list[House]):
        with Session(self.engine) as session:
            session.add_all(house_list)
            session.commit()

    def get_sorted(self, sort, limit: int) -> list[House]:
        with (Session(self.engine) as session):
            query = (select(House)
                     .order_by(sort)
                     .limit(limit))
            return list(session.scalars(query))

    def get_sum(self, field) -> int:
        with Session(self.engine) as session:
            query = func.sum(field)
            return int(session.scalar(query))

    def get_min(self, field) -> int:
        with Session(self.engine) as session:
            query = func.min(field)
            return int(session.scalar(query))

    def get_max(self, field) -> int:
        with Session(self.engine) as session:
            query = func.max(field)
            return int(session.scalar(query))

    def get_avg(self, field) -> float:
        with Session(self.engine) as session:
            query = func.avg(field)
            return float(session.scalar(query))

    def get_frequency(self, field):
        with Session(self.engine) as session:
            query = select(field, func.count(field).label("count")).group_by(field)
            return list(session.execute(query))

    def get_by_great_than_floor_and_between_year(self, floor_value, from_year, to_year, sort, limit):
        with Session(self.engine) as session:
            query = (select(House)
                     .where(House.floors > floor_value)
                     .where(House.year.between(from_year, to_year))
                     .order_by(sort)
                     .limit(limit))
            return list(session.scalars(query))

    def get_review_by_in_city(self, cities: list[str], sort_review):
        with Session(self.engine) as session:
            query = (select(ReviewHouse)
                     .select_from(House)
                     .join(ReviewHouse, House.name == ReviewHouse.name)
                     .where(House.city.in_(cities))
                     .order_by(sort_review))
            return list(session.scalars(query))

    def get_house_with_max_rating(self, limit):
        with Session(self.engine) as session:
            sub_query = (select(ReviewHouse.name.label("name"), func.max(ReviewHouse.rating).label('rating'))
                         .group_by(ReviewHouse.name)
                         .subquery())
            query = (select(House, sub_query.c.rating)
                     .select_from(House).join(sub_query, House.name == sub_query.c.name)
                     .where(sub_query.c.rating is not None)
                     .order_by(sub_query.c.rating.desc())
                     .limit(limit))
            print(query)
            return list(session.execute(query))

    def get_review_by_year_house_between(self, year_start, year_end, sort, limit):
        with Session(self.engine) as session:
            query = (select(ReviewHouse)
                     .select_from(House)
                     .join(ReviewHouse, House.name == ReviewHouse.name)
                     .where(House.year.between(year_start, year_end))
                     .order_by(sort)
                     .limit(limit))
            return list(session.scalars(query))


class ReviewHouseRepository:
    def __init__(self, engine):
        self.engine = engine

    def save_all(self, review_house_list: list[ReviewHouse]):
        with Session(self.engine) as session:
            session.add_all(review_house_list)
            session.commit()


class SongRepository:
    def __init__(self, engine):
        self.engine = engine

    def save_all(self, song_list: list[Song]):
        with Session(self.engine) as session:
            session.add_all(song_list)
            session.commit()

    def get_sorted(self, sort, limit: int) -> list[Song]:
        with (Session(self.engine) as session):
            query = (select(Song)
                     .order_by(sort)
                     .limit(limit))
            return list(session.scalars(query))

    def get_sum(self, field) -> int:
        with Session(self.engine) as session:
            query = func.sum(field)
            return int(session.scalar(query))

    def get_min(self, field) -> int:
        with Session(self.engine) as session:
            query = func.min(field)
            return int(session.scalar(query))

    def get_max(self, field) -> int:
        with Session(self.engine) as session:
            query = func.max(field)
            return int(session.scalar(query))

    def get_avg(self, field) -> float:
        with Session(self.engine) as session:
            query = func.avg(field)
            return float(session.scalar(query))

    def get_frequency(self, field):
        with Session(self.engine) as session:
            query = select(field, func.count(field).label("count")).group_by(field)
            return list(session.execute(query))

    def get_by_genre_and_between_year(self, genre, from_year, to_year, sort, limit):
        with Session(self.engine) as session:
            query = (select(Song)
                     .where(Song.genre.contains(genre))
                     .where(Song.year.between(from_year, to_year))
                     .order_by(sort)
                     .limit(limit))
            return list(session.scalars(query))


class PhoneRepository:
    def __init__(self, engine):
        self.engine = engine

    def save_all(self, phone_list: list[Phone]):
        with Session(self.engine) as session:
            session.add_all(phone_list)
            session.commit()