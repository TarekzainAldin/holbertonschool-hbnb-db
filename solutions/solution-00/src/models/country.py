from sqlalchemy import Column, String
from src.models.base import Base

class Country(Base):
    __tablename__ = 'countries'

    code = Column(String, primary_key=True)
    name = Column(String, nullable=False)

    def __init__(self, name: str, code: str, **kw) -> None:
        super().__init__(**kw)
        self.name = name
        self.code = code

    def __repr__(self) -> str:
        return f"<Country {self.code} ({self.name})>"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "code": self.code,
        }

    @staticmethod
    def get_all() -> list["Country"]:
        from src.persistence import repo
        return repo.session.query(Country).all()

    @staticmethod
    def get(code: str) -> "Country | None":
        from src.persistence import repo
        return repo.session.query(Country).filter_by(code=code).first()

    @staticmethod
    def create(name: str, code: str) -> "Country":
        from src.persistence import repo

        new_country = Country(name=name, code=code)
        repo.session.add(new_country)
        repo.session.commit()

        return new_country
