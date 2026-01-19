## Quick Start

**Install uv**
```bash
pip install uv
```

**Sync environment (install deps into .venv)**
```bash
uv sync
```

**Run FastAPI (development)**
```bash
uv run uvicorn apps.main:app --reload
```

**Open browser**

- App: http://127.0.0.1:8000
- Docs: http://127.0.0.1:8000/docs 