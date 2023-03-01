from fastapi import FastAPI
from fastapi.responses import FileResponse
from datamodel import ImageInfo
import os
from model import SDModel
import threading
from config import Config


config = Config('config/config.yaml')

app = FastAPI()

model = SDModel(model_path=config.model_path, save_path=config.save_path, device=config.device)

@app.post("/")
async def submit_job(image_info: ImageInfo):
    if not image_info.prompt:
        return None
    print(image_info.prompt)
    threading.Thread(target=model.get_and_save_images_from_prompt, kwargs={'image_info': image_info, 'save_path': config.save_path, 'quality': config.jpg_quality}).start()
    return {'job_id': model.get_job_id()}

@app.get("/status/{job_id}")
async def get_job_status(job_id: int):
    return {'id': int(job_id), 'status': model.get_job_status(job_id)}

@app.get("/{job_id}/{image_id}")
async def get_image(job_id: int, image_id: int):
    if model.get_job_status(int(job_id)) == 'Done':
        return FileResponse(os.path.join(config.generated_image_save_path, model.get_image_name_from_id(job_id, image_id)))
    else:
        return None
