import multion
import os
multion_api_key = os.getenv('62259af8ee764b759a94f8614cca2465')
multion.login(use_api=True, multion_api_key=multion_api_key)

response = multion.create_session({"url": "https://google.com"})
print(response['message'])
session_id = response['session_id']
print("SID: " + session_id)

prompt = "Create a meeting for March 5 from 7-8pm at 2311 bowditch street."
url = "https://calendar.google.com"

while True:
    res = multion.step_session(session_id,{"input":  prompt, "url": url})
 
    print(res)
    if res['status'] == 'DONE':
        print('task completed')
        break

multion.close_session(session_id)
