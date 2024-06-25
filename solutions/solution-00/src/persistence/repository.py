from src.models.base import Base
from src.persistence.repository import Repository
from src.persistence import db

class SQLAlchemyRepository(Repository):
    def __init__(self):
        pass
    """SQLAlchemy DB repository"""

    def get_all(self, model_name: str) -> list:
        """Get all objects of a given model"""
        model_class = Base._decl_class_registry.get(model_name)
        return model_class.query.all() if model_class else []

    def get(self, model_name: str, obj_id: str) -> Base | None:
        """Get an object by its ID"""
        model_class = Base._decl_class_registry.get(model_name)
        return model_class.query.get(obj_id) if model_class else None

    def reload(self) -> None:
        """No need for reload in DB"""
        pass

    def save(self, obj: Base) -> None:
        """Save an object"""
        db.session.add(obj)
        db.session.commit()

    def update(self, obj: Base) -> Base | None:
        """Update an object"""
        db.session.commit()
        return obj

    def delete(self, obj: Base) -> bool:
        """Delete an object"""
        db.session.delete(obj)
        db.session.commit()
        return True
