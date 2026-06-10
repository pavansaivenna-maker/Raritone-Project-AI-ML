from fastapi import FastAPI
from recommendation import recommend

app = FastAPI(
    title="Raritone Cross Selling Recommendation API",
    version="1.0"
)

@app.get("/")
def home():
    return {
        "message": "Cross Selling Recommendation System"
    }

@app.get("/cross-sell/{product}")
def cross_sell(product: str):

    recommendations = recommend(product)

    return {
        "product": product,
        "recommendations": recommendations
    }