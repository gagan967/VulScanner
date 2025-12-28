import time
from app.scanner import scan_installed_software
from app.cve_fetcher import fetch_cves
from app.database import SessionLocal, engine
from app import models

def run_scan():
    print("Starting scheduled scan...")
    # Ensure tables exist
    models.Base.metadata.create_all(bind=engine)
    
    software_list = scan_installed_software()
    print(f"Found {len(software_list)} installed software items.")
    
    db = SessionLocal()
    try:
        for sw in software_list:
            name = sw['name']
            print(f"Checking vulnerabilities for: {name}")
            cves = fetch_cves(name)
            
            for cve in cves:
                cve_id = cve['cve_id']
                # Logic: Mock Professional Patching
                sanitized_name = name.replace(" ", "_").lower()
                mock_url = f"http://patches.internal.corp/{sanitized_name}/v_latest_stable.exe"
                mock_instructions = f"1. Download patch from authorized repo.\n2. Run {sanitized_name}_update.exe as Administrator.\n3. Restart application."
                
                final_patch_cmd = f"Mock Fix: {mock_url}|{mock_instructions}"

                exists = db.query(models.Vulnerability).filter_by(cve_id=cve_id).first()
                if not exists:
                    print(f"  -> New vulnerability found: {cve_id} ({cve['severity']})")
                    v = models.Vulnerability(
                        cve_id=cve_id,
                        software_name=name,
                        affected_version=sw['version'],
                        severity=cve['severity'],
                        patch_command=final_patch_cmd,
                        published_date=sw['published_date']
                    )
                    db.add(v)
                else:
                    # UPDATE existing record to ensure new Mock logic is applied
                    if exists.patch_command != final_patch_cmd:
                        print(f"  -> Updating patch info for: {cve_id}")
                        exists.patch_command = final_patch_cmd
                        
            db.commit()
    except Exception as e:
        print(f"Scan cycle failed: {e}")
    finally:
        db.close()
    print("Scan complete.")

def update_all_existing_patch_commands():
    """Forces all existing DB records to use the new Mock format"""
    print("Running one-time database update for Mock Patches...")
    db = SessionLocal()
    try:
        vulns = db.query(models.Vulnerability).all()
        count = 0
        for v in vulns:
            # Re-generate mock command
            sanitized_name = v.software_name.replace(" ", "_").lower()
            mock_url = f"http://patches.internal.corp/{sanitized_name}/v_latest_stable.exe"
            mock_instructions = f"1. Download patch from authorized repo.\n2. Run {sanitized_name}_update.exe as Administrator.\n3. Restart application."
            new_cmd = f"Mock Fix: {mock_url}|{mock_instructions}"
            
            if v.patch_command != new_cmd:
                v.patch_command = new_cmd
                count += 1
        db.commit()
        print(f"Updated {count} records to Mock format.")
    except Exception as e:
        print(f"Migration failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Continuous Vulnerability Scanner Service Started")
    # Run the migration once on startup
    update_all_existing_patch_commands()
    
    while True:
        run_scan()
        # Sleep for 1 hour (3600 seconds)
        print("Sleeping for 1 hour...")
        time.sleep(3600)
