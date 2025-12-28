from fastapi import APIRouter
from app.scanner import scan_installed_software

router = APIRouter()

@router.get("/scan")
def scan_machine():
    software = scan_installed_software()
    return software
