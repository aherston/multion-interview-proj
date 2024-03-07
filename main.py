from http.client import HTTPException
from typing import Union

from flask import jsonify
from fastapi import FastAPI, Form
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

@app.post("/uploadimage/")
async def upload_image(uri: str = Form(...)):

    print(uri)  

    output: str = get_food_type(uri)

    print(output)
    response: [] = []

    if output == "grocery":
        response = order_food(uri, "InstaCart")
    elif output == "prepared":
        response = order_food(uri, "DoorDash")
    elif output == "list":
        response = order_list(uri)
    else: 
        print("ERROR")
        exit(1)

    if (response != []):
        print(response)
        return jsonify(response)
    else:
        print("error ordering food")


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}