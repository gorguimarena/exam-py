from typing import List, Optional
from sqlalchemy.orm import Session
from gestion_des_approvisionnements.models import Fournisseur
from gestion_des_approvisionnements.schemas import FournisseurCreate, FournisseurUpdate


class FournisseurRepository:
    """Repository pour gérer les fournisseurs"""
    
    @staticmethod
    def create(db: Session, fournisseur_data: FournisseurCreate) -> Fournisseur:
        """Créer un nouveau fournisseur"""
        fournisseur = Fournisseur(**fournisseur_data.model_dump())
        db.add(fournisseur)
        db.commit()
        db.refresh(fournisseur)
        return fournisseur
    
    @staticmethod
    def get_all(db: Session) -> List[Fournisseur]:
        """Récupérer tous les fournisseurs"""
        return db.query(Fournisseur).order_by(Fournisseur.created_at.desc()).all()
    
    @staticmethod
    def get_by_id(db: Session, fournisseur_id: str) -> Optional[Fournisseur]:
        """Récupérer un fournisseur par son ID"""
        return db.query(Fournisseur).filter(Fournisseur.id == fournisseur_id).first()
    
    @staticmethod
    def update(db: Session, fournisseur: Fournisseur, fournisseur_data: FournisseurUpdate) -> Fournisseur:
        """Mettre à jour un fournisseur"""
        update_data = fournisseur_data.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(fournisseur, key, value)
        
        db.commit()
        db.refresh(fournisseur)
        return fournisseur
    
    @staticmethod
    def delete(db: Session, fournisseur: Fournisseur) -> None:
        """Supprimer un fournisseur"""
        db.delete(fournisseur)
        db.commit()
    
    @staticmethod
    def exists(db: Session, fournisseur_id: str) -> bool:
        """Vérifier si un fournisseur existe"""
        return db.query(Fournisseur).filter(Fournisseur.id == fournisseur_id).count() > 0


fournisseur_repository = FournisseurRepository()
