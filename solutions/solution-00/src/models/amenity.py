# src/models/amenity.py

from src.persistence import db
from src.models.base import Base
from src.persistence.sqlalchemy_repository import SQLAlchemyRepository

class Amenity(db.Model, Base):
    __tablename__ = 'amenity'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = name

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict, repository: SQLAlchemyRepository) -> "Amenity":
        amenity = Amenity(name=data['name'])
        repository.add(amenity)
        repository.commit()
        return amenity

    @staticmethod
    def update(amenity_id: str, data: dict, repository: SQLAlchemyRepository) -> "Amenity | None":
        amenity = repository.get(Amenity, amenity_id)
        if not amenity:
            return None
        if 'name' in data:
            amenity.name = data['name']
        repository.commit()
        return amenity

    @staticmethod
    def delete(amenity_id: str, repository: SQLAlchemyRepository) -> bool:
        amenity = repository.get(Amenity, amenity_id)
        if not amenity:
            return False
        repository.delete(amenity)
        repository.commit()
        return True

    @staticmethod
    def get(amenity_id: str, repository: SQLAlchemyRepository) -> "Amenity | None":
        return repository.get(Amenity, amenity_id)

    @staticmethod
    def get_all(repository: SQLAlchemyRepository) -> list["Amenity"]:
        return repository.all(Amenity)
