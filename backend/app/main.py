from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import scan, patch, scans_db

app = FastAPI()

# Enable CORS for Angular frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scan.router)
app.include_router(patch.router)
app.include_router(scans_db.router)
