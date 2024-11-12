from fastapi import FastAPI
from .routers import edsdata
app = FastAPI()

app.include_router(edsdata.router)
# @app.get('/test/')
# def index():
#     return {'msg':'fastapi Uvicorn Project Setup Completed Succesfully'}