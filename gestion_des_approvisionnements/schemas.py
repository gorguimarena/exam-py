from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


# Schémas User
class UserBase(BaseModel):
    email: EmailStr
    nom: str


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: str
    role: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# Schémas Fournisseur
class FournisseurBase(BaseModel):
    nom: str
    telephone: str
    adresse: str


class FournisseurCreate(FournisseurBase):
    pass


class FournisseurUpdate(BaseModel):
    nom: Optional[str] = None
    telephone: Optional[str] = None
    adresse: Optional[str] = None


class FournisseurResponse(FournisseurBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Schémas Produit
class ProduitBase(BaseModel):
    libelle: str
    prix_unitaire: float = Field(..., gt=0)
    quantite_stock: Optional[int] = Field(default=0, ge=0)


class ProduitCreate(ProduitBase):
    pass


class ProduitUpdate(BaseModel):
    libelle: Optional[str] = None
    prix_unitaire: Optional[float] = Field(None, gt=0)
    quantite_stock: Optional[int] = Field(None, ge=0)


class ProduitResponse(ProduitBase):
    id: str
    image: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class StockOperation(BaseModel):
    quantite: int = Field(..., gt=0)


# Schémas Approvisionnement
class ApprovisionnementBase(BaseModel):
    quantite: int = Field(..., gt=0)
    fournisseur_id: str
    produit_id: str
    date: Optional[datetime] = None


class ApprovisionnementCreate(ApprovisionnementBase):
    pass


class ApprovisionnementUpdate(BaseModel):
    quantite: Optional[int] = Field(None, gt=0)
    fournisseur_id: Optional[str] = None
    produit_id: Optional[str] = None
    date: Optional[datetime] = None


class ApprovisionnementResponse(BaseModel):
    id: str
    date: datetime
    quantite: int
    fournisseur_id: str
    produit_id: str
    fournisseur: FournisseurResponse
    produit: ProduitResponse
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Schémas de réponse génériques
class SuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[dict] = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    details: Optional[dict] = None
