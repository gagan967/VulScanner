from fastapi import APIRouter, HTTPException
import re

router = APIRouter()

@router.get("/patch")
def patch_command(software_name: str):
    # Basic sanitization: only allow alphanumeric, dashes, underscores, and dots
    if not re.match(r"^[a-zA-Z0-9.\-_]+$", software_name):
        raise HTTPException(status_code=400, detail="Invalid software name")

    return {
        "command": f"echo 'Please follow vendor instructions to patch: {software_name}'"
    }
