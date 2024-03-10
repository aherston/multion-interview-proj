image = "assets/ananya-text.jpg"
import base64
import pyperclip

def image_to_uri(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return "data:image/jpg;base64," + encoded_string

uri = image_to_uri(image)
pyperclip.copy(uri)

