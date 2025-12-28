import requests

def fetch_cves(software_name):
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={software_name}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching CVEs for {software_name}: {e}")
        return []

    vulnerabilities = []
    for item in data.get("vulnerabilities", []):
        try:
            cve_item = item.get("cve", {})
            cve_id = cve_item.get("id")
            
            # Safe access to metrics
            metrics = cve_item.get("metrics", {})
            cvss_v31 = metrics.get("cvssMetricV31", [])
            
            if cvss_v31:
                severity = cvss_v31[0].get("cvssData", {}).get("baseSeverity", "UNKNOWN")
            else:
                severity = "UNKNOWN"

            # Extract References for Patch URL
            # Extract References for Patch URL
            references = cve_item.get("references", [])
            patch_url = None
            
            # Priority 1: Look for "tags" containing "Patch"
            for ref in references:
                tags = ref.get("tags", [])
                if "Patch" in tags:
                    patch_url = ref.get("url")
                    break
            
            # Priority 2: Look for "Vendor Advisory"
            if not patch_url:
                for ref in references:
                    tags = ref.get("tags", [])
                    if "Vendor Advisory" in tags:
                        patch_url = ref.get("url")
                        break
            
            # Priority 3: Fallback to first URL
            if not patch_url and references:
                patch_url = references[0].get("url")
            
            if not patch_url:
                patch_url = "Check vendor website"

            if cve_id:
                vulnerabilities.append({
                    "cve_id": cve_id,
                    "severity": severity,
                    "patch_url": patch_url
                })
        except (KeyError, IndexError):
            continue

    return vulnerabilities
