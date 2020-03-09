from PIL import Image
from io import BytesIO

def load_img_from_request(request):
    img = Image.open(BytesIO(request.content))

    if img.format == "PNG":
        # convert to jpg with white background if it's png
        with_background = Image.new("RGB", img.size, (255, 255, 255))
        with_background.paste(img, mask=img.split()[3])
        byte_io = BytesIO()
        with_background.save(byte_io, 'JPEG')
    else:
        byte_io = BytesIO()
        img.save(byte_io, 'JPEG')
    
    return byte_io.getvalue()
