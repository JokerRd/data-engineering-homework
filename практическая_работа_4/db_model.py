from typing import Optional

from sqlalchemy import String, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BIGINT, Integer, NVARCHAR, String, TIMESTAMP


class Base(DeclarativeBase):
    pass


class House(Base):
    __tablename__ = "house"

    id: Mapped[int] = mapped_column(BIGINT(), primary_key=True)
    name: Mapped[str]
    street: Mapped[str]
    city: Mapped[str]
    zipcode: Mapped[int] = mapped_column(BIGINT())
    floors: Mapped[int] = mapped_column(Integer())
    year: Mapped[int] = mapped_column(Integer())
    parking: Mapped[bool]
    prob_price: Mapped[int] = mapped_column(BIGINT())
    views: Mapped[int] = mapped_column(Integer())

    @staticmethod
    def create_from_dict(dict_: dict):
        house = House()
        for key in dict_:
            setattr(house, key, dict_[key])
        return house

    def to_dict(self):
        return {"id": self.id, "name": self.name, "street": self.street, "city": self.city,
                "zipcode": self.zipcode, "floors": self.floors, "year": self.year,
                "parking": self.parking, "prob_price": self.prob_price, "views": self.views}


class ReviewHouse(Base):
    __tablename__ = "review_house"

    id = mapped_column(Integer, primary_key=True, autoincrement='auto')
    name: Mapped[str]
    rating: Mapped[float]
    convenience: Mapped[int] = mapped_column(Integer())
    security: Mapped[int] = mapped_column(Integer())
    functionality: Mapped[int] = mapped_column(Integer())
    comment: Mapped[str]

    def __repr__(self):
        return (f"<ReviewHouse id={self.id}, name={self.name}, rating={self.rating}, "
                f"convenience={self.convenience}, security={self.security},"
                f" functionality={self.functionality}, comment={self.comment}>")

    @staticmethod
    def create_from_dict(dict_: dict):
        review_house = ReviewHouse()
        for key in dict_:
            setattr(review_house, key, dict_[key])
        return review_house

    def to_dict(self):
        return {'name': self.name, 'rating': self.rating,
                'convenience': self.convenience, 'security': self.security,
                'functionality': self.functionality, 'comment': self.comment}


class Song(Base):
    __tablename__ = "song"

    id = mapped_column(Integer, primary_key=True, autoincrement='auto')
    artist: Mapped[str]
    song: Mapped[str]
    duration_ms: Mapped[int] = mapped_column(Integer())
    year: Mapped[int] = mapped_column(Integer())
    tempo: Mapped[float]
    genre: Mapped[str]

    @staticmethod
    def create_from_dict(dict_: dict):
        song = Song()
        for key in dict_:
            setattr(song, key, dict_[key])
        return song

    def to_dict(self):
        return {'artist': self.artist, 'song': self.song, 'duration_ms': self.duration_ms,
                'year': self.year, 'tempo': self.tempo, 'genre': self.genre}


class Phone(Base):
    __tablename__ = "phone"

    id = mapped_column(Integer, primary_key=True, autoincrement='auto')
    from_city: Mapped[str]
    is_available: Mapped[bool]
    name: Mapped[str]
    price: Mapped[int] = mapped_column(Integer(), CheckConstraint("price >= 0"))
    quantity: Mapped[int] = mapped_column(Integer(), CheckConstraint("quantity >= 0"))
    views: Mapped[int] = mapped_column(Integer(), CheckConstraint("views >= 0"))
    count_update: Mapped[int] = mapped_column(Integer(), default=0)

    @staticmethod
    def create_from_dict(dict_: dict):
        phone = Phone()
        for key in dict_:
            if key == 'fromCity':
                setattr(phone, 'from_city', dict_[key])
            elif key == 'isAvailable':
                setattr(phone, 'is_available', dict_[key])
            elif key == 'price':
                setattr(phone, key, round(dict_[key]))
            else:
                setattr(phone, key, dict_[key])
        return phone

    def to_dict(self):
        return {'from_city': self.from_city, 'is_available': self.is_available,
                'name': self.name, 'price': self.price, 'quantity': self.quantity,
                'views': self.views, 'count_update': self.count_update}

    def __repr__(self):
        return (f'<Phone name={self.name}, from_city={self.from_city}, '
                f'is_available={self.is_available}, price={self.price}, '
                f'quantity={self.quantity}, views={self.views}, count_update={self.count_update}>')
