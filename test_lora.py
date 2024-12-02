from diffusers import DiffusionPipeline
import torch
import os
from random import randint

image_save_path: str = os.path.join('generated_images')
model_path = "./train_lora/pinterest_lora.safetensors"

pipe = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5",
                                         torch_dtype=torch.float16,
                                         safety_checker = None)
pipe.to("cuda")

pipe_with_lora = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5",
                                                   torch_dtype=torch.float16,
                                                   safety_checker=None)
pipe_with_lora.to("cuda")
pipe_with_lora.load_lora_weights(model_path)

image_count = 2
height = 1024
weight = 1024

while True:
    prompt = input('Prompt: ').strip()
    generator = torch.Generator(device="cuda").manual_seed(randint(0, 100_000_000))

    # generate images without LoRA
    images = pipe(prompt,
                 num_images_per_prompt=image_count,
                 width=height,
                 height=weight,
                 generator=generator,
                 num_inference_steps=20,
                 guidance_scale=3.5).images

    folder_name: str = prompt.lower().replace(',', '').replace(' ', '_').replace('__', '_')
    os.makedirs(os.path.join(image_save_path, folder_name), exist_ok=True)

    for index, image in enumerate(images):
        image.save(os.path.join(image_save_path, folder_name, f'{index}.png'))

    # generate images with LoRA
    images = pipe_with_lora(prompt,
                           num_images_per_prompt=image_count,
                           generator=generator,
                           width=height,
                           height=weight,
                           num_inference_steps=20,
                           guidance_scale=7.5).images
    
    for index, image in enumerate(images):
        image.save(os.path.join(image_save_path, folder_name, f'{index}_with_lora.png'))