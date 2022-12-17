import torch
from diffusers import StableDiffusionPipeline


def callback(step: int, timestep: int, latents: torch.FloatTensor):
    print(f'step: {step}, timestep: {timestep}')

#torch.cuda.set_per_process_memory_fraction(1.0, None)

pipe = StableDiffusionPipeline.from_pretrained("./stable-diffusion-v1-5")
#pipe = pipe.to('cuda')

prompt = "a photograph of an astronaut riding a horse"
image = pipe(prompt, num_images_per_prompt=1).images[0]

image.save("astronaut_rides_horse.png")