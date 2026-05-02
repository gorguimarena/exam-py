from typing import List, Optional
from sqlalchemy.orm import Session
from gestion_des_approvisionnements.models import Approvisionnement
from gestion_des_approvisionnements.schemas import ApprovisionnementUpdate


class ApprovisionnementRepository:
    """Repository pour gérer les approvisionnements"""
    
    @staticmethod
    def create(db: Session, appro_data: dict) -> Approvisionnement:
        """Créer un nouvel approvisionnement"""
        approvisionnement = Approvisionnement(**appro_data)
        db.add(approvisionnement)
        db.commit()
        db.refresh(approvisionnement)
        return approvisionnement
    
    @staticmethod
    def get_all(db: Session) -> List[Approvisionnement]:
        """Récupérer tous les approvisionnements"""
        return db.query(Approvisionnement).order_by(Approvisionnement.date.desc()).all()
    
    @staticmethod
    def get_by_id(db: Session, appro_id: str) -> Optional[Approvisionnement]:
        """Récupérer un approvisionnement par son ID"""
        return db.query(Approvisionnement).filter(Approvisionnement.id == appro_id).first()
    
    @staticmethod
    def update(db: Session, appro: Approvisionnement, appro_data: ApprovisionnementUpdate) -> Approvisionnement:
        """Mettre à jour un approvisionnement"""
        update_data = appro_data.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(appro, key, value)
        
        db.commit()
        db.refresh(appro)
        return appro
    
    @staticmethod
    def delete(db: Session, appro: Approvisionnement) -> None:
        """Supprimer un approvisionnement"""
        db.delete(appro)
        db.commit()
    
    @staticmethod
    def exists(db: Session, appro_id: str) -> bool:
        """Vérifier si un approvisionnement existe"""
        return db.query(Approvisionnement).filter(Approvisionnement.id == appro_id).count() > 0


approvisionnement_repository = ApprovisionnementRepository()
