import multion
import os

text = """

Photographers at Berkeley
Meeting Minutes
3/7/22, 6:40PM
Eshelman 318
________________________________________________________________________________________________ 


ATTENDEES
Abigail Mamani
Sumit Choudhary
Shipransh Agrawal
Alice Herston

PURPOSE
Finalize infosession dates and note tabling improvements for tomorrow

TOPICS DISCUSSED
Infosession rooms confirmed – add infosession date and times to flyers
14th in person, 18th hybrid
Wednesday’s meeting – finalize infosession info
Goods and bads about today’s tabling
Goods
People were more receptive to going up to them and handing out flyers
Instead of tabling some days we could just go around with flyers taking pictures
Bads
Not very many people in the last few hours
A lot of people asking about the infosession dates
More ideas for spreading the word
Put up flyers on billboards
Contact people in dorms and get flyers put up there

ACTION ITEMS
Abigail: Update flyers with infosession info, print 200 flyers
Alice: Edit + post photos, create infosession details post
Shipransh: timeline graphic
Sumit: pick up poster

NEXT MEETING
Wednesday, 3/9/22, 7:10PM, Eshelman 350/Zoom

"""

multion_api_key = os.getenv('cfab4cd24d1e4ea191ac006a1816185c')
multion.login(use_api=True, multion_api_key=multion_api_key)

response = multion.create_session({"url": "https://google.com"})
print(response['message'])
session_id = response['session_id']
print("SID: " + session_id)

prompt = "summarize these meeting notes into an email, then send it to aherston@gmail.com. use a new line for each bullet point and separate paragraphs. verify with the user before sending the email: " + text
url = "https://mail.google.com"

while True:
    res = multion.step_session(session_id,{"input":  prompt, "url": url})
 
    print(res)
    if res['status'] == 'DONE':
        print('task completed')
        break

multion.close_session(session_id)
