from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from gestion_des_approvisionnements.models import Approvisionnement
from gestion_des_approvisionnements.schemas import ApprovisionnementCreate, ApprovisionnementUpdate
from gestion_des_approvisionnements.repositories.approvisionnement_repo import approvisionnement_repository
from gestion_des_approvisionnements.repositories.fournisseur_repo import fournisseur_repository
from gestion_des_approvisionnements.repositories.produit_repo import produit_repository


class ApprovisionnementService:
    """Service pour gérer les approvisionnements"""
    
    @staticmethod
    def create_approvisionnement(db: Session, appro_data: ApprovisionnementCreate) -> Approvisionnement:
        """
        Créer un nouvel approvisionnement et mettre à jour le stock automatiquement
        """
        # Vérifier que le fournisseur existe
        if not fournisseur_repository.exists(db, appro_data.fournisseur_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fournisseur non trouvé"
            )
        
        # Vérifier que le produit existe
        produit = produit_repository.get_by_id(db, appro_data.produit_id)
        if not produit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produit non trouvé"
            )
        
        try:
            # Créer l'approvisionnement
            appro_dict = appro_data.model_dump()
            approvisionnement = approvisionnement_repository.create(db, appro_dict)
            
            # Mettre à jour le stock du produit
            produit_repository.increment_stock(db, produit, appro_data.quantite)
            
            # Rafraîchir pour obtenir les relations
            db.refresh(approvisionnement)
            
            return approvisionnement
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erreur lors de la création de l'approvisionnement: {str(e)}"
            )
    
    @staticmethod
    def get_all_approvisionnements(db: Session) -> List[Approvisionnement]:
        """Récupérer tous les approvisionnements"""
        return approvisionnement_repository.get_all(db)
    
    @staticmethod
    def get_approvisionnement_by_id(db: Session, appro_id: str) -> Approvisionnement:
        """Récupérer un approvisionnement par son ID"""
        approvisionnement = approvisionnement_repository.get_by_id(db, appro_id)
        
        if not approvisionnement:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Approvisionnement non trouvé"
            )
        
        return approvisionnement
    
    @staticmethod
    def update_approvisionnement(
        db: Session,
        appro_id: str,
        appro_data: ApprovisionnementUpdate
    ) -> Approvisionnement:
        """Mettre à jour un approvisionnement"""
        approvisionnement = approvisionnement_repository.get_by_id(db, appro_id)
        
        if not approvisionnement:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Approvisionnement non trouvé"
            )
        
        # Vérifier que le fournisseur existe si fourni
        if appro_data.fournisseur_id and not fournisseur_repository.exists(db, appro_data.fournisseur_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fournisseur non trouvé"
            )
        
        # Vérifier que le produit existe si fourni
        if appro_data.produit_id and not produit_repository.exists(db, appro_data.produit_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produit non trouvé"
            )
        
        return approvisionnement_repository.update(db, approvisionnement, appro_data)
    
    @staticmethod
    def delete_approvisionnement(db: Session, appro_id: str) -> None:
        """Supprimer un approvisionnement"""
        approvisionnement = approvisionnement_repository.get_by_id(db, appro_id)
        
        if not approvisionnement:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Approvisionnement non trouvé"
            )
        
        approvisionnement_repository.delete(db, approvisionnement)


approvisionnement_service = ApprovisionnementService()
