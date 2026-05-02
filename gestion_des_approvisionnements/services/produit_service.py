from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional
from gestion_des_approvisionnements.models import Produit
from gestion_des_approvisionnements.schemas import ProduitCreate, ProduitUpdate
from gestion_des_approvisionnements.repositories.produit_repo import produit_repository
from gestion_des_approvisionnements.services.cloudinary_service import cloudinary_service


class ProduitService:
    """Service pour gérer les produits"""
    
    @staticmethod
    async def create_produit(
        db: Session,
        produit_data: ProduitCreate,
        file: Optional[UploadFile] = None
    ) -> Produit:
        """Créer un nouveau produit"""
        image_url = None
        
        # Upload de l'image si fournie
        if file:
            image_url = await cloudinary_service.upload_image(file)
        
        produit_dict = produit_data.model_dump()
        produit_dict['image'] = image_url
        
        return produit_repository.create(db, produit_dict)
    
    @staticmethod
    def get_all_produits(db: Session) -> List[Produit]:
        """Récupérer tous les produits"""
        return produit_repository.get_all(db)
    
    @staticmethod
    def get_produit_by_id(db: Session, produit_id: str) -> Produit:
        """Récupérer un produit par son ID"""
        produit = produit_repository.get_by_id(db, produit_id)
        
        if not produit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produit non trouvé"
            )
        
        return produit
    
    @staticmethod
    async def update_produit(
        db: Session,
        produit_id: str,
        produit_data: ProduitUpdate,
        file: Optional[UploadFile] = None
    ) -> Produit:
        """Mettre à jour un produit"""
        produit = produit_repository.get_by_id(db, produit_id)
        
        if not produit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produit non trouvé"
            )
        
        update_dict = produit_data.model_dump(exclude_unset=True)
        
        # Upload de la nouvelle image si fournie
        if file:
            # Supprimer l'ancienne image
            if produit.image:
                cloudinary_service.delete_image(produit.image)
            
            image_url = await cloudinary_service.upload_image(file)
            update_dict['image'] = image_url
        
        return produit_repository.update(db, produit, update_dict)
    
    @staticmethod
    def delete_produit(db: Session, produit_id: str) -> None:
        """Supprimer un produit"""
        produit = produit_repository.get_by_id(db, produit_id)
        
        if not produit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produit non trouvé"
            )
        
        # Supprimer l'image de Cloudinary
        if produit.image:
            cloudinary_service.delete_image(produit.image)
        
        produit_repository.delete(db, produit)
    
    @staticmethod
    def increment_stock(db: Session, produit_id: str, quantite: int) -> Produit:
        """Incrémenter le stock d'un produit"""
        produit = produit_repository.get_by_id(db, produit_id)
        
        if not produit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produit non trouvé"
            )
        
        return produit_repository.increment_stock(db, produit, quantite)
    
    @staticmethod
    def decrement_stock(db: Session, produit_id: str, quantite: int) -> Produit:
        """Décrémenter le stock d'un produit"""
        produit = produit_repository.get_by_id(db, produit_id)
        
        if not produit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produit non trouvé"
            )
        
        return produit_repository.decrement_stock(db, produit, quantite)


produit_service = ProduitService()
