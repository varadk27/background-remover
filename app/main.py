from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .models import ImageRequest, ImageResponse
from .services.image_processor import ImageProcessor
from .services.storage import StorageService
from .utils.validators import validate_coordinates, validate_image_url
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Background Removal API",
    description="API for removing backgrounds from product images",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[""],
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize services
image_processor = ImageProcessor()
storage_service = StorageService()

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.post("/remove-background", response_model=ImageResponse)
async def remove_background(request: ImageRequest):
    """Remove background from an image."""
    try:
        # Validate image URL
        if not await validate_image_url(request.image_url):
            raise HTTPException(status_code=400, detail="Invalid or inaccessible image URL")

        # Validate coordinates
        if not validate_coordinates(request.bounding_box):
            raise HTTPException(status_code=400, detail="Invalid bounding box coordinates")

        # Process the image
        processed_image_data = await image_processor.process_image(request.image_url, request.bounding_box)

        # Upload directly to Cloudinary
        processed_image_url = await storage_service.upload_image(processed_image_data)

        return ImageResponse(
            original_image_url=request.image_url,
            processed_image_url=processed_image_url
        )

    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")







# @app.post("/remove-background", response_model=ImageResponse)
# async def remove_background(request: ImageRequest):
#     """Remove background from an image."""
#     try:
#         # Validate image URL
#         if not await validate_image_url(request.image_url):
#             raise HTTPException(status_code=400, detail="Invalid or inaccessible image URL")

#         # Validate coordinates
#         if not validate_coordinates(request.bounding_box):
#             raise HTTPException(status_code=400, detail="Invalid bounding box coordinates")

#         # Process the image
#         processed_image_path = await image_processor.process_image(request.image_url, request.bounding_box)

#         # Simulate image upload
#         processed_image_url = await storage_service.upload_image(processed_image_path)

#         return ImageResponse(
#             original_image_url=request.image_url,
#             processed_image_url=processed_image_url
#         )

#     except Exception as e:
#         logger.error(f"Error processing image: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")