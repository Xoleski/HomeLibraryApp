from fastapi import FastAPI, Path
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from src.settings import settings


app = FastAPI()
app.add_middleware(
    middleware_class=ProxyHeadersMiddleware,
    trusted_hosts=("*", )
)
static = StaticFiles(directory=settings.BASE_DIR / "static")
app.mount(path="/static", app=static, name="static")
templating = Jinja2Templates(directory=settings.BASE_DIR / "templates")


@app.get(path="/", name="index")
async def index(request: Request):
    return templating.TemplateResponse(
        request=request,
        name="blog/index.html",
    )


@app.get(path='/login', name="login")
async def login(request: Request):
    return templating.TemplateResponse(
        request=request,
        name="blog/login.html",
    )


@app.get(path='/register', name="register")
async def register(request: Request):
    return templating.TemplateResponse(
        request=request,
        name="blog/register.html",
    )


@app.get(path="/{slug}", name="index")
async def index(request: Request, slug: str = Path(alias="slug")):
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
