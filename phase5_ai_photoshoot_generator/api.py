from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Photoshoot Generator API"}

@app.get("/fashion-model")
def fashion_model():
    return {"status": "Fashion Model Generator Working"}

@app.get("/product-photo")
def product_photo():
    return {"status": "Product Photo Generator Working"}

@app.get("/lifestyle-image")
def lifestyle_image():
    return {"status": "Lifestyle Image Generator Working"}

@app.get("/marketing-image")
def marketing_image():
    return {"status": "Marketing Image Generator Working"}
