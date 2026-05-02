import cloudinary
import cloudinary.uploader
import cloudinary.api
from fastapi import UploadFile, HTTPException
from gestion_des_approvisionnements.config import settings

# Configuration Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)


class CloudinaryService:
    """Service pour gérer les uploads sur Cloudinary"""
    
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
                folder="supply-management/produits",
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
        Supprimer une image de Cloudinary
        
        Args:
            image_url: URL de l'image à supprimer
            
        Returns:
            True si la suppression a réussi, False sinon
        """
        if not image_url:
            return False
            
        try:
            # Extraire le public_id depuis l'URL de manière robuste
            # Cloudinary URL formats:
            # - https://res.cloudinary.com/demo/image/upload/v12345/folder/image.jpg
            # - https://res.cloudinary.com/demo/image/upload/folder/image.jpg
            # - https://res.cloudinary.com/demo/image/upload/w_500,c_fill/folder/image.jpg
            
            # Trouver la position de "upload/" dans l'URL
            upload_pos = image_url.find("/upload/")
            if upload_pos == -1:
                print(f"Format d'URL Cloudinary invalide: {image_url}")
                return False
            
            # Récupérer tout ce qui suit "/upload/"
            after_upload = image_url[upload_pos + 8:]
            
            # Supprimer les transformations (tout ce qui commence par w_, h_, c_, etc.)
            parts = after_upload.split('/')
            clean_parts = []
            for part in parts:
                # Ignorer les paramètres de transformation (w_500, c_fill, etc.)
                if '=' in part:
                    continue
                clean_parts.append(part)
            
            # Reconstruire le chemin du fichier
            if clean_parts:
                file_path = '/'.join(clean_parts)
                # Extraire le public_id sans l'extension
                public_id = file_path.rsplit('.', 1)[0] if '.' in file_path else file_path
                
                # Supprimer l'image de Cloudinary
                result = cloudinary.uploader.destroy(public_id)
                
                if result.get("result") == "ok":
                    print(f"Image supprimée avec succès: {public_id}")
                    return True
                else:
                    print(f"Échec de la suppression de l'image: {result}")
                    return False
            else:
                print(f"Impossible d'extraire le chemin du fichier: {image_url}")
                return False
            
        except Exception as e:
            # Ne pas bloquer l'opération si la suppression échoue
            print(f"Erreur lors de la suppression de l'image: {str(e)}")
            return False


cloudinary_service = CloudinaryService()
