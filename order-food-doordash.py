from food_functions import grocery_or_prepared, order_food
from PIL import Image

# get meeting info from photo

image: Image = Image.open("assets/fish-tacos.jpg", "rb")

output: str = grocery_or_prepared(image)

while (output != ("grocery" or "prepared")):
    # rerun until we get an expected output
    print("rerunning g/p")
    output = grocery_or_prepared(image)

if output == "grocery":
    output = order_food(image, "InstaCart")
elif output == "prepared":
    output = order_food(image, "DoorDash")
else: 
    print("ERROR")
    exit(1)

