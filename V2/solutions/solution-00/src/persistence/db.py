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

from src.models.base import Base
from src.persistence.repository import Repository
from src.__init__ import db
from src.__init__ import app
from src.__init__ import db_session

class DBRepository(Repository):
    """Dummy DB repository"""

    def __init__(self) -> None:
        """Initialisation du repository"""
        self.session = db_session

    def get_all(self, model_name: str) -> list:
        """Récupère tous les objets d'un modèle donné"""
        model = self._get_model_class(model_name)
        return self.session.query(model).all()

    def get(self, model_name: str, obj_id: str) -> Base | None:
        """Récupère un objet par son identifiant"""
        model = self._get_model_class(model_name)
        return self.session.query(model).get(obj_id)

    def reload(self) -> None:
        """Not implemented"""

    def save(self, obj: Base) -> None:
        """Not implemented"""

    def update(self, obj: Base) -> Base | None:
        """Sauvegarde un objet dans la base de données"""
        self.session.add(obj)
        self.session.commit()

    def update(self, obj: Base) -> Base | None:
        """Met à jour un objet dans la base de données"""
        self.session.merge(obj)
        self.session.commit()
        return obj

    def delete(self, obj: Base) -> bool:
        """Supprime un objet de la base de données"""
        self.session.delete(obj)
        self.session.commit()
        return True

    def _get_model_class(self, model_name: str):
        """Obtient la classe de modèle à partir de son nom"""
        # Assurez-vous d'importer ou de référencer toutes les classes de modèle disponibles
        if model_name == 'User':
            from src.models.user import User
            return User
        # Ajoutez d'autres modèles ici selon vos besoins
        raise ValueError(f"Modèle inconnu : {model_name}")

class DataManager:
    def save_user(self, user):
        if app.config['USE_DATABASE']:
            db.session.add(user)
            db.session.commit()
        else:
            # Implement file-based save logic
            pass
