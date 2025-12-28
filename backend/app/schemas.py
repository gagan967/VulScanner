from pydantic import BaseModel
from datetime import date

class SoftwareSchema(BaseModel):
    name: str
    version: str
    published_date: date

class VulnerabilitySchema(BaseModel):
    cve_id: str
    severity: str
    patch_command: str
