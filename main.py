from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database.db_manager import init_db
from routers import food, chat, auth, dashboard, planner
import os

app = FastAPI(title="NutriBharat API", version="1.0.0")

# Initialize database on startup
@app.on_event("startup")
def on_startup():
    init_db()

# Include Routers
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(food.router)
app.include_router(chat.router)
app.include_router(planner.router)

# Mount static files for the frontend demo
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def read_root():
    """
    Serves the static frontend demo.
    """
    return FileResponse(os.path.join(static_dir, "index.html"))
