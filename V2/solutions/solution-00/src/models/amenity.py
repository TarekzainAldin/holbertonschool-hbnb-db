from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Amenity(db.Model):
    """Amenity representation"""

    __tablename__ = 'amenities'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    def __init__(self, name: str):
        self.name = name

    def __repr__(self) -> str:
        """String representation of the object"""
        return f"<Amenity {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @staticmethod
    def create(data: dict) -> "Amenity":
        """Create a new amenity"""
        existing_amenity = Amenity.query.filter_by(name=data["name"]).first()

        if existing_amenity:
            raise ValueError("Amenity already exists")

        new_amenity = Amenity(name=data["name"])

        db.session.add(new_amenity)
        db.session.commit()

        return new_amenity

    @staticmethod
    def update(amenity_id: str, data: dict) -> "Amenity":
        """Update an existing amenity"""
        amenity = Amenity.query.get(amenity_id)

        if not amenity:
            return None

        if "name" in data:
            amenity.name = data["name"]

        db.session.commit()

        return amenity


class PlaceAmenity(db.Model):
    """PlaceAmenity representation"""

    __tablename__ = 'place_amenities'

    id = db.Column(db.String(36), primary_key=True)
    place_id = db.Column(db.String(36), nullable=False)
    amenity_id = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    def __init__(self, place_id: str, amenity_id: str):
        self.place_id = place_id
        self.amenity_id = amenity_id

    def __repr__(self) -> str:
        """String representation of the object"""
        return f"<PlaceAmenity ({self.place_id} - {self.amenity_id})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "place_id": self.place_id,
            "amenity_id": self.amenity_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @staticmethod
    def get(place_id: str, amenity_id: str) -> "PlaceAmenity":
        """Get a PlaceAmenity object by place_id and amenity_id"""
        return PlaceAmenity.query.filter_by(place_id=place_id, amenity_id=amenity_id).first()

    @staticmethod
    def create(data: dict) -> "PlaceAmenity":
        """Create a new PlaceAmenity object"""
        new_place_amenity = PlaceAmenity(place_id=data["place_id"], amenity_id=data["amenity_id"])

        db.session.add(new_place_amenity)
        db.session.commit()

        return new_place_amenity

    @staticmethod
    def delete(place_id: str, amenity_id: str) -> bool:
        """Delete a PlaceAmenity object by place_id and amenity_id"""
        place_amenity = PlaceAmenity.get(place_id, amenity_id)

        if not place_amenity:
            return False

        db.session.delete(place_amenity)
        db.session.commit()

        return True

    @staticmethod
    def update(entity_id: str, data: dict):
        """Not implemented, isn't needed"""
        raise NotImplementedError(
            "This method is defined only because of the Base class"
        )
