import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"

HF_TOKEN = os.getenv("HF_TOKEN")

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

prompt = """
Professional fashion model wearing a luxury black hoodie,
studio lighting,
realistic photography,
e-commerce fashion photoshoot.
"""

try:
    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": prompt},
        timeout=120
    )

    print("Status Code:", response.status_code)

    if response.status_code == 200:

        os.makedirs("output", exist_ok=True)

        with open("output/fashion_model.png", "wb") as f:
            f.write(response.content)

        print("Fashion model generated successfully!")

    else:
        print("Error:")
        print(response.text)

except Exception as e:
    print("Exception:", e)