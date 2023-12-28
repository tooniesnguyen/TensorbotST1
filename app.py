import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from multiprocessing import Pool
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# Mount the 'static' directory to serve static files
app.mount("/static", StaticFiles(directory="/home/toonies/Learn/Tensorbot/static"), name="static")

# Create an instance of Jinja2Templates and set the directory for templates
templates = Jinja2Templates(directory="/home/toonies/Learn/Tensorbot/templates")


origins = [
    "https://localhost",
    "https://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Adjust this to your specific frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Message(BaseModel):
    message: str

@app.get("/")
async def root(request: Request):
    # Render the HTML template using Jinja2Templates
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
async def predict(message: Message):
    text = message.message
    response = text
    return JSONResponse(content={"answer": response})

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)



# app = FLask(__name__)


# @app.get("/")
# def index_get():
#     return render_template("base.html")

# @app.post("/predict")
# def predict():
#     text = request.get_json().get("messenge")
#     respone = get_respone(text)
#     mess = {"answer": respone}
#     return jsonify(messenge)