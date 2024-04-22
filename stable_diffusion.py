from diffusers import StableDiffusionPipeline
import torch

model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)

# If run on macOS change the device to "mps", else use "cuda" for Linux or Windows
pipe = pipe.to("mps")

def generate_image(prompt):
    image = pipe(prompt).images[0]  
    image.save("generated.png")
