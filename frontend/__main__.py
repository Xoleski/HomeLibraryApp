from fastapi import FastAPI, Path
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request

from src.settings import settings


app = FastAPI()
static = StaticFiles(directory=settings.BASE_DIR / "static")
app.mount(path="/static", app=static, name="static")
templating = Jinja2Templates(directory=settings.BASE_DIR / "templates")



@app.get(path="/", name="index")
async def index(request: Request):
    return templating.TemplateResponse(
        request=request,
        name="blog/index.html",
    )


@app.get(path="/{id}", name="index")
async def index(request: Request, pk: int = Path(alias="id")):
    return templating.TemplateResponse(
        request=request,
        name="blog/index.html",
    )


if __name__ == '__main__':
    from uvicorn import run
    run(
        app=app,
        host=settings.HOST,
        port=settings.PORT
    )