from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from gestion_des_approvisionnements.models import Fournisseur
from gestion_des_approvisionnements.schemas import FournisseurCreate, FournisseurUpdate, FournisseurResponse
from gestion_des_approvisionnements.repositories.fournisseur_repo import fournisseur_repository


class FournisseurService:
    """Service pour gérer les fournisseurs"""
    
    @staticmethod
    def create_fournisseur(db: Session, fournisseur_data: FournisseurCreate) -> Fournisseur:
        """Créer un nouveau fournisseur"""
        return fournisseur_repository.create(db, fournisseur_data)
    
    @staticmethod
    def get_all_fournisseurs(db: Session) -> List[Fournisseur]:
        """Récupérer tous les fournisseurs"""
        return fournisseur_repository.get_all(db)
    
    @staticmethod
    def get_fournisseur_by_id(db: Session, fournisseur_id: str) -> Fournisseur:
        """Récupérer un fournisseur par son ID"""
        fournisseur = fournisseur_repository.get_by_id(db, fournisseur_id)
        
        if not fournisseur:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fournisseur non trouvé"
            )
        
        return fournisseur
    
    @staticmethod
    def update_fournisseur(db: Session, fournisseur_id: str, fournisseur_data: FournisseurUpdate) -> Fournisseur:
        """Mettre à jour un fournisseur"""
        fournisseur = fournisseur_repository.get_by_id(db, fournisseur_id)
        
        if not fournisseur:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fournisseur non trouvé"
            )
        
        return fournisseur_repository.update(db, fournisseur, fournisseur_data)
    
    @staticmethod
    def delete_fournisseur(db: Session, fournisseur_id: str) -> None:
        """Supprimer un fournisseur"""
        fournisseur = fournisseur_repository.get_by_id(db, fournisseur_id)
        
        if not fournisseur:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fournisseur non trouvé"
            )
        
        fournisseur_repository.delete(db, fournisseur)


fournisseur_service = FournisseurService()
