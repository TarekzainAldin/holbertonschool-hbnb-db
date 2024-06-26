from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.models.base import Base
from src.models.user import User
from src.models.place import Place

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(String, primary_key=True)
    place_id = Column(String, ForeignKey('places.id'), nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    comment = Column(String, nullable=False)
    rating = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    place = relationship("Place", backref="reviews")
    user = relationship("User", backref="reviews")

    def __init__(self, place_id: str, user_id: str, comment: str, rating: float, **kw) -> None:
        super().__init__(**kw)
        self.place_id = place_id
        self.user_id = user_id
        self.comment = comment
        self.rating = rating

    def __repr__(self) -> str:
        return f"<Review {self.id} - '{self.comment[:25]}...'>"

    def to_dict(self) -> dict:
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
    def create(data: dict) -> "Review":
        from src.persistence import repo

        user = User.get(data["user_id"])
        if not user:
            raise ValueError(f"User with ID {data['user_id']} not found")

        place = Place.get(data["place_id"])
        if not place:
            raise ValueError(f"Place with ID {data['place_id']} not found")

        new_review = Review(
            place_id=data["place_id"],
            user_id=data["user_id"],
            comment=data["comment"],
            rating=data["rating"]
        )

        repo.session.add(new_review)
        repo.session.commit()

        return new_review

    @staticmethod
    def update(review_id: str, data: dict) -> "Review | None":
        from src.persistence import repo

        review = Review.query.get(review_id)

        if not review:
            raise ValueError("Review not found")

        for key, value in data.items():
            setattr(review, key, value)

        repo.session.commit()

        return review
