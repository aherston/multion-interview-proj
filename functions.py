import replicate
import multion
import os

# return true if image includes information about food, and false otherwise
def get_is_food(image: str) -> bool:
    output = replicate.run(
    "yorickvp/llava-13b:a0fdc44e4f2e1f20f2bb4e27846899953ac8e66c5886c5878fa1d6b73ce009e5",
    input={
        "image": image,
        "top_p": 1,
        "prompt": "if this photo mentions or depicts food anywhere, respond with \"true\". otherwise, respond with \"false\". Please include no additional text or explanation",
        "max_tokens": 1024,
        "temperature": 0.2
    }
    )

    res = ""
    for item in output:
        res += item

    print("is_food is " + res)

    if (res.lower() == "true"):
        return True
    elif (res.lower() == "false"):
        return False
    else:
        print("incorrect value for is_food: " + res.lower() + "...rerunning")
        get_is_food(image)

# return "grocery" or "prepared" based on an image of food passed in
def get_food_type(image: str) -> str:
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

    res = ""
    for item in output:
        res += item

    if (res.lower() != "grocery" and res.lower() != "prepared" and res.lower() != "list"):
        print("incorrect value for food_type: " + res.lower() + "...rerunning get_food_type")
        return get_food_type(image)
    else:
        return output
    
def get_one_or_several(image: any) -> str:
    output = replicate.run(
    "andreasjansson/blip-2:f677695e5e89f8b236e52ecd1d3f01beb44c34606419bcc19345e046d8f786f9",
    input={
        "image": image,
        "caption": False,
        "question": "is this a picture of an item, or a list of several items? please respond in only one word: \"one,\" or \"several\"",
        "temperature": 1,
        "use_nucleus_sampling": False
    }
    )
    res = ""
    for item in output:
        res += item

    if (res.lower() != "several" and res.lower() != "one"):
        print("incorrect value for food_type: " + res.lower() + "...rerunning get_one_or_several")
        return get_one_or_several(image)
    else:
        return output

# order food from [image] from website [site] 
def order_food(image: any, site: str) -> []:
    
    output = replicate.run(
    "yorickvp/llava-13b:a0fdc44e4f2e1f20f2bb4e27846899953ac8e66c5886c5878fa1d6b73ce009e5",
    input={
        "image": image,
        "top_p": 1,
        "prompt": "I am a waiter, and you want to order this item exactly at a restaurant. Be very descriptive. Do not include any items that aren't in the photo. Please include only the response you would give to the waiter if I said \"What can I get for you today?\" Include only information about the food on the plate; no other information about the background or the dinnerware. ",
        "max_tokens": 1024,
        "temperature": 0.2
    }
    )

    caption = ""
    return_str = []

    for item in output:
        # https://replicate.com/yorickvp/llava-13b/api#output-schema
        caption = caption + item

    print(caption)
    return_str.append(caption)

    multion.login()
    multion.set_remote(False)

    response = multion.create_session({"url": "https://google.com"})
    print(response['message'])
    return_str.append(response['message'])
    session_id = response['session_id']
    print("SID: " + session_id)
    return_str.append("SID: " + session_id)

    prompt = "Please put the following item in my cart on " + site + ": " + caption
    
    url = "https://https.google.com"

    while True:
        res = multion.step_session(session_id,{"input":  prompt, "url": url})
    
        print(res)
        return_str.append(res)

        if res['status'] == 'DONE':
            print('task completed')
            break

    multion.close_session(session_id)
    
    # on success
    return return_str

# order list of food items in image on InstaCart
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

    multion.login()
    multion.set_remote(False)

    return_str = []
    return_str.append(shopping_list)

    response = multion.create_session({"url": "https://google.com"})
    print(response['message'])
    return_str.append(response['message'])
    session_id = response['session_id']
    print("SID: " + session_id)
    return_str.append("SID: " + session_id)

    prompt = "Please put the following items in my cart on Instacart: " + shopping_list + "\n Please notify the user of any items that are unavailable. Pay close attention to make sure the quantities of items are correct"
    url = "https://https.google.com"

    while True:
        res = multion.step_session(session_id,{"input":  prompt, "url": url})
    
        print(res)
        return_str.append(res)
        
        if res['status'] == 'DONE':
            print('task completed')
            break

    multion.close_session(session_id)
    return return_str

# add meeting to calendar based on image
def add_to_calendar(image: str) -> []:

    # get time and date for meeting
    output = replicate.run(
        "yorickvp/llava-v1.6-34b:41ecfbfb261e6c1adf3ad896c9066ca98346996d7c4045c5bc944a79d430f174",
        input={
            "image": image,
            "top_p": 1,
            "prompt": "what is the proposed time and date for the meeting?",
            "history": [],
            "max_tokens": 1024,
            "temperature": 0.2
        }
    )

    meeting_info = ""

    for item in output:
        # https://replicate.com/yorickvp/llava-v1.6-34b/api#output-schema
        meeting_info = meeting_info + item

    # get meeting title
    output = replicate.run(
    "yorickvp/llava-v1.6-34b:41ecfbfb261e6c1adf3ad896c9066ca98346996d7c4045c5bc944a79d430f174",
    input={
        "image": image,
        "top_p": 1,
        "prompt": "what is the subject of this conversation and who is the user texting? their name is at the top of the photo. \n\nplease format your response as a concise sentence stating the topic and the person's name. for example:\n\"getting coffee with suzie\"\n\"visiting ben's office\"\n\"running with james\"",
        "history": [],
        "max_tokens": 1024,
        "temperature": 0.2
    }
    )

    meeting_title = ""

    for item in output:
        # https://replicate.com/yorickvp/llava-v1.6-34b/api#output-schema
        meeting_title = meeting_title + item

    # pass info into multion API

    multion.login()
    multion.set_remote(False)

    return_str = []

    response = multion.create_session({"url": "https://google.com"})
    print(response['message'])
    session_id = response['session_id']
    print("SID: " + session_id)

    prompt = "Your goal is to create a Google Calendar event. " + meeting_info + "Follow these instructions carefully to create the event: 1. Click the 'Create' button to activate the event creation dropdown. \n2. Wait 2 seconds. You should now be able to see the dropdown with several options. Please select the first option, labeled 'Event'. Keep attempting to select 'Event' until the meeting details pop up.\n3. Fill in the details for the meeting accordingly. Use " + meeting_title + " as the title for the event."
    url = "https://https.calendar.google.com"

    while True:
        res = multion.step_session(session_id,{"input":  prompt, "url": url})
    
        print(res)
        
        if res['status'] == 'DONE':
            print('task completed')
            return_str.append(res['message'])
            break

    multion.close_session(session_id)
    return return_str
