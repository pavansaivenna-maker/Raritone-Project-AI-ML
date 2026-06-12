import os
from torchvision import transforms
from PIL import Image

class TryOnDatasetPrep:
    def __init__(self, target_size=(512, 384)):
        self.target_size = target_size
        self.transform_pipeline = transforms.Compose([
            transforms.Resize(self.target_size),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])

    def prepare_directory(self, input_dir: str, output_dir: str):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for filename in os.listdir(input_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(input_dir, filename)
                img = Image.open(img_path).convert('RGB')
                tensor_img = self.transform_pipeline(img)
                save_img = transforms.ToPILImage()(tensor_img * 0.5 + 0.5)
                save_img.save(os.path.join(output_dir, filename))

if __name__ == "__main__":
    prep = TryOnDatasetPrep()
    prep.prepare_directory("processed_data/", "model_ready_data/")