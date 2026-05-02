from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from gestion_des_approvisionnements.database import get_db
from gestion_des_approvisionnements.schemas import UserCreate, UserLogin, UserResponse
from gestion_des_approvisionnements.services.auth_service import auth_service
from gestion_des_approvisionnements.auth import get_current_user
from gestion_des_approvisionnements.models import User

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un nouvel utilisateur"
)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Inscription d'un nouvel utilisateur.
    
    - **email**: Email de l'utilisateur
    - **password**: Mot de passe (minimum 6 caractères)
    - **nom**: Nom complet de l'utilisateur
    """
    result = auth_service.register(db, user_data)
    return {
        "success": True,
        "message": "Utilisateur créé avec succès",
        "data": result
    }


@router.post(
    "/login",
    response_model=dict,
    summary="Se connecter"
)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """
    Connexion d'un utilisateur.
    
    - **email**: Email de l'utilisateur
    - **password**: Mot de passe
    """
    result = auth_service.login(db, login_data)
    return {
        "success": True,
        "message": "Connexion réussie",
        "data": result
    }


@router.get(
    "/profile",
    response_model=dict,
    summary="Récupérer le profil utilisateur"
)
def get_profile(current_user: User = Depends(get_current_user)):
    """
    Récupérer le profil de l'utilisateur connecté.
    
    Nécessite un token JWT valide.
    """
    return {
        "success": True,
        "data": UserResponse.model_validate(current_user)
    }
