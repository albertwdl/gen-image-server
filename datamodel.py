from pydantic import BaseModel

class ImageInfo(BaseModel):
    prompt: str
    width: int = 512
    height: int = 512
    num_images_per_prompt: int = 1

class Job():
    job_id: int
    prompt: str