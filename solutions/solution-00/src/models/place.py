# src/models/place.py

from src.persistence import db
from src.models.base import Base
from src.models.city import City
from src.models.user import User
from src.persistence.sqlalchemy_repository import SQLAlchemyRepository


class Place(db.Model, Base):
    """Place representation"""

    __tablename__ = 'place'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    address = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    host_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    city_id = db.Column(db.String(36), db.ForeignKey('city.id'), nullable=False)
    price_per_night = db.Column(db.Integer, nullable=False)
    number_of_rooms = db.Column(db.Integer, nullable=False)
    number_of_bathrooms = db.Column(db.Integer, nullable=False)
    max_guests = db.Column(db.Integer, nullable=False)

    city = db.relationship('City', backref=db.backref('places', lazy=True))
    host = db.relationship('User', backref=db.backref('places', lazy=True))

    def __init__(self, data: dict | None = None, **kwargs) -> None:
        """Constructor"""
        super().__init__(**kwargs)

        if data:
            self.name = data.get("name", "")
            self.description = data.get("description", "")
            self.address = data.get("address", "")
            self.city_id = data["city_id"]
            self.latitude = float(data.get("latitude", 0.0))
            self.longitude = float(data.get("longitude", 0.0))
            self.host_id = data["host_id"]
            self.price_per_night = int(data.get("price_per_night", 0))
            self.number_of_rooms = int(data.get("number_of_rooms", 0))
            self.number_of_bathrooms = int(data.get("number_of_bathrooms", 0))
            self.max_guests = int(data.get("max_guests", 0))

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "city_id": self.city_id,
            "host_id": self.host_id,
            "price_per_night": self.price_per_night,
            "number_of_rooms": self.number_of_rooms,
            "number_of_bathrooms": self.number_of_bathrooms,
            "max_guests": self.max_guests,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict, repository: SQLAlchemyRepository) -> "Place":
        """Create a new place"""
        user = repository.get(User, data['host_id'])

        if not user:
            raise ValueError(f"User with ID {data['host_id']} not found")

        city = repository.get(City, data['city_id'])

        if not city:
            raise ValueError(f"City with ID {data['city_id']} not found")

        new_place = Place(data=data)
        repository.add(new_place)
        repository.commit()
        return new_place

    @staticmethod
    def update(place_id: str, data: dict, repository: SQLAlchemyRepository) -> "Place | None":
        """Update an existing place"""
        place = repository.get(Place, place_id)

        if not place:
            return None

        for key, value in data.items():
            setattr(place, key, value)

        repository.commit()
        return place

    @staticmethod
    def delete(place_id: str, repository: SQLAlchemyRepository) -> bool:
        """Delete a place by ID"""
        place = repository.get(Place, place_id)

        if not place:
            return False

        repository.delete(place)
        repository.commit()
        return True

    @staticmethod
    def get(place_id: str, repository: SQLAlchemyRepository) -> "Place | None":
        """Get a place by ID"""
        return repository.get(Place, place_id)

    @staticmethod
    def get_all(repository: SQLAlchemyRepository) -> list["Place"]:
        """Get all places"""
        return repository.all(Place)
