import uvicorn
from gestion_des_approvisionnements.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "gestion_des_approvisionnements.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
