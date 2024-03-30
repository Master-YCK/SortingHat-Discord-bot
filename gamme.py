import setting
import torch 

from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b", token=setting.HF_TOKEN)
model = AutoModelForCausalLM.from_pretrained("google/gemma-2b", token=setting.HF_TOKEN, device_map="auto", torch_dtype=torch.float16)

def genText(input_text):
    input_ids = tokenizer(input_text, return_tensors="pt").to("cuda")
    outputs = model.generate(**input_ids, max_length=80)
    return tokenizer.decode(outputs[0])
