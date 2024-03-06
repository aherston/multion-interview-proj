from http.client import HTTPException
from typing import Union

from click import File

from fastapi import FastAPI, UploadFile
from pydantic import BaseModel

from food_functions import get_food_type, order_food, order_list

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a JPEG or PNG image.")
    
    image = await file.read()
    
    # image: any = open("assets/peets.jpg", "rb")

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


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}