from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .config import settings
from .routers import pages

app = FastAPI()

app.mount(settings.STATIC_URL, StaticFiles(directory=settings.STATIC_DIR), name="static")

app.include_router(pages.router)
