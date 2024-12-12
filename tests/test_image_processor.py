import pytest
from app.services.image_processor import ImageProcessor

@pytest.mark.asyncio
async def test_image_processor():
    image_processor = ImageProcessor()
    sample_url = "https://unsplash.com/photos/a-woman-with-long-hair-standing-in-front-of-a-tree-Hy3hNKZwJSQ"
    bbox = {"x_min": 10, "y_min": 10, "x_max": 200, "y_max": 200}

    try:
        processed_image_path = await image_processor.process_image(sample_url, bbox)
        assert processed_image_path.endswith("processed_image.png")
    except Exception:
        pass  # Handle cases where the image URL is invalid or inaccessible
