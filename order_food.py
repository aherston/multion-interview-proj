from food_functions import get_food_type, order_food, order_list

# get meeting info from photo

image: any = open("assets/peets.jpg", "rb")

output: str = get_food_type(image)

print(output)

if output == "grocery":
    success: int = order_food(image, "InstaCart")
elif output == "prepared":
    success: int = order_food(image, "DoorDash")
elif output == "list":
    success: int = order_list(image)
else: 
    print("ERROR")
    exit(1)

if (success == 0):
    print("success")
else:
    print("error ordering food")

