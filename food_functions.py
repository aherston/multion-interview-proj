import replicate
import multion
import os

# return "grocery" or "prepared" based on an image of food passed in
def get_food_type(image: any) -> str:
    output = replicate.run(
        "andreasjansson/blip-2:f677695e5e89f8b236e52ecd1d3f01beb44c34606419bcc19345e046d8f786f9",
        input={
            "image": image,
            "caption": False,
            "question": "is this a picture of an item you would find at a grocery store, a prepared food item you would find at a restaurant, or a list of multiple items? Please respond in only one word: \"grocery,\" \"prepared,\" or \"list\".",
            "temperature": 1,
            "use_nucleus_sampling": False
        }
    )
    if (output != "grocery" and output != "prepared" and output != "list"):
        # rerun until we get an expected output
        # TODO might want to add an end case here i.e. if this runs like 5 times
        print("output: " + output + "...rerunning get_food_type")
        return get_food_type(image)
    else:
        return output

# order food from [image] from website [site] 
def order_food(image: any, site: str) -> int:
    output = replicate.run(
    "yorickvp/llava-13b:a0fdc44e4f2e1f20f2bb4e27846899953ac8e66c5886c5878fa1d6b73ce009e5",
    input={
        "image": image,
        "top_p": 1,
        "prompt": "I am a waiter, and you want to order this item exactly at a restaurant. Be very descriptive. Please include only the response you would give to the waiter if I said \"What can I get for you today?\" Include only information about the food on the plate; no other information about the background or the dinnerware. ",
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

    prompt = "Please put the following item in my cart on " + site + ": " + caption
    url = "https://https.google.com"

    while True:
        res = multion.step_session(session_id,{"input":  prompt, "url": url})
    
        print(res)
        if res['status'] == 'DONE':
            print('task completed')
            break

    multion.close_session(session_id)
    
    # on success
    return 0

def order_list(image: any):
    output = replicate.run(
    "yorickvp/llava-v1.6-34b:41ecfbfb261e6c1adf3ad896c9066ca98346996d7c4045c5bc944a79d430f174",
    input={
        "image": image,
        "top_p": 1,
        "prompt": "Output the text in this image as a bullet point grocery list.",
        "max_tokens": 1024,
        "temperature": 0.2
    }
    )

    shopping_list: str = ""

    # The yorickvp/llava-v1.6-34b model can stream output as it's running.
    # The predict method returns an iterator, and you can iterate over that output.
    for item in output:
        # https://replicate.com/yorickvp/llava-v1.6-34b/api#output-schema
        shopping_list = shopping_list + item

    multion_api_key = os.getenv('62259af8ee764b759a94f8614cca2465')
    multion.login(use_api=True, multion_api_key=multion_api_key)

    response = multion.create_session({"url": "https://google.com"})
    print(response['message'])
    session_id = response['session_id']
    print("SID: " + session_id)

    prompt = "Please put the following items in my cart on Instacart: " + shopping_list + "\n Please notify the user of any items that are unavailable. Pay close attention to make sure the quantities of items are correct"
    
    url = "https://https.google.com"

    while True:
        res = multion.step_session(session_id,{"input":  prompt, "url": url})
    
        print(res)
        if res['status'] == 'DONE':
            print('task completed')
            break

