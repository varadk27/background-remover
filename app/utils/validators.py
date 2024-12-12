from aiohttp import ClientSession
import logging

logger = logging.getLogger(__name__)

def validate_coordinates(bbox: dict) -> bool:
    """Validate bounding box coordinates."""
    try:
        return (
            bbox.x_min >= 0 and
            bbox.y_min >= 0 and
            bbox.x_max > bbox.x_min and
            bbox.y_max > bbox.y_min
        )
    except Exception as e:
        logger.error(f"Error validating coordinates: {str(e)}")
        return False

async def validate_image_url(url: str) -> bool:
    """Validate if image URL is accessible and contains an image."""
    try:
        async with ClientSession() as session:
            async with session.head(url) as response:
                content_type = response.headers.get('content-type', '')
                return (
                    response.status == 200 and
                    content_type.startswith('image/')
                )
    except Exception as e:
        logger.error(f"Error validating image URL: {str(e)}")
        return False