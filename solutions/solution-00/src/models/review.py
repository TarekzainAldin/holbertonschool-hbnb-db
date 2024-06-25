from src.persistence import db
from src.models.base import Base
from src.models.place import Place
from src.models.user import User
from src.persistence.sqlalchemy_repository import SQLAlchemyRepository


class Review(db.Model, Base):
    """Review representation"""

    __tablename__ = 'review'

    id = db.Column(db.String(36), primary_key=True)
    place_id = db.Column(db.String(36), db.ForeignKey('place.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)

    place = db.relationship('Place', backref=db.backref('reviews', lazy=True))
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))

    def __init__(self, place_id: str, user_id: str, comment: str, rating: float, **kwargs) -> None:
        """Constructor"""
        super().__init__(**kwargs)
        self.place_id = place_id
        self.user_id = user_id
        self.comment = comment
        self.rating = rating

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "place_id": self.place_id,
            "user_id": self.user_id,
            "comment": self.comment,
            "rating": self.rating,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict, repository: SQLAlchemyRepository) -> "Review":
        """Create a new review"""
        user = repository.get(User, data['user_id'])

        if not user:
            raise ValueError(f"User with ID {data['user_id']} not found")

        place = repository.get(Place, data['place_id'])

        if not place:
            raise ValueError(f"Place with ID {data['place_id']} not found")

        new_review = Review(
            place_id=data['place_id'])
