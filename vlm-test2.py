import replicate

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

for item in output:
    # https://replicate.com/yorickvp/llava-v1.6-34b/api#output-schema
    print(item, end="")
