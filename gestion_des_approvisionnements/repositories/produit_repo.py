from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from gestion_des_approvisionnements.models import Produit


class ProduitRepository:
    """Repository pour gérer les produits"""
    
    @staticmethod
    def create(db: Session, produit_data: dict) -> Produit:
        """Créer un nouveau produit"""
        produit = Produit(**produit_data)
        db.add(produit)
        db.commit()
        db.refresh(produit)
        return produit
    
    @staticmethod
    def get_all(db: Session) -> List[Produit]:
        """Récupérer tous les produits"""
        return db.query(Produit).order_by(Produit.created_at.desc()).all()
    
    @staticmethod
    def get_by_id(db: Session, produit_id: str) -> Optional[Produit]:
        """Récupérer un produit par son ID"""
        return db.query(Produit).filter(Produit.id == produit_id).first()
    
    @staticmethod
    def update(db: Session, produit: Produit, produit_data: dict) -> Produit:
        """Mettre à jour un produit"""
        for key, value in produit_data.items():
            if value is not None:
                setattr(produit, key, value)
        
        db.commit()
        db.refresh(produit)
        return produit
    
    @staticmethod
    def delete(db: Session, produit: Produit) -> None:
        """Supprimer un produit"""
        db.delete(produit)
        db.commit()
    
    @staticmethod
    def increment_stock(db: Session, produit: Produit, quantite: int) -> Produit:
        """Incrémenter le stock d'un produit"""
        produit.quantite_stock += quantite
        db.commit()
        db.refresh(produit)
        return produit
    
    @staticmethod
    def decrement_stock(db: Session, produit: Produit, quantite: int) -> Produit:
        """Décrémenter le stock d'un produit"""
        if produit.quantite_stock < quantite:
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuffisant. Stock disponible: {produit.quantite_stock}, Quantité demandée: {quantite}"
            )
        
        produit.quantite_stock -= quantite
        db.commit()
        db.refresh(produit)
        return produit
    
    @staticmethod
    def exists(db: Session, produit_id: str) -> bool:
        """Vérifier si un produit existe"""
        return db.query(Produit).filter(Produit.id == produit_id).count() > 0


produit_repository = ProduitRepository()
