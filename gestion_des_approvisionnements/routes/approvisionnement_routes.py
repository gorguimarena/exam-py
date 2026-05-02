from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from gestion_des_approvisionnements.database import get_db
from gestion_des_approvisionnements.schemas import ApprovisionnementCreate, ApprovisionnementUpdate, ApprovisionnementResponse
from gestion_des_approvisionnements.services.approvisionnement_service import approvisionnement_service
from gestion_des_approvisionnements.auth import get_current_user
from gestion_des_approvisionnements.models import User

router = APIRouter(prefix="/api/approvisionnements", tags=["Approvisionnements"])


@router.post(
    "/",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un nouvel approvisionnement"
)
def create_approvisionnement(
    appro_data: ApprovisionnementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Créer un nouvel approvisionnement et mettre à jour le stock automatiquement.
    
    - **quantite**: Quantité à approvisionner (doit être positive)
    - **fournisseur_id**: ID du fournisseur
    - **produit_id**: ID du produit
    - **date**: Date de l'approvisionnement (optionnel, par défaut maintenant)
    
    Le stock du produit sera automatiquement augmenté de la quantité indiquée.
    """
    approvisionnement = approvisionnement_service.create_approvisionnement(db, appro_data)
    return {
        "success": True,
        "message": "Approvisionnement créé avec succès et stock mis à jour",
        "data": ApprovisionnementResponse.model_validate(approvisionnement)
    }


@router.get(
    "/",
    response_model=dict,
    summary="Récupérer tous les approvisionnements"
)
def get_all_approvisionnements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer la liste de tous les approvisionnements avec les détails du fournisseur et du produit."""
    approvisionnements = approvisionnement_service.get_all_approvisionnements(db)
    return {
        "success": True,
        "data": [ApprovisionnementResponse.model_validate(a) for a in approvisionnements]
    }


@router.get(
    "/{appro_id}",
    response_model=dict,
    summary="Récupérer un approvisionnement par son ID"
)
def get_approvisionnement_by_id(
    appro_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les détails d'un approvisionnement spécifique."""
    approvisionnement = approvisionnement_service.get_approvisionnement_by_id(db, appro_id)
    return {
        "success": True,
        "data": ApprovisionnementResponse.model_validate(approvisionnement)
    }


@router.put(
    "/{appro_id}",
    response_model=dict,
    summary="Modifier un approvisionnement"
)
def update_approvisionnement(
    appro_id: str,
    appro_data: ApprovisionnementUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Mettre à jour les informations d'un approvisionnement.
    
    Tous les champs sont optionnels.
    """
    approvisionnement = approvisionnement_service.update_approvisionnement(db, appro_id, appro_data)
    return {
        "success": True,
        "message": "Approvisionnement mis à jour avec succès",
        "data": ApprovisionnementResponse.model_validate(approvisionnement)
    }


@router.delete(
    "/{appro_id}",
    response_model=dict,
    summary="Supprimer un approvisionnement"
)
def delete_approvisionnement(
    appro_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Supprimer un approvisionnement de la base de données."""
    approvisionnement_service.delete_approvisionnement(db, appro_id)
    return {
        "success": True,
        "message": "Approvisionnement supprimé avec succès"
    }
