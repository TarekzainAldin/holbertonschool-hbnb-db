from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Country(db.Model):
    """Country representation"""

    __tablename__ = 'countries'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(3), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    cities = db.relationship('City', back_populates='country', lazy=True)

    def __init__(self, name: str, code: str):
        self.name = name
        self.code = code

    def __repr__(self) -> str:
        """String representation of the object"""
        return f"<Country {self.code} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @staticmethod
    def get_all() -> list["Country"]:
        """Get all countries"""
        return Country.query.all()

    @staticmethod
    def get(code: str) -> "Country":
        """Get a country by its code"""
        return Country.query.filter_by(code=code).first()

    @staticmethod
    def create(name: str, code: str) -> "Country":
        """Create a new country"""
        new_country = Country(name=name, code=code)

        db.session.add(new_country)
        db.session.commit()

        return new_country
