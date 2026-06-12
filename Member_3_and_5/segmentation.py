import os
from rembg import remove
from PIL import Image
import io

class GarmentSegmenter:
    def __init__(self):
        pass

    def process_image(self, input_path: str, output_path: str):
        try:
            with open(input_path, 'rb') as i:
                input_data = i.read()
            output_data = remove(input_data)
            img = Image.open(io.BytesIO(output_data)).convert("RGBA")
            img.save(output_path, 'PNG')
            return {"status": "success", "output_path": output_path}
        except Exception as e:
            return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    segmenter = GarmentSegmenter()
    result = segmenter.process_image("raw_data/tee_01.jpg", "processed_data/tee_01_seg.png")
    print(result)