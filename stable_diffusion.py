from diffusers import StableDiffusionPipeline
import torch

model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("mps")

# prompt = "a photo of an astronaut riding a horse on mars"
# image = pipe(prompt).images[0]  
    
# image.save("astronaut_rides_horse.png")

def genImg(user_Prompt):
    prompt = user_Prompt
    image = pipe(prompt).images[0]
    image.save("images/gen/stable_diffusion.png")
    return "images/gen/stable_diffusion.png"

    