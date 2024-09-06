from io import BytesIO
from PIL import Image as PILImage
from django.core.files.base import ContentFile


class ImageHandler:

    @staticmethod
    def compress_image(image_file):
        with PILImage.open(image_file) as img:
            output_io = BytesIO()
            img.save(output_io, format=img.format, quality=85)  # Adjust quality as needed
            output_io.seek(0)  # Reset file pointer to the beginning
            return ContentFile(output_io.read(), name=image_file.name)


    @staticmethod
    def is_image_greater_than_one_mb(image):
        return image.size > 1 * 1024 * 1024