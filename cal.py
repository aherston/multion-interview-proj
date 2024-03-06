import replicate
import multion
import os

# get meeting info from photo

image = open("assets/meeting-text2.png", "rb")

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

# pass info into multion API

multion_api_key = os.getenv('62259af8ee764b759a94f8614cca2465')
multion.login(use_api=True, multion_api_key=multion_api_key)

response = multion.create_session({"url": "https://google.com"})
print(response['message'])
session_id = response['session_id']
print("SID: " + session_id)

prompt = "Create a google calendar event." + meeting_info
url = "https://calendar.google.com"

while True:
    res = multion.step_session(session_id,{"input":  prompt, "url": url})
 
    print(res)
    if res['status'] == 'DONE':
        print('task completed')
        break

multion.close_session(session_id)
