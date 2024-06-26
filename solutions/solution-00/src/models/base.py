from datetime import datetime
from typing import Any, Optional
import uuid
from abc import ABC, abstractmethod
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Session

@as_declarative()
class Base(ABC):
    """
    Base Interface for all models
    """

    id: str = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs) -> None:
        """
        Base class constructor
        If kwargs are provided, set them as attributes
        """

        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def get(cls, session: Session, id: str) -> "Any | None":
        """
        This is a common method to get a specific object
        of a class by its id

        If a class needs a different implementation,
        it should override this method
        """
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def get_all(cls, session: Session) -> list["Any"]:
        """
        This is a common method to get all objects of a class

        If a class needs a different implementation,
        it should override this method
        """
        return session.query(cls).all()

    @classmethod
    def delete(cls, session: Session, id: str) -> bool:
        """
        This is a common method to delete a specific
        object of a class by its id

        If a class needs a different implementation,
        it should override this method
        """
        obj = cls.get(session, id)

        if not obj:
            return False

        session.delete(obj)
        session.commit()
        return True

    @abstractmethod
    def to_dict(self) -> dict:
        """Returns the dictionary representation of the object"""

    @staticmethod
    @abstractmethod
    def create(session: Session, data: dict) -> Any:
        """Creates a new object of the class"""

    @staticmethod
    @abstractmethod
    def update(session: Session, entity_id: str, data: dict) -> Any | None:
        """Updates an object of the class"""
