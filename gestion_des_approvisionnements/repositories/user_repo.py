from typing import Optional
from sqlalchemy.orm import Session
from gestion_des_approvisionnements.models import User


class UserRepository:
    """Repository pour gérer les utilisateurs"""
    
    @staticmethod
    def create(db: Session, user_data: dict) -> User:
        """Créer un nouvel utilisateur"""
        user = User(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        """Récupérer un utilisateur par email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_by_id(db: Session, user_id: str) -> Optional[User]:
        """Récupérer un utilisateur par ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def exists(db: Session, email: str) -> bool:
        """Vérifier si un utilisateur existe"""
        return db.query(User).filter(User.email == email).count() > 0


user_repository = UserRepository()
