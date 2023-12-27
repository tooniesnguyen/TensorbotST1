import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse



app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("/home/toonies/Learn/Tensorbot/templates/index.html", "r") as f:
        content = f.read()
    return HTMLResponse(content=content)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0",port=8000)