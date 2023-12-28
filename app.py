import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from multiprocessing import Pool
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import ssl
import sys
import socket
import os
from pathlib import Path


HOST = socket.gethostbyname(socket.gethostname())
FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]
WORK_DIR = os.path.dirname(ROOT)
print("WORK_DIR", WORK_DIR)


app = FastAPI(ssl_keyfile=f'{WORK_DIR}/Tensorbot/keyfile.pem', ssl_certfile=f"{WORK_DIR}/Tensorbot/certfile.pem")

app.mount("/static", StaticFiles(directory=f"{WORK_DIR}/Tensorbot/static"), name="static")

templates = Jinja2Templates(directory= f"{WORK_DIR}/Tensorbot/templates")


origins = [
    "https://localhost",
    "https://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Message(BaseModel):
    message: str

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
async def predict(message: Message):
    text = message.message
    response = text
    return JSONResponse(content={"answer": response})

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)


