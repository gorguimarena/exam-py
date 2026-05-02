from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from gestion_des_approvisionnements.database import get_db
from gestion_des_approvisionnements.schemas import FournisseurCreate, FournisseurUpdate, FournisseurResponse
from gestion_des_approvisionnements.services.fournisseur_service import fournisseur_service
from gestion_des_approvisionnements.auth import get_current_user
from gestion_des_approvisionnements.models import User

router = APIRouter(prefix="/api/fournisseurs", tags=["Fournisseurs"])


@router.post(
    "/",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un nouveau fournisseur"
)
def create_fournisseur(
    fournisseur_data: FournisseurCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Créer un nouveau fournisseur.
    
    - **nom**: Nom du fournisseur
    - **telephone**: Numéro de téléphone
    - **adresse**: Adresse complète
    """
    fournisseur = fournisseur_service.create_fournisseur(db, fournisseur_data)
    return {
        "success": True,
        "message": "Fournisseur créé avec succès",
        "data": FournisseurResponse.model_validate(fournisseur)
    }


@router.get(
    "/",
    response_model=dict,
    summary="Récupérer tous les fournisseurs"
)
def get_all_fournisseurs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer la liste de tous les fournisseurs."""
    fournisseurs = fournisseur_service.get_all_fournisseurs(db)
    return {
        "success": True,
        "data": [FournisseurResponse.model_validate(f) for f in fournisseurs]
    }


@router.get(
    "/{fournisseur_id}",
    response_model=dict,
    summary="Récupérer un fournisseur par son ID"
)
def get_fournisseur_by_id(
    fournisseur_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les détails d'un fournisseur spécifique."""
    fournisseur = fournisseur_service.get_fournisseur_by_id(db, fournisseur_id)
    return {
        "success": True,
        "data": FournisseurResponse.model_validate(fournisseur)
    }


@router.put(
    "/{fournisseur_id}",
    response_model=dict,
    summary="Modifier un fournisseur"
)
def update_fournisseur(
    fournisseur_id: str,
    fournisseur_data: FournisseurUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Mettre à jour les informations d'un fournisseur.
    
    Tous les champs sont optionnels.
    """
    fournisseur = fournisseur_service.update_fournisseur(db, fournisseur_id, fournisseur_data)
    return {
        "success": True,
        "message": "Fournisseur mis à jour avec succès",
        "data": FournisseurResponse.model_validate(fournisseur)
    }


@router.delete(
    "/{fournisseur_id}",
    response_model=dict,
    summary="Supprimer un fournisseur"
)
def delete_fournisseur(
    fournisseur_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Supprimer un fournisseur de la base de données."""
    fournisseur_service.delete_fournisseur(db, fournisseur_id)
    return {
        "success": True,
        "message": "Fournisseur supprimé avec succès"
    }
