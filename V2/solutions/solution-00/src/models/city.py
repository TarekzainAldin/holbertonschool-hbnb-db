from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class City(db.Model):
    """City representation"""

    __tablename__ = 'cities'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country_code = db.Column(db.String(36), db.ForeignKey('countries.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    country = db.relationship('Country', back_populates='cities')

    def __init__(self, name: str, country_code: str):
        self.name = name
        self.country_code = country_code

    def __repr__(self) -> str:
        """String representation of the object"""
        return f"<City {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "country_code": self.country_code,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @staticmethod
    def create(data: dict) -> "City":
        """Create a new city"""
        from src.models.country import Country

        country = Country.query.get(data["country_code"])

        if not country:
            raise ValueError("Country not found")

        new_city = City(name=data["name"], country_code=data["country_code"])

        db.session.add(new_city)
        db.session.commit()

        return new_city

    @staticmethod
    def update(city_id: str, data: dict) -> "City":
        """Update an existing city"""
        city = City.query.get(city_id)

        if not city:
            raise ValueError("City not found")

        if "name" in data:
            city.name = data["name"]
        if "country_code" in data:
            city.country_code = data["country_code"]

        db.session.commit()

        return city
