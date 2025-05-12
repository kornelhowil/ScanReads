import io
from PIL import Image

def img_to_bytes(image: Image.Image) -> bytes: 
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    
    return img_byte_arr.getvalue()
