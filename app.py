import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from multiprocessing import Pool
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from utils.nlp import Tensorbot
from utils.controller import OriginPathFollow
from utils.conn_db import get_list_target, retrieval_coordinates
from utils.search_algorithm import search_func
import ssl
import sys
import socket
import os
from pathlib import Path
import numpy as np
import re

HOST = socket.gethostbyname(socket.gethostname())
FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]
WORK_DIR = os.path.dirname(ROOT)

PATTERN = get_list_target()

app = FastAPI()
app.mount("/static", StaticFiles(directory=f"{WORK_DIR}/Tensorbot/static"), name="static")
templates = Jinja2Templates(directory= f"{WORK_DIR}/Tensorbot/templates")
tensorbot = Tensorbot()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
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
    response, tag = tensorbot.feed_back(text)
    if tag == "moving":
        current_point = retrieval_coordinates("tensorbot")
        target = re.findall(PATTERN, text.lower())
        # path1 = np.array([[0,0],[0.5,0],[1,0.5],[2,-0.2],[3,0],[0,0]])
        # OriginPathFollow(path1, 4)
        if target:
            print("#################", type(retrieval_coordinates(target[0])) )
            target_point = retrieval_coordinates(target[0])
            path_to_running = search_func.Astar_search(current_point,target_point)
            print(path_to_running)

            running_flag = 1
            # while running_flag:
            #     print("Running OriginPathFollow")

            # OriginPathFollow()
    return JSONResponse(content={"answer": response})

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True, workers=Pool()._processes)


