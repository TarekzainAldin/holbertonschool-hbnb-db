"""
  Now is easy to implement the database repository. The DBRepository
  should implement the Repository (Storage) interface and the methods defined
  in the abstract class Storage.

  The methods to implement are:
    - get_all
    - get
    - save
    - update
    - delete
    - reload (which can be empty)
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.models.base import Base
from src.persistence.repository import Repository

DATABASE_URL = "sqlite:///./test.db"  # Or your actual database URL

# Create the SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class DBRepository(Repository):
    """DB repository implementation using SQLAlchemy"""

    def __init__(self) -> None:
        """Initialize the DB repository with a session"""
        self.db: Session = next(get_db())

    def get_all(self, model_name: str) -> list:
        """Get all instances of a model"""
        model = self._get_model_class_by_name(model_name)
        return self.db.query(model).all()

    def get(self, model_name: str, obj_id: str) -> Base | None:
        """Get a single instance of a model by ID"""
        model = self._get_model_class_by_name(model_name)
        return self.db.query(model).filter(model.id == obj_id).first()

    def reload(self) -> None:
        """Reload the session (not implemented, as SQLAlchemy handles sessions)"""
        pass

    def save(self, obj: Base) -> None:
        """Save an instance to the database"""
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

    def update(self, obj: Base) -> Base | None:
        """Update an instance in the database"""
        self.db.merge(obj)
        self.db.commit()
        return obj

    def delete(self, obj: Base) -> bool:
        """Delete an instance from the database"""
        self.db.delete(obj)
        self.db.commit()
        return True

    def _get_model_class_by_name(self, model_name: str) -> type:
        """Helper method to get model class by its name"""
        from src.models import amenity, city, country, place, review, user
        model_classes = {
            "Amenity": amenity.Amenity,
            "City": city.City,
            "Country": country.Country,
            "Place": place.Place,
            "Review": review.Review,
            "User": user.User
        }
        return model_classes.get(model_name)

