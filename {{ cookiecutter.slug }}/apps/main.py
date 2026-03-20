from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .config import settings
from .routers import pages

app = FastAPI()

# 1. HTTPS redirect
if settings.HTTPS_REDIRECT:
    app.add_middleware(HTTPSRedirectMiddleware)

# 2. Trusted host validation
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS,
)

# 3. CORS policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

app.mount(settings.STATIC_URL, StaticFiles(directory=settings.STATIC_DIR), name="static")

app.include_router(pages.router)
