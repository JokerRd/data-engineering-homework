import datetime
from typing import Optional

from sqlalchemy import String, CheckConstraint, Date
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


class Club(Base):
    __tablename__ = "clubs"

    club_id = mapped_column(Integer, primary_key=True)
    club_code: Mapped[str]
    name: Mapped[str]
    squad_size: Mapped[int]
    average_age: Mapped[Optional[float]]
    foreigners_number: Mapped[int]
    national_team_players: Mapped[int]
    stadium_name: Mapped[str]
    stadium_seats: Mapped[int]
    net_transfer_record: Mapped[str]
    last_season: Mapped[int]

    @staticmethod
    def create_from_dict(dict_: dict):
        club = Club()
        for key in dict_:
            setattr(club, key, dict_[key])
        return club

    def to_dict(self):
        return {'club_id': self.club_id, 'club_code': self.club_code, 'name': self.name,
                'squad_size': self.squad_size, ' average_age': self.average_age,
                'foreigners_number': self.foreigners_number, ' national_team_players': self.national_team_players,
                'stadium_name': self.stadium_name, 'stadium_seats': self.stadium_seats,
                'net_transfer_record': self.net_transfer_record, 'last_season': self.last_season}


class ClubGame(Base):
    __tablename__ = 'club_games'

    id = mapped_column(Integer, primary_key=True, autoincrement='auto')
    game_id: Mapped[int]
    club_id: Mapped[int]
    own_goals: Mapped[int]
    own_position: Mapped[Optional[int]]
    own_manager_name: Mapped[str]
    opponent_id: Mapped[int]
    opponent_goals: Mapped[int]
    opponent_position: Mapped[Optional[int]]
    opponent_manager_name: Mapped[str]
    hosting: Mapped[str]
    is_win: Mapped[bool]

    @staticmethod
    def create_from_dict(dict_: dict):
        club_games = ClubGame()
        for key in dict_:
            setattr(club_games, key, dict_[key])
        return club_games

    def to_dict(self):
        return {'game_id': self.game_id, 'club_id': self.club_id, 'own_goals': self.own_goals,
                'own_position': self.own_position, 'own_manager_name': self.own_manager_name,
                'opponent_goals': self.opponent_goals, 'opponent_position': self.opponent_position,
                'opponent_manager_name': self.opponent_manager_name, 'hosting': self.hosting, 'is_win': self.is_win}


class Player(Base):
    __tablename__ = 'players'

    player_id = mapped_column(Integer, primary_key=True)
    first_name: Mapped[Optional[str]]
    last_name: Mapped[str]
    name: Mapped[str]
    last_season: Mapped[int]
    current_club_id: Mapped[int]
    country_of_birth: Mapped[Optional[str]]
    city_of_birth: Mapped[Optional[str]]
    date_of_birth: Mapped[Optional[datetime.date]]
    position: Mapped[str]
    foot: Mapped[Optional[str]]
    height_in_cm: Mapped[Optional[int]]
    market_value_in_eur: Mapped[Optional[int]]

    @staticmethod
    def create_from_dict(dict_: dict):
        player = Player()
        for key in dict_:
            setattr(player, key, dict_[key])
        return player

    def to_dict(self):
        return {'player_id': self.player_id, 'first_name': self.first_name, 'last_name': self.last_name,
                'name': self.name, 'last_season': self.last_season, 'current_club_id': self.current_club_id,
                'country_of_birth': self.country_of_birth, 'city_of_birth': self.city_of_birth,
                'date_of_birth': self.date_of_birth, 'position': self.position, 'foot': self.foot,
                'height_in_cm': self.height_in_cm, 'market_value_in_eur': self.market_value_in_eur}
