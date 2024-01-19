import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from multiprocessing import Pool
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from utils.search_algorithm import search_func, search
from utils.nlp import Tensorbot
from utils.conn_db import *
from utils.controller import PathFollowing2
# from utils.sim_client import PathFollowing2
from utils.utils import speech_moving
import ssl
import sys
import socket
import os
from pathlib import Path
import numpy as np
import re
import asyncio
from datetime import datetime


HOST = socket.gethostbyname(socket.gethostname())
FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]
WORK_DIR = os.path.dirname(ROOT)

PATTERN = get_list_target()



app = FastAPI(docs_url=None, redoc_url=None)
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



@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )

@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )

@app.post("/predict")
async def predict(message: Message):
    try:
        global target_point, barrier_arr
        text = message.message
        text = re.sub(r'[^\w\s]', '',text)
        response, tag = tensorbot.feed_back(text)

        if tag == "moving":
            
            current_point = retrieval_coordinates("tensorbot")
            target = re.findall(PATTERN, text.lower())
            if target:
                target_point = retrieval_coordinates(target[0])
                barrier_arr = search.read_txt_file()

                async def process_movement():
                    nonlocal current_point


                    speech_moving(mode = "start")
                    while current_point != target_point:
                        path_to_running = search_func.Astar_search(current_point, target_point, barrier_arr)
                        speech_moving(mode = "found")
                        print("Path to running", path_to_running)
                        check_return = PathFollowing2(path_to_running)
                        print("Check return", check_return)

                        if len(check_return) >= 2:
                            barrier_arr.extend(barrier_i for barrier_i in check_return[1:] if barrier_i not in barrier_arr)
                            print("Update barrier", len(barrier_arr))

                        current_point = retrieval_coordinates("tensorbot")
                        print("Current point", current_point)
                        print("Dieu khien to break", current_point == target_point)
                        if current_point == target_point:
                            speech_moving(mode = "finish")

                # Chạy coroutine mà không chờ đợi
                asyncio.create_task(process_movement())
        elif tag == "info":
            target = re.findall(PATTERN, text.lower())
            response = retrieval_info(target[0])
        elif tag == "time":
            current_time = datetime.now()
            response = current_time.strftime("Day: %A, Date: %d/%m/%Y, Time: %H:%M")

        return JSONResponse(content={"answer": response})
    
    except:
        response = "Sorry, I don't understand"
        return JSONResponse(content={"answer": response})

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True, workers=Pool()._processes)