from fastapi import APIRouter, Depends, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from gestion_des_approvisionnements.database import get_db
from gestion_des_approvisionnements.schemas import ProduitCreate, ProduitUpdate, ProduitResponse, StockOperation
from gestion_des_approvisionnements.services.produit_service import produit_service
from gestion_des_approvisionnements.auth import get_current_user
from gestion_des_approvisionnements.models import User

router = APIRouter(prefix="/api/produits", tags=["Produits"])


@router.post(
    "/",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un nouveau produit avec image"
)
async def create_produit(
    libelle: str = Form(...),
    prix_unitaire: float = Form(..., gt=0),
    quantite_stock: Optional[int] = Form(0, ge=0),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Créer un nouveau produit avec upload d'image sur Cloudinary.
    
    - **libelle**: Nom du produit
    - **prix_unitaire**: Prix unitaire (doit être positif)
    - **quantite_stock**: Quantité en stock (optionnel, par défaut 0)
    - **image**: Fichier image (optionnel)
    """
    produit_data = ProduitCreate(
        libelle=libelle,
        prix_unitaire=prix_unitaire,
        quantite_stock=quantite_stock
    )
    
    produit = await produit_service.create_produit(db, produit_data, image)
    return {
        "success": True,
        "message": "Produit créé avec succès",
        "data": ProduitResponse.model_validate(produit)
    }


@router.get(
    "/",
    response_model=dict,
    summary="Récupérer tous les produits"
)
def get_all_produits(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer la liste de tous les produits."""
    produits = produit_service.get_all_produits(db)
    return {
        "success": True,
        "data": [ProduitResponse.model_validate(p) for p in produits]
    }


@router.get(
    "/{produit_id}",
    response_model=dict,
    summary="Récupérer un produit par son ID"
)
def get_produit_by_id(
    produit_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les détails d'un produit spécifique."""
    produit = produit_service.get_produit_by_id(db, produit_id)
    return {
        "success": True,
        "data": ProduitResponse.model_validate(produit)
    }


@router.put(
    "/{produit_id}",
    response_model=dict,
    summary="Modifier un produit"
)
async def update_produit(
    produit_id: str,
    libelle: Optional[str] = Form(None),
    prix_unitaire: Optional[float] = Form(None, gt=0),
    quantite_stock: Optional[int] = Form(None, ge=0),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Mettre à jour les informations d'un produit.
    
    Tous les champs sont optionnels. Si une nouvelle image est fournie,
    l'ancienne sera supprimée de Cloudinary.
    """
    produit_data = ProduitUpdate(
        libelle=libelle,
        prix_unitaire=prix_unitaire,
        quantite_stock=quantite_stock
    )
    
    produit = await produit_service.update_produit(db, produit_id, produit_data, image)
    return {
        "success": True,
        "message": "Produit mis à jour avec succès",
        "data": ProduitResponse.model_validate(produit)
    }


@router.delete(
    "/{produit_id}",
    response_model=dict,
    summary="Supprimer un produit"
)
def delete_produit(
    produit_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Supprimer un produit de la base de données et son image de Cloudinary."""
    produit_service.delete_produit(db, produit_id)
    return {
        "success": True,
        "message": "Produit supprimé avec succès"
    }


@router.patch(
    "/{produit_id}/increment",
    response_model=dict,
    summary="Incrémenter le stock d'un produit"
)
def increment_stock(
    produit_id: str,
    stock_data: StockOperation,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Augmenter la quantité en stock d'un produit.
    
    - **quantite**: Quantité à ajouter (doit être positive)
    """
    produit = produit_service.increment_stock(db, produit_id, stock_data.quantite)
    return {
        "success": True,
        "message": "Stock incrémenté avec succès",
        "data": ProduitResponse.model_validate(produit)
    }


@router.patch(
    "/{produit_id}/decrement",
    response_model=dict,
    summary="Décrémenter le stock d'un produit"
)
def decrement_stock(
    produit_id: str,
    stock_data: StockOperation,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Diminuer la quantité en stock d'un produit.
    
    - **quantite**: Quantité à retirer (doit être positive)
    
    Le stock ne peut jamais être négatif. Une erreur 400 sera retournée
    si la quantité demandée est supérieure au stock disponible.
    """
    produit = produit_service.decrement_stock(db, produit_id, stock_data.quantite)
    return {
        "success": True,
        "message": "Stock décrémenté avec succès",
        "data": ProduitResponse.model_validate(produit)
    }
