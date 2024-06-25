from src.persistence import db
from src.models.base import Base
from src.models.country import Country
from src.persistence.sqlalchemy_repository import SQLAlchemyRepository


class City(db.Model, Base):
    """City representation"""

    __tablename__ = 'city'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    country_code = db.Column(db.String(10), db.ForeignKey('country.code'), nullable=False)

    country = db.relationship('Country', backref=db.backref('cities', lazy=True))

    def __init__(self, name: str, country_code: str, **kwargs) -> None:
        """Constructor"""
        super().__init__(**kwargs)
        self.name = name
        self.country_code = country_code

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "country_code": self.country_code,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict, repository: SQLAlchemyRepository) -> "City":
        """Create a new city"""
        country = repository.get(Country, data['country_code'])

        if not country:
            raise ValueError("Country not found")

        city = City(name=data['name'], country_code=data['country_code'])
        repository.add(city)
        repository.commit()
        return city

    @staticmethod
    def update(city_id: str, data: dict, repository: SQLAlchemyRepository) -> "City | None":
        """Update an existing city"""
        city = repository.get(City, city_id)

        if not city:
            raise ValueError("City not found")

        if 'name' in data:
            city.name = data['name']

        if 'country_code' in data:
            city.country_code = data['country_code']

        repository.commit()
        return city

    @staticmethod
    def delete(city_id: str, repository: SQLAlchemyRepository) -> bool:
        """Delete a city by ID"""
        city = repository.get(City, city_id)

        if not city:
            return False

        repository.delete(city)
        repository.commit()
        return True

    @staticmethod
    def get(city_id: str, repository: SQLAlchemyRepository) -> "City | None":
        """Get a city by ID"""
        return repository.get(City, city_id)

    @staticmethod
    def get_all(repository: SQLAlchemyRepository) -> list["City"]:
        """Get all cities"""
        return repository.all(City)
