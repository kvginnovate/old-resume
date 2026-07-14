"""
Deploy docs/ to Netlify Drop — no account needed.
Run: python deploy_netlify.py
"""
import zipfile, os, urllib.request, json, sys

docs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
zip_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_deploy.zip")

# Create zip
print("Zipping docs/...")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for f in os.listdir(docs_dir):
        zf.write(os.path.join(docs_dir, f), f)
        print(f"  + {f}")

# Deploy
print("\nDeploying to Netlify...")
with open(zip_path, "rb") as f:
    req = urllib.request.Request(
        "https://api.netlify.com/api/v1/sites",
        data=f.read(),
        headers={"Content-Type": "application/zip", "Accept": "application/json"},
        method="POST",
    )

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
        url = data.get("ssl_url") or data.get("url")
        print(f"\n{'='*50}")
        print(f"LIVE URL: {url}")
        print(f"{'='*50}")
        print(f"Open this link in your browser to view your resume.")
except urllib.error.HTTPError as e:
    print(f"Error {e.code}: {e.read().decode()}")
finally:
    os.remove(zip_path)
    print("Cleaned up temp zip.")

input("\nPress Enter to exit...")
