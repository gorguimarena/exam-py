import cloudinary
import cloudinary.uploader
from fastapi import UploadFile, HTTPException
from gestion_des_approvisionnements.config import settings
from urllib.parse import unquote, urlparse

# Configuration Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)


class CloudinaryService:
    """Service pour gérer les uploads sur Cloudinary"""

    @staticmethod
    def _extract_public_id_from_url(image_url: str) -> str:
        """Extraire le public_id Cloudinary à partir d'une URL complète."""
        parsed_url = urlparse(image_url)
        path = unquote(parsed_url.path or "")

        upload_marker = "/upload/"
        if upload_marker not in path:
            return ""

        # Garder uniquement la partie utile après /upload/
        path_after_upload = path.split(upload_marker, 1)[1].lstrip("/")
        known_folder = "gestion-approvisionnement/produits/"

        # Nos images sont stockées dans ce dossier: c'est le point d'ancrage
        if known_folder in path_after_upload:
            relative_path = path_after_upload.split(known_folder, 1)[1]
            if not relative_path:
                return ""
            return f"{known_folder}{relative_path.rsplit('.', 1)[0]}"

        # Fallback générique pour les URL Cloudinary classiques
        segments = [segment for segment in path_after_upload.split("/") if segment]
        if not segments:
            return ""

        if segments[0].startswith("v") and segments[0][1:].isdigit():
            segments = segments[1:]

        if not segments:
            return ""

        public_path = "/".join(segments)
        return public_path.rsplit(".", 1)[0]
    
    @staticmethod
    async def upload_image(file: UploadFile) -> str:
        """
        Upload une image sur Cloudinary
        
        Args:
            file: Fichier image à uploader
            
        Returns:
            URL de l'image uploadée
        """
        # Vérifier le type de fichier
        allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp"]
        
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail="Seules les images sont acceptées (JPEG, PNG, GIF, WEBP)"
            )
        
        # Vérifier la taille (5MB max)
        contents = await file.read()
        file_size = len(contents)
        
        if file_size > 5 * 1024 * 1024:  # 5MB
            raise HTTPException(
                status_code=400,
                detail="La taille du fichier ne doit pas dépasser 5MB"
            )
        
        try:
            # Upload sur Cloudinary
            result = cloudinary.uploader.upload(
                contents,
                folder="gestion-approvisionnement/produits",
                resource_type="image"
            )
            
            return result.get("secure_url")
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur lors de l'upload de l'image: {str(e)}"
            )
    
    @staticmethod
    def delete_image(image_url: str) -> bool:
        """
        Supprimer une image de Cloudinary depuis son URL
        
        Args:
            image_url: URL de l'image à supprimer
            
        Returns:
            True si la suppression a réussi, False sinon
        """
        if not image_url:
            return False
            
        try:
            public_id = CloudinaryService._extract_public_id_from_url(image_url)
            if not public_id:
                print(f"Impossible d'extraire le public_id depuis l'URL: {image_url}")
                return False

            result = cloudinary.uploader.destroy(
                public_id,
                resource_type="image",
                type="upload",
                invalidate=True
            )

            # "not found" veut souvent dire déjà supprimée
            if result.get("result") in {"ok", "not found"}:
                return True

            print(f"Échec de la suppression Cloudinary: {result}")
            return False
            
        except Exception as e:
            print(f"Erreur lors de la suppression de l'image: {str(e)}")
            return False


cloudinary_service = CloudinaryService()
