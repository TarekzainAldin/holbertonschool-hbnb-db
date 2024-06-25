from src.persistence import db
from src.models.base import Base
from src.persistence.sqlalchemy_repository import SQLAlchemyRepository


class Country(db.Model, Base):
    """Country representation"""

    __tablename__ = 'country'

    code = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __init__(self, name: str, code: str, **kwargs) -> None:
        """Constructor"""
        super().__init__(**kwargs)
        self.name = name
        self.code = code

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "name": self.name,
            "code": self.code,
        }

    @staticmethod
    def get_all(repository: SQLAlchemyRepository) -> list["Country"]:
        """Get all countries"""
        return repository.all(Country)

    @staticmethod
    def get(code: str, repository: SQLAlchemyRepository) -> "Country | None":
        """Get a country by its code"""
        return repository.get(Country, code)

    @staticmethod
    def create(name: str, code: str, repository: SQLAlchemyRepository) -> "Country":
        """Create a new country"""
        country = Country(name=name, code=code)
        repository.add(country)
        repository.commit()
        return country

    @staticmethod
    def update(code: str, data: dict, repository: SQLAlchemyRepository) -> "Country | None":
        """Update an existing country"""
        country = repository.get(Country, code)

        if not country:
            return None

        if 'name' in data:
            country.name = data['name']

        repository.commit()
        return country

    @staticmethod
    def delete(code: str, repository: SQLAlchemyRepository) -> bool:
        """Delete a country by code"""
        country = repository.get(Country, code)

        if not country:
            return False

        repository.delete(country)
        repository.commit()
        return True
