#instalacion fastapi: pip install "fastapi[all]"

from fastapi import FastAPI
from routers import users_db

app = FastAPI()

app.include_router(users_db.router)

@app.get("/")
async def root():
    return "Hola Bryan"

# Inicia el server: uvicorn main:app --reload
# Url local: http://127.0.0.1:8000/url
