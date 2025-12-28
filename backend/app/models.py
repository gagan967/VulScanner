from sqlalchemy import Column, Integer, String, Date
from app.database import Base

class Software(Base):
    __tablename__ = "software"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    published_date = Column(Date)

class Vulnerability(Base):
    __tablename__ = "vulnerabilities"

    id = Column(Integer, primary_key=True, index=True)
    cve_id = Column(String, nullable=False)
    software_name = Column(String, nullable=False)
    affected_version = Column(String, nullable=False)
    severity = Column(String)
    patch_command = Column(String)
    published_date = Column(Date)
