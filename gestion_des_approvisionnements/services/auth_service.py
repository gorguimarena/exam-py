from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from gestion_des_approvisionnements.schemas import UserCreate, UserLogin, UserResponse, Token
from gestion_des_approvisionnements.repositories.user_repo import user_repository
from gestion_des_approvisionnements.auth import get_password_hash, verify_password, create_access_token


class AuthService:
    """Service pour gérer l'authentification"""
    
    @staticmethod
    def register(db: Session, user_data: UserCreate) -> dict:
        """Inscrire un nouvel utilisateur"""
        # Vérifier si l'utilisateur existe déjà
        if user_repository.exists(db, user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Un utilisateur avec cet email existe déjà"
            )
        
        # Hasher le mot de passe
        hashed_password = get_password_hash(user_data.password)
        
        # Créer l'utilisateur
        user_dict = user_data.model_dump()
        user_dict['password'] = hashed_password
        
        user = user_repository.create(db, user_dict)
        
        # Générer le token
        access_token = create_access_token(data={"sub": user.email})
        
        return {
            "user": UserResponse.model_validate(user),
            "token": access_token
        }
    
    @staticmethod
    def login(db: Session, login_data: UserLogin) -> dict:
        """Connecter un utilisateur"""
        # Trouver l'utilisateur
        user = user_repository.get_by_email(db, login_data.email)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou mot de passe incorrect"
            )
        
        # Vérifier le mot de passe
        if not verify_password(login_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou mot de passe incorrect"
            )
        
        # Générer le token
        access_token = create_access_token(data={"sub": user.email})
        
        return {
            "user": UserResponse.model_validate(user),
            "token": access_token
        }


auth_service = AuthService()
