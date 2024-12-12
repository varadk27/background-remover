# import cloudinary
# import cloudinary.uploader
# import logging
# from io import BytesIO
# import os

# logger = logging.getLogger(__name__)

# class StorageService:
#     """Cloudinary-based Storage Service."""

#     def __init__(self):
#         cloudinary.config(
#             cloud_name=os.getenv("CLOUD_NAME"),
#             api_key=os.getenv("API_KEY"),
#             api_secret=os.getenv("SECRET_KEY"),
#         )

#     async def upload_image(self, image_data: BytesIO) -> str:
#         """
#         Upload the image to Cloudinary and return the public URL.
#         """
#         try:
#             logger.info("Uploading image to Cloudinary")
#             response = cloudinary.uploader.upload(
#                 image_data,
#                 folder="background_removal"
#             )
#             return response["secure_url"]
#         except Exception as e:
#             logger.error(f"Error uploading image to Cloudinary: {str(e)}")
#             raise Exception(f"Cloudinary upload failed: {str(e)}")






import cloudinary
import cloudinary.uploader
import logging
import os

logger = logging.getLogger(__name__)

class StorageService:
    """Cloudinary-based Storage Service."""

    def __init__(self):
        cloudinary.config(
            cloud_name=os.getenv("CLOUD_NAME"),
            api_key=os.getenv("API_KEY"),
            api_secret=os.getenv("SECRET_KEY"),
        )

    async def upload_image(self, image_path: str) -> str:
        """
        Upload the image to Cloudinary and return the public URL.
        """
        try:
            logger.info(f"Uploading {image_path} to Cloudinary.")
            response = cloudinary.uploader.upload(image_path, folder="background_removal")
            return response["secure_url"]
        except Exception as e:
            logger.error(f"Error uploading image to Cloudinary: {str(e)}")
            raise Exception(f"Cloudinary upload failed: {str(e)}")
