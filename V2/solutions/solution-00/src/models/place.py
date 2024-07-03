from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Place(db.Model):
    """Place representation"""

    __tablename__ = 'places'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    address = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    host_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    city_id = db.Column(db.String(36), db.ForeignKey('cities.id'), nullable=False)
    price_per_night = db.Column(db.Integer, nullable=False)
    number_of_rooms = db.Column(db.Integer, nullable=False)
    number_of_bathrooms = db.Column(db.Integer, nullable=False)
    max_guests = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    host = db.relationship('User', back_populates='places')
    city = db.relationship('City', back_populates='places')

    def __init__(self, name: str, description: str, address: str, latitude: float, longitude: float, host_id: str, city_id: str, price_per_night: int, number_of_rooms: int, number_of_bathrooms: int, max_guests: int):
        self.name = name
        self.description = description
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.host_id = host_id
        self.city_id = city_id
        self.price_per_night = price_per_night
        self.number_of_rooms = number_of_rooms
        self.number_of_bathrooms = number_of_bathrooms
        self.max_guests = max_guests

    def __repr__(self) -> str:
        """String representation of the object"""
        return f"<Place {self.id} ({self.name})>"

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
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @staticmethod
    def create(data: dict) -> "Place":
        """Create a new place"""
        from src.models.user import User
        from src.models.city import City

        user = User.query.get(data["host_id"])
        if not user:
            raise ValueError(f"User with ID {data['host_id']} not found")

        city = City.query.get(data["city_id"])
        if not city:
            raise ValueError(f"City with ID {data['city_id']} not found")

        new_place = Place(
            name=data["name"],
            description=data.get("description", ""),
            address=data["address"],
            latitude=float(data["latitude"]),
            longitude=float(data["longitude"]),
            host_id=data["host_id"],
            city_id=data["city_id"],
            price_per_night=int(data["price_per_night"]),
            number_of_rooms=int(data["number_of_rooms"]),
            number_of_bathrooms=int(data["number_of_bathrooms"]),
            max_guests=int(data["max_guests"])
        )

        db.session.add(new_place)
        db.session.commit()

        return new_place

    @staticmethod
    def update(place_id: str, data: dict) -> "Place | None":
        """Update an existing place"""
        place = Place.query.get(place_id)

        if not place:
            return None

        for key, value in data.items():
            setattr(place, key, value)

        db.session.commit()

        return place
