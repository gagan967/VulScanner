import sys
import os
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date

# Add 'backend' to sys.path so 'app' module can be found
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend"))

from app.database import SessionLocal
from app.models import Software, Vulnerability




# 1️⃣ Create a database session
db = SessionLocal()

# 2️⃣ Add a sample software entry
new_software = Software(
    name="ExampleApp",
    version="1.0.0",
    published_date=date.today()
)
db.add(new_software)
db.commit()
db.refresh(new_software)
print(f"Added Software: ID={new_software.id}, Name={new_software.name}, Version={new_software.version}")

# 3️⃣ Add a sample vulnerability
new_vuln = Vulnerability(
    cve_id="CVE-2025-0001",
    software_name="ExampleApp",
    affected_version="1.0.0",
    severity="High",
    patch_command="update ExampleApp",
    published_date=date.today()
)
db.add(new_vuln)
db.commit()
db.refresh(new_vuln)
print(f"Added Vulnerability: ID={new_vuln.id}, CVE={new_vuln.cve_id}, Severity={new_vuln.severity}")

# 4️⃣ Query all software
all_software = db.query(Software).all()
print("\nAll Software in DB:")
for s in all_software:
    print(f"ID={s.id}, Name={s.name}, Version={s.version}, Published={s.published_date}")

# 5️⃣ Query vulnerabilities for ExampleApp
vulns = db.query(Vulnerability).filter_by(software_name="ExampleApp").all()
print("\nVulnerabilities for ExampleApp:")
for v in vulns:
    print(f"ID={v.id}, CVE={v.cve_id}, Severity={v.severity}, Patch={v.patch_command}")

# 6️⃣ Close the session
db.close()
