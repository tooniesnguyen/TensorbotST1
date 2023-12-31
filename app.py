import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from multiprocessing import Pool
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from utils.search_algorithm import search_func, search
from utils.nlp import Tensorbot
# from utils.controller import PathFollowing
from utils.conn_db import *
from utils.sim_client import PathFollowing
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
    


# def update_coor_robot(func):
#     def update_db(*args, **kwargs):
#         current_pos = func(*args, **kwargs)
#         print("Current_pos_to_db", current_pos)
#         try:
#             while True:
#                 current_pos_to_db = next(current_pos)
                
#                 if len(current_pos_to_db) <= 1:
#                     update_target_coordinates("Tensorbot",current_pos_to_db[0])
#                     print("In mode update ############################################################3")
#                 else:
#                     update_target_coordinates("Tensorbot",current_pos_to_db[0])
#                     barrier_arr.extend([current_pos_to_db[i] for i in range(1, len(current_pos_to_db))])
#                     current_point = retrieval_coordinates("tensorbot")
#                     path_to_running = search_func.Astar_search(current_point,target_point)
#                     func_Path_Following(path_to_running)
#                     print("Update block varibale and then run again A_Star")
#         except StopIteration:
#             print("Finish Loop")
#     return update_db

# @update_coor_robot
# def func_Path_Following(path):
#     PathFollowing(path)

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
async def predict(message: Message):
    global target_point, barrier_arr
    text = message.message
    response, tag = tensorbot.feed_back(text)
    if tag == "moving":
        current_point = retrieval_coordinates("tensorbot")
        target = re.findall(PATTERN, text.lower())
        if target:
            print("#################", type(retrieval_coordinates(target[0])) )
            target_point = retrieval_coordinates(target[0]) # return 1D
            barrier_arr = search.read_txt_file()
            while current_point != target_point:
                path_to_running = search_func.Astar_search(current_point,target_point,barrier_arr)
                print("Path to running", path_to_running)
                check_return = PathFollowing(path_to_running) # retu 2D
                if len(check_return)>= 2:
                    barrier_arr.extend(barrier_i for barrier_i in check_return[1:] if barrier_i not in barrier_arr)
                    print("Update barrier", len(barrier_arr))
                current_point = retrieval_coordinates("tensorbot")
                print("Currenr point", current_point)
                print("Dieu khien to brak", current_point == target_point)

                
    return JSONResponse(content={"answer": response})

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True, workers=Pool()._processes)


