from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import TemplateNotFound
from ..config import settings

router = APIRouter()

templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "pages/index.html",
        {"request": request, "title": "Home"}
    )


PAGES_DIR = Path(settings.TEMPLATES_DIR) / "pages"

@router.get("/{template_name}", response_class=HTMLResponse)
def dynamic_pages_view(request: Request, template_name: str):

    # Build and resolve path safely
    template_path = (PAGES_DIR / f"{template_name}.html").resolve()

    # Ensure resolved path is inside pages directory
    if not str(template_path).startswith(str(PAGES_DIR.resolve())):
        return templates.TemplateResponse(
            "pages/error-404.html",
            {"request": request},
            status_code=404
        )

    try:
        return templates.TemplateResponse(
            f"pages/{template_name}.html",
            {"request": request}
        )
    except TemplateNotFound:
        return templates.TemplateResponse(
            "pages/error-404.html",
            {"request": request},
            status_code=404
        )