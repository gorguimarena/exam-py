# 🐍 API RESTful Gestion des Approvisionnements - FastAPI

API complète pour la gestion des approvisionnements d'une boutique avec **FastAPI**, **SQLAlchemy**, et **PostgreSQL (Neon)**.

## 🚀 Technologies utilisées

- **FastAPI** - Framework web moderne et rapide
- **SQLAlchemy** - ORM Python
- **Neon PostgreSQL** - Base de données serverless
- **Cloudinary** - Stockage d'images
- **JWT** - Authentification
- **Uvicorn** - Serveur ASGI
- **Pydantic** - Validation de données

## 📋 Fonctionnalités

### 1. Authentification
- ✅ Inscription (register)
- ✅ Connexion (login)
- ✅ Récupération du profil utilisateur
- ✅ Protection des routes avec JWT

### 2. Gestion des Fournisseurs
- ✅ CRUD complet (Create, Read, Update, Delete)
- ✅ Liste de tous les fournisseurs
- ✅ Détails d'un fournisseur avec ses approvisionnements

### 3. Gestion des Produits
- ✅ CRUD complet
- ✅ Upload d'image sur Cloudinary
- ✅ Gestion du stock (increment/decrement)
- ✅ Validation du stock (pas de stock négatif)
- ✅ Liste de tous les produits
- ✅ Détails d'un produit avec ses approvisionnements

### 4. Gestion des Approvisionnements
- ✅ CRUD complet
- ✅ Mise à jour automatique du stock lors de la création
- ✅ Liste de tous les approvisionnements avec fournisseur et produit

## 🏗️ Architecture

```
app/
├── routes/              # Routes API (Controllers)
├── services/            # Logique métier (Service Layer)
├── repositories/        # Accès aux données (Repository Pattern)
├── models.py            # Modèles SQLAlchemy
├── schemas.py           # Schémas Pydantic
├── auth.py              # Authentification JWT
├── database.py          # Configuration base de données
├── config.py            # Configuration de l'application
├── cloudinary_service.py # Service Cloudinary
└── main.py              # Application FastAPI
```

## 📦 Installation

### 1. Cloner le projet

```bash
git clone <url-du-repo>
cd gestion-des-approvisionnements
```

### 2. Créer un environnement virtuel

```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur macOS/Linux:
source venv/bin/activate

# Sur Windows:
venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configuration de l'environnement

Créer un fichier `.env` à la racine du projet :

```env
# Database (Neon PostgreSQL)
DATABASE_URL=postgresql://username:password@host.neon.tech/dbname?sslmode=require

# Server
APP_NAME="Supply Management API"
DEBUG=True
HOST=0.0.0.0
PORT=8000

# JWT
SECRET_KEY=your_super_secret_key_change_this_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# Cloudinary
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### 5. Démarrer l'application

```bash
# Méthode 1 : Via uvicorn directement
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Méthode 2 : Via le script run.py
python run.py
```

Le serveur démarrera sur `http://localhost:8000`

## 📚 Documentation API

La documentation interactive Swagger est disponible à :
- **Swagger UI** : http://localhost:8000/api-docs
- **ReDoc** : http://localhost:8000/api-redoc

## 🔐 Authentification

Toutes les routes (sauf `/api/auth/register` et `/api/auth/login`) nécessitent un token JWT.

### 1. S'inscrire

```bash
POST http://localhost:8000/api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "nom": "John Doe"
}
```

### 2. Se connecter

```bash
POST http://localhost:8000/api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Réponse :**
```json
{
  "success": true,
  "message": "Connexion réussie",
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "nom": "John Doe"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

### 3. Utiliser le token

Ajouter le token dans le header `Authorization` :

```
Authorization: Bearer <votre_token>
```

## 📝 Exemples d'utilisation

### Créer un fournisseur

```bash
POST http://localhost:8000/api/fournisseurs
Authorization: Bearer <token>
Content-Type: application/json

{
  "nom": "Fournisseur ABC",
  "telephone": "221771234567",
  "adresse": "Dakar, Sénégal"
}
```

### Créer un produit avec image

```bash
POST http://localhost:8000/api/produits
Authorization: Bearer <token>
Content-Type: multipart/form-data

libelle=Ordinateur Portable
prix_unitaire=750000
quantite_stock=10
image=@/path/to/image.jpg
```

### Créer un approvisionnement

```bash
POST http://localhost:8000/api/approvisionnements
Authorization: Bearer <token>
Content-Type: application/json

{
  "quantite": 50,
  "fournisseur_id": "uuid-du-fournisseur",
  "produit_id": "uuid-du-produit"
}
```

## 🧪 Tester l'API

### Méthode 1 : Via Swagger UI (Recommandé)

1. Ouvrir http://localhost:8000/api-docs
2. Cliquer sur "Authorize" en haut à droite
3. Entrer le token : `Bearer VOTRE_TOKEN`
4. Tester toutes les routes directement

### Méthode 2 : Via cURL

Voir le fichier `CURL_EXAMPLES.md` pour tous les exemples

### Méthode 3 : Via Postman/Thunder Client

Importer la collection depuis `postman-collection.json`

## 🔧 Commandes utiles

```bash
# Démarrer le serveur en mode développement
uvicorn app.main:app --reload

# Démarrer le serveur en mode production
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Formater le code avec black
black app/

# Linter avec flake8
flake8 app/
```

## 📊 Modèle de données

### User
- id (UUID)
- email (String, unique)
- password (String, hashé)
- nom (String)
- role (String, default: "user")

### Fournisseur
- id (UUID)
- nom (String)
- telephone (String)
- adresse (String)

### Produit
- id (UUID)
- libelle (String)
- prix_unitaire (Float)
- quantite_stock (Integer, default: 0)
- image (String, nullable)

### Approvisionnement
- id (UUID)
- date (DateTime)
- quantite (Integer)
- fournisseur_id (UUID)
- produit_id (UUID)

## 🛡️ Sécurité

- Authentification JWT avec tokens sécurisés
- Hashage des mots de passe avec bcrypt
- Validation stricte des données avec Pydantic
- Protection CORS configurée
- Gestion centralisée des erreurs

## ✅ Règles métier

- ❌ Le stock ne peut jamais être négatif
- ✅ Erreur 400 si stock insuffisant lors de la décrémentation
- ✅ Upload d'images sur Cloudinary (max 5MB)
- ✅ Mise à jour automatique du stock lors des approvisionnements
- ✅ Suppression automatique des images lors de la suppression des produits

## 🎯 Points forts

### Architecture professionnelle
- Repository Pattern pour l'accès aux données
- Service Layer pour la logique métier
- Séparation claire des responsabilités
- Code maintenable et testable

### Performance
- FastAPI = très rapide (basé sur Starlette et Pydantic)
- Async/await supporté nativement
- Documentation auto-générée

### Developer Experience
- Type hints complets
- Validation automatique avec Pydantic
- Messages d'erreur clairs
- Documentation interactive

## 📄 Licence

MIT

## 👨‍💻 Auteur

Développé pour l'examen de fin de module - École Supérieure Professionnelle 221
