from pydantic import BaseModel

class BoundingBox(BaseModel):
    x_min: int
    y_min: int
    x_max: int
    y_max: int

class ImageRequest(BaseModel):
    image_url: str
    bounding_box: BoundingBox

class ImageResponse(BaseModel):
    original_image_url: str
    processed_image_url: str
