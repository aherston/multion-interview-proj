from http.client import HTTPException
from typing import Union

from fastapi import FastAPI, Form
from pydantic import BaseModel

from functions import get_food_type, order_food, order_list, get_is_food, add_to_calendar,\
    get_one_or_several

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

    if (get_is_food(uri)):
        output: str = get_one_or_several(uri)

        print(output)
        response: [] = []

        if output == "one":
            output = get_food_type(uri)
            if output == "grocery":
                response = order_food(uri, "InstaCart")
            elif output == "prepared":
                response = order_food(uri, "DoorDash")
        elif output == "several":
            response = order_list(uri)
        else: 
            print("ERROR")
            exit(1)
    else:
        response = add_to_calendar(uri)

    if (response != []):
        print(response)
        return response
    else:
        print("error: multion did not run")
        exit(1)
