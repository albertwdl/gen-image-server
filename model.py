import torch
from diffusers import StableDiffusionPipeline
from typing import List
from PIL import Image
from datamodel import ImageInfo
import os
# import queue


class SDModel():
    def __init__(self, model_path: str='./model/diffusers/chilloutmix', save_path:str = './generated_content', device: str = "cpu") -> None:
        self.pipe = StableDiffusionPipeline.from_pretrained(model_path, torch_dtype=torch.float16).to(device)
        self.status = 'Ready'
        # self.job_queue = queue.Queue()
        self.job_status_dict = {}
        images_list = os.listdir(os.path.join(save_path, 'images_save'))
        if len(images_list) > 0:
            images_list.sort()
            self.next_job_id = int(images_list[-1].split('-')[1]) + 1
        else:
            self.next_job_id = 0

    def get_images_from_prompt(self, image_info: ImageInfo) -> List[Image.Image]:
        job_id = self.next_job_id
        self.job_status_dict[job_id] = 'Runing'
        self.status = 'Runing'
        images = self.pipe(image_info.prompt, height=image_info.height, width=image_info.width, num_images_per_prompt=image_info.num_images_per_prompt).images
        self.status = 'Ready'
        self.job_status_dict[job_id] = 'Finish'
        self.next_job_id += 1
        return images
    
    def save_images(self, images: List[Image.Image], prompt: str, path: str="./generated_content", quality: int=95):
        image_id = 0
        job_id = self.next_job_id - 1
        for image in images:
            image.save(os.path.join(path, 'images_transfer', f'img-{job_id:05}-{image_id:03}.jpg'), quality=quality)
            image.save(os.path.join(path, 'images_save', f'img-{job_id:05}-{image_id:03}.png'))
            with open(os.path.join(path, 'images_info', 'images_info.log'), 'a') as f:
                f.writelines(f'{job_id},{image_id},{prompt}\n')
            image_id += 1
        self.job_status_dict[self.next_job_id - 1] = 'Done'

    def get_job_id(self):
        return self.next_job_id

    def get_job_status(self, job_id: int):
        return self.job_status_dict.setdefault(job_id, 'No Job')
    
    def get_image_name_from_id(self, job_id: int, image_id: int):
        return f'img-{job_id:05}-{image_id:03}.jpg'

    def get_and_save_images_from_prompt(self, image_info: ImageInfo, save_path: str='./generated_content', quality: int=95) -> List[Image.Image]:
        images = self.get_images_from_prompt(image_info)
        self.save_images(images, image_info.prompt, save_path, quality)
        return images


