from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from gestion_des_approvisionnements.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    nom = Column(String, nullable=False)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Fournisseur(Base):
    __tablename__ = "fournisseurs"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    nom = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
    adresse = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    approvisionnements = relationship("Approvisionnement", back_populates="fournisseur", cascade="all, delete-orphan")


class Produit(Base):
    __tablename__ = "produits"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    libelle = Column(String, nullable=False)
    prix_unitaire = Column(Float, nullable=False)
    quantite_stock = Column(Integer, default=0)
    image = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    approvisionnements = relationship("Approvisionnement", back_populates="produit", cascade="all, delete-orphan")


class Approvisionnement(Base):
    __tablename__ = "approvisionnements"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    date = Column(DateTime, default=datetime.utcnow)
    quantite = Column(Integer, nullable=False)
    fournisseur_id = Column(String, ForeignKey("fournisseurs.id", ondelete="CASCADE"), nullable=False)
    produit_id = Column(String, ForeignKey("produits.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    fournisseur = relationship("Fournisseur", back_populates="approvisionnements")
    produit = relationship("Produit", back_populates="approvisionnements")
