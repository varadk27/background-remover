import cv2
import numpy as np
from rembg import remove
import requests
from io import BytesIO
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class ImageProcessor:
    """Service for processing images and removing backgrounds."""

    async def process_image(self, image_url: str, bounding_box: dict) -> BytesIO:
        try:
            # Download image
            logger.info(f"Downloading image from {image_url}")
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()

            # Convert to PIL Image
            image = Image.open(BytesIO(response.content))

            # Convert to numpy array for OpenCV processing
            image_np = np.array(image)

            # Ensure image is RGB
            if len(image_np.shape) == 2:  # Grayscale
                image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2RGB)
            elif image_np.shape[2] == 4:  # RGBA
                image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2RGB)

            # Crop image to bounding box
            cropped = image_np[
                bounding_box.y_min:bounding_box.y_max,
                bounding_box.x_min:bounding_box.x_max
            ]

            # Remove background using rembg
            processed_image = remove(cropped)

            # Convert back to PIL Image and save to BytesIO
            img_byte_arr = BytesIO()
            Image.fromarray(processed_image).save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)

            return img_byte_arr

        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            raise Exception(f"Error processing image: {str(e)}")









# import cv2
# import numpy as np
# from rembg import remove
# import requests
# from io import BytesIO
# from PIL import Image
# import os
# import logging

# logger = logging.getLogger(__name__)

# class ImageProcessor:
#     """Service for processing images and removing backgrounds."""

#     async def process_image(self, image_url: str, bounding_box: dict) -> str:
#         try:
#             # Download image
#             logger.info(f"Downloading image from {image_url}")
#             response = requests.get(image_url, timeout=10)
#             response.raise_for_status()

#             # Convert to PIL Image
#             image = Image.open(BytesIO(response.content))

#             # Convert to numpy array for OpenCV processing
#             image_np = np.array(image)

#             # Ensure image is RGB
#             if len(image_np.shape) == 2:  # Grayscale
#                 image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2RGB)
#             elif image_np.shape[2] == 4:  # RGBA
#                 image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2RGB)

#             # Crop image to bounding box
#             cropped = image_np[
#                 bounding_box.y_min:bounding_box.y_max,
#                 bounding_box.x_min:bounding_box.x_max
#             ]

#             # Remove background using rembg
#             processed_image = remove(cropped)

#             # Save the processed image locally
#             output_path = os.path.join("static", "processed_image.png")
#             Image.fromarray(processed_image).save(output_path, format="PNG")

#             logger.info(f"Processed image saved at {output_path}")
#             return output_path

#         except Exception as e:
#             logger.error(f"Error processing image: {str(e)}")
#             raise Exception(f"Error processing image: {str(e)}")