from datetime import datetime
from typing import Optional
import uuid
from xmlrpc.client import DateTime
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base import Base

class Amenity(Base):
    """Amenity representation"""
    
    __tablename__ = 'amenities'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, name: str, **kwargs) -> None:
        """Amenity init"""
        super().__init__(**kwargs)
        self.name = name

    def __repr__(self) -> str:
        """Amenity repr"""
        return f"<Amenity {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(session, data: dict) -> "Amenity":
        """Create a new amenity"""
        amenity = Amenity(**data)
        session.add(amenity)
        session.commit()
        return amenity

    @staticmethod
    def update(session, amenity_id: str, data: dict) -> "Amenity | None":
        """Update an existing amenity"""
        amenity: Amenity = session.query(Amenity).filter_by(id=amenity_id).first()
        if not amenity:
            return None
        if "name" in data:
            amenity.name = data["name"]
        session.commit()
        return amenity


class PlaceAmenity(Base):
    """PlaceAmenity representation"""
    
    __tablename__ = 'place_amenities'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    place_id = Column(String(36), ForeignKey('places.id'), nullable=False)
    amenity_id = Column(String(36), ForeignKey('amenities.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, place_id: str, amenity_id: str, **kwargs) -> None:
        """PlaceAmenity init"""
        super().__init__(**kwargs)
        self.place_id = place_id
        self.amenity_id = amenity_id

    def __repr__(self) -> str:
        """PlaceAmenity repr"""
        return f"<PlaceAmenity ({self.place_id} - {self.amenity_id})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "place_id": self.place_id,
            "amenity_id": self.amenity_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def get(session, place_id: str, amenity_id: str) -> "PlaceAmenity | None":
        """Get a PlaceAmenity object by place_id and amenity_id"""
        return session.query(PlaceAmenity).filter_by(place_id=place_id, amenity_id=amenity_id).first()

    @staticmethod
    def create(session, data: dict) -> "PlaceAmenity":
        """Create a new PlaceAmenity object"""
        new_place_amenity = PlaceAmenity(**data)
        session.add(new_place_amenity)
        session.commit()
        return new_place_amenity

    @staticmethod
    def delete(session, place_id: str, amenity_id: str) -> bool:
        """Delete a PlaceAmenity object by place_id and amenity_id"""
        place_amenity = PlaceAmenity.get(session, place_id, amenity_id)
        if not place_amenity:
            return False
        session.delete(place_amenity)
        session.commit()
        return True

    @staticmethod
    def update(session, entity_id: str, data: dict):
        """Not implemented, isn't needed"""
        raise NotImplementedError(
            "This method is defined only because of the Base class"
        )
