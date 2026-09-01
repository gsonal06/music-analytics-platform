from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Music Analytics Platform is running!"}