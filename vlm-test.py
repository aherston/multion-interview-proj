import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-VL-Chat", trust_remote_code=True)

model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-VL-Chat", device_map="cuda", trust_remote_code=True).eval()
model.generation_config = GenerationConfig.from_pretrained("Qwen/Qwen-VL-Chat", trust_remote_code=True)

query = tokenizer.from_list_format([
    {'image': 'assets/meeting-email.png'},
    {'text': 'Is this a photo of text message/email thread, or a food packaging?'},
])

response, history = model.chat(tokenizer, query=query, history=None)
print(response)

