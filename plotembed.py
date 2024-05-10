import base64

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

image_path = "assets/plot.png"
encoded_image = encode_image_to_base64(image_path)
