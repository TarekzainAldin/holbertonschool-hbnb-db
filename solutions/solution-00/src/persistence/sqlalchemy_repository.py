# # src/persistence/sqlalchemy_repository.py

# from src.models.base import Base
# from src import db
# from datetime import datetime
# from src.persistence.repository import Repository

# # 
# from src.persistence.repository import Repository

# class SQLAlchemyRepository(Repository):
#     def __init__(self):
#         pass

#     def all(self, model_cls):
#         return model_cls.query.all()

#     def get(self, model_cls, obj_id):
#         return model_cls.query.get(obj_id)

#     def add(self, obj):
#         from src import db
#         db.session.add(obj)

#     def commit(self):
#         from src import db
#         db.session.commit()

#     def delete(self, obj):
#         from src import db
#         db.session.delete(obj)
#         db.session.commit()

# src/persistence/sqlalchemy_repository.py

from src import db

class SQLAlchemyRepository:
    def all(self, model_cls):
        return model_cls.query.all()

    def get(self, model_cls, obj_id):
        return model_cls.query.get(obj_id)

    def add(self, obj):
        db.session.add(obj)

    def commit(self):
        db.session.commit()

    def delete(self, obj):
        db.session.delete(obj)
        db.session.commit()
