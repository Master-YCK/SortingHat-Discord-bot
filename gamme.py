import setting
import torch 

# pip install accelerate
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b", token=setting.HF_TOKEN)
model = AutoModelForCausalLM.from_pretrained("google/gemma-2b", token=setting.HF_TOKEN, device_map="auto", torch_dtype=torch.float16)

# input_text = "Write me a poem about Machine Learning."
# input_ids = tokenizer(input_text, return_tensors="pt")

# outputs = model.generate(**input_ids)
# print(tokenizer.decode(outputs[0]))

def generate(input_text):
    input_ids = tokenizer(input_text, return_tensors="pt").to("mps")
    outputs = model.generate(**input_ids)
    AIgenerate = tokenizer.decode(outputs[0])
    return AIgenerate

