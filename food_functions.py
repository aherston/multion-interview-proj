import replicate
import multion
import os
from PIL import Image

# return "grocery" or "prepared" based on an image of food passed in
def grocery_or_prepared(image: Image):
    return replicate.run(
        "andreasjansson/blip-2:f677695e5e89f8b236e52ecd1d3f01beb44c34606419bcc19345e046d8f786f9",
        input={
            "image": image,
            "caption": False,
            "question": "is this a grocery item or a prepared food item? Please respond in only one word: \"grocery\" or \"prepared\".",
            "temperature": 1,
            "use_nucleus_sampling": False
        }
    )

# order food from [image] from website [site] 
def order_food(image: Image, site: str):
    output = replicate.run(
    "yorickvp/llava-13b:a0fdc44e4f2e1f20f2bb4e27846899953ac8e66c5886c5878fa1d6b73ce009e5",
    input={
        "image": image,
        "top_p": 1,
        "prompt": "I am a waiter, and you want to order this item exactly at a restaurant. Please include only the response you would give to the waiter if I said \"What can I get for you today?\" Include only information about the food on the plate; no other information about the background or the dinnerware. ",
        "max_tokens": 1024,
        "temperature": 0.2
    }
    )

    caption = ""

    for item in output:
        # https://replicate.com/yorickvp/llava-13b/api#output-schema
        caption = caption + item

    print(caption)

    multion_api_key = os.getenv('62259af8ee764b759a94f8614cca2465')
    multion.login(use_api=True, multion_api_key=multion_api_key)

    response = multion.create_session({"url": "https://google.com"})
    print(response['message'])
    session_id = response['session_id']
    print("SID: " + session_id)

    prompt = "Please put the following item in my cart on" + site + ": " + caption
    url = "https://https.google.com"

    while True:
        res = multion.step_session(session_id,{"input":  prompt, "url": url})
    
        print(res)
        if res['status'] == 'DONE':
            print('task completed')
            break

    multion.close_session(session_id)

