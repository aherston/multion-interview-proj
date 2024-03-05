import replicate
import multion
import os

# get meeting info from photo

image = open("assets/granola.jpg", "rb")

output = replicate.run(
    "andreasjansson/blip-2:f677695e5e89f8b236e52ecd1d3f01beb44c34606419bcc19345e046d8f786f9",
    input={
        "image": image,
        "caption": False,
        "question": "what is this a picture of?",
        "temperature": 1,
        "use_nucleus_sampling": False
    }
)

caption = ""

for item in output:
    # https://replicate.com/yorickvp/llava-v1.6-34b/api#output-schema
    caption = caption + item

print(caption)

# pass info into multion API

multion_api_key = os.getenv('62259af8ee764b759a94f8614cca2465')
multion.login(use_api=True, multion_api_key=multion_api_key)

response = multion.create_session({"url": "https://google.com"})
print(response['message'])
session_id = response['session_id']
print("SID: " + session_id)

prompt = "Put this item in my cart on instacart (for groceries) or doordash (for fresh food): " + caption
url = "https://https.google.com"

while True:
    res = multion.step_session(session_id,{"input":  prompt, "url": url})
 
    print(res)
    if res['status'] == 'DONE':
        print('task completed')
        break

multion.close_session(session_id)
