from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from gestion_des_approvisionnements.config import settings
from gestion_des_approvisionnements.database import engine, Base
from gestion_des_approvisionnements.routes import auth_routes, fournisseur_routes, produit_routes, approvisionnement_routes

# Créer les tables
Base.metadata.create_all(bind=engine)

# Créer l'application FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description="API RESTful complète pour la gestion des approvisionnements d'une boutique",
    version="1.0.0",
    docs_url="/api-docs",
    redoc_url="/api-redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Gestionnaire d'erreurs global
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Gestionnaire d'erreurs global"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "Une erreur interne est survenue",
            "details": str(exc) if settings.DEBUG else None
        }
    )


# Route de base
@app.get("/", tags=["Root"])
def read_root():
    """Route de base de l'API"""
    return {
        "success": True,
        "message": "API de Gestion des Approvisionnements",
        "version": "1.0.0",
        "documentation": "/api-docs"
    }


# Enregistrer les routes
app.include_router(auth_routes.router)
app.include_router(fournisseur_routes.router)
app.include_router(produit_routes.router)
app.include_router(approvisionnement_routes.router)
