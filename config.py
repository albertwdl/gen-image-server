import yaml

class Config():
    device: str = 'cpu'
    generated_image_save_path: str = './generated_content/images_transfer'
    model_path: str
    save_path: str = 'generated_content'
    jpg_quality: 95

    def __init__(self, config_file_path: str) -> None:
        with open(config_file_path, 'r') as f:
            yaml.load(f.read(), yaml.Loader)
            self.device = yaml['device']
            self.jpg_quality = yaml['jpg_quality']
            self.model_path = yaml['model_path']
            self.save_path = yaml['save_path']


