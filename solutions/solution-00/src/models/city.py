from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.models.base import Base

class City(Base):
    __tablename__ = 'cities'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    country_code = Column(String, ForeignKey('countries.code'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    country = relationship("Country", backref="cities")

    def __init__(self, name: str, country_code: str, id=None) -> None:
        super().__init__()
        self.id = id  # Assuming id is generated elsewhere or handled by SQLAlchemy
        self.name = name
        self.country_code = country_code

    def __repr__(self) -> str:
        return f"<City {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "country_code": self.country_code,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "City":
        from src.persistence import repo
        from src.models.country import Country

        country_code = data.get("country_code")
        country = Country.query.filter_by(code=country_code).first()

        if not country:
            raise ValueError("Country not found")

        new_city = City(
            name=data["name"],
            country_code=country_code
        )

        repo.session.add(new_city)
        repo.session.commit()

        return new_city

    @staticmethod
    def update(city_id: str, data: dict) -> "City":
        from src.persistence import repo

        city = City.query.get(city_id)

        if not city:
            raise ValueError("City not found")

        for key, value in data.items():
            setattr(city, key, value)

        repo.session.commit()

        return city
