"""
Seed script to initialize the database with sample data
Run with: python seed.py
"""
from gestion_des_approvisionnements.database import SessionLocal, engine, Base
from gestion_des_approvisionnements.models import User, Fournisseur, Produit, Approvisionnement
from gestion_des_approvisionnements.auth import get_password_hash
from datetime import datetime, timedelta
import uuid


def generate_uuid():
    return str(uuid.uuid4())


def seed_users(db):
    """Create default users"""
    users_data = [
        {
            "email": "admin@examen.com",
            "password": "admin123",
            "nom": "Administrateur",
            "role": "admin"
        },
        {
            "email": "user@examen.com",
            "password": "user123",
            "nom": "Utilisateur Test",
            "role": "user"
        }
    ]
    
    for user_data in users_data:
        existing_user = db.query(User).filter(User.email == user_data["email"]).first()
        if not existing_user:
            user = User(
                id=generate_uuid(),
                email=user_data["email"],
                password=get_password_hash(user_data["password"]),
                nom=user_data["nom"],
                role=user_data["role"],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(user)
            print(f"Created user: {user_data['email']}")
        else:
            print(f"User already exists: {user_data['email']}")
    
    db.commit()


def seed_fournisseurs(db):
    """Create sample fournisseurs"""
    fournisseurs_data = [
        {
            "nom": "Samsung Electronics",
            "telephone": "+33 1 23 45 67 89",
            "adresse": "15 Avenue de lOpéra, 75001 Paris, France"
        },
        {
            "nom": "Apple Inc.",
            "telephone": "+33 1 40 08 44 00",
            "adresse": "40 Rue de Bercy, 75012 Paris, France"
        },
        {
            "nom": "Sony Corporation",
            "telephone": "+33 1 55 26 00 00",
            "adresse": "20 Rue Quentin, 92100 Boulogne-Billancourt, France"
        },
        {
            "nom": "LG Electronics",
            "telephone": "+33 1 46 09 00 00",
            "adresse": "17 Avenue des Champs-Élysées, 75008 Paris, France"
        },
        {
            "nom": "Xiaomi Technology",
            "telephone": "+33 1 83 63 00 00",
            "adresse": "25 Rue de la Victoire, 75009 Paris, France"
        }
    ]
    
    created_fournisseurs = []
    for fournisseur_data in fournisseurs_data:
        existing = db.query(Fournisseur).filter(Fournisseur.nom == fournisseur_data["nom"]).first()
        if not existing:
            fournisseur = Fournisseur(
                id=generate_uuid(),
                nom=fournisseur_data["nom"],
                telephone=fournisseur_data["telephone"],
                adresse=fournisseur_data["adresse"],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(fournisseur)
            db.flush()
            created_fournisseurs.append(fournisseur)
            print(f"Created fournisseur: {fournisseur_data['nom']}")
        else:
            created_fournisseurs.append(existing)
            print(f"Fournisseur already exists: {fournisseur_data['nom']}")
    
    db.commit()
    return created_fournisseurs


def seed_produits(db):
    """Create sample produits"""
    produits_data = [
        {
            "libelle": "Samsung Galaxy S24",
            "prix_unitaire": 899.99,
            "quantite_stock": 50,
            "image": "https://example.com/galaxy-s24.jpg"
        },
        {
            "libelle": "iPhone 15 Pro",
            "prix_unitaire": 1199.99,
            "quantite_stock": 30,
            "image": "https://example.com/iphone15.jpg"
        },
        {
            "libelle": "Sony PlayStation 5",
            "prix_unitaire": 549.99,
            "quantite_stock": 25,
            "image": "https://example.com/ps5.jpg"
        },
        {
            "libelle": "LG OLED TV 55 pouces",
            "prix_unitaire": 1299.99,
            "quantite_stock": 15,
            "image": "https://example.com/lg-oled.jpg"
        },
        {
            "libelle": "Xiaomi Redmi Note 13",
            "prix_unitaire": 299.99,
            "quantite_stock": 100,
            "image": "https://example.com/redmi-note.jpg"
        },
        {
            "libelle": "Samsung TV QLED 65 pouces",
            "prix_unitaire": 1499.99,
            "quantite_stock": 20,
            "image": "https://example.com/samsung-qled.jpg"
        },
        {
            "libelle": "AirPods Pro 2",
            "prix_unitaire": 249.99,
            "quantite_stock": 75,
            "image": "https://example.com/airpods.jpg"
        },
        {
            "libelle": "Sony WH-1000XM5",
            "prix_unitaire": 379.99,
            "quantite_stock": 40,
            "image": "https://example.com/sony-headphones.jpg"
        }
    ]
    
    created_produits = []
    for produit_data in produits_data:
        existing = db.query(Produit).filter(Produit.libelle == produit_data["libelle"]).first()
        if not existing:
            produit = Produit(
                id=generate_uuid(),
                libelle=produit_data["libelle"],
                prix_unitaire=produit_data["prix_unitaire"],
                quantite_stock=produit_data["quantite_stock"],
                image=produit_data["image"],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(produit)
            db.flush()
            created_produits.append(produit)
            print(f"Created produit: {produit_data['libelle']}")
        else:
            created_produits.append(existing)
            print(f"Produit already exists: {produit_data['libelle']}")
    
    db.commit()
    return created_produits


def seed_approvisionnements(db, fournisseurs, produits):
    """Create sample approvisionnements"""
    if not fournisseurs or not produits:
        print("No fournisseurs or produits found. Run seed_fournisseurs and seed_produits first.")
        return
    
    # Create sample approvisionnements linking specific produits to fournisseurs
    approvisionnements_data = [
        {"fournisseur_index": 0, "produit_index": 0, "quantite": 20},   # Samsung -> Galaxy S24
        {"fournisseur_index": 1, "produit_index": 1, "quantite": 15},   # Apple -> iPhone 15 Pro
        {"fournisseur_index": 2, "produit_index": 2, "quantite": 10},   # Sony -> PS5
        {"fournisseur_index": 3, "produit_index": 3, "quantite": 8},    # LG -> LG OLED TV
        {"fournisseur_index": 4, "produit_index": 4, "quantite": 50},   # Xiaomi -> Redmi Note 13
        {"fournisseur_index": 0, "produit_index": 5, "quantite": 12},   # Samsung -> Samsung TV QLED
        {"fournisseur_index": 1, "produit_index": 6, "quantite": 30},   # Apple -> AirPods
        {"fournisseur_index": 2, "produit_index": 7, "quantite": 20},   # Sony -> Sony Headphones
    ]
    
    for appro_data in approvisionnements_data:
        fournisseur = fournisseurs[appro_data["fournisseur_index"]]
        produit = produits[appro_data["produit_index"]]
        
        # Check if approvisionnement already exists
        existing = db.query(Approvisionnement).filter(
            Approvisionnement.fournisseur_id == fournisseur.id,
            Approvisionnement.produit_id == produit.id
        ).first()
        
        if not existing:
            approvisionnement = Approvisionnement(
                id=generate_uuid(),
                date=datetime.utcnow() - timedelta(days=appro_data["fournisseur_index"]),
                quantite=appro_data["quantite"],
                fournisseur_id=fournisseur.id,
                produit_id=produit.id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(approvisionnement)
            print(f"Created approvisionnement: {produit.libelle} from {fournisseur.nom}")
        else:
            print(f"Approvisionnement already exists: {produit.libelle} from {fournisseur.nom}")
    
    db.commit()


def main():
    """Main function to seed the database"""
    print("=" * 50)
    print("Starting database seeding...")
    print("=" * 50)
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    print("Tables created/verified.")
    
    # Create a session
    db = SessionLocal()
    
    try:
        # Seed data
        seed_users(db)
        fournisseurs = seed_fournisseurs(db)
        produits = seed_produits(db)
        seed_approvisionnements(db, fournisseurs, produits)
        
        print("=" * 50)
        print("Database seeding completed successfully!")
        print("=" * 50)
        
        # Print login credentials
        print("\nLogin credentials:")
        print("  Admin:  admin@examen.com / admin123")
        print("  User:   user@examen.com / user123")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
