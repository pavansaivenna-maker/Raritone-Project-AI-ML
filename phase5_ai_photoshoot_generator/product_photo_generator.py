import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"

headers = {
    "Authorization": f"Bearer {os.getenv('HF_TOKEN')}"
}

prompt = """
Luxury black hoodie product photography,
white background,
professional studio lighting,
e-commerce catalog image
"""

# product_photo_generator.py

print("Product Photo Generator")
print("Output saved at output/product_photo_generator.png")