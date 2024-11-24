from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routers import edsdata
app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"),name="static")

app.include_router(edsdata.router)
# @app.get('/test/')
# def index():
#     return {'msg':'fastapi Uvicorn Project Setup Completed Succesfully'}