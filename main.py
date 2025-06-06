# main.py

from env_loader import load_credentials
from navigator import resolve_site_id
from extractors import extract_data
from dotenv import load_dotenv

def main():
    print("🧪 [1] Loading credentials and populating .env...")
    if not load_credentials("credentials.txt"):
        exit("❌ Failed to load credentials. Aborting.")

    load_dotenv(override=True)

    print("🧭 [2] Resolving SharePoint site ID...")
    site_id = resolve_site_id()
    if not site_id:
        exit("❌ Failed to resolve site. Check .env and SharePoint settings.")

    print(f"✅ Ready for extraction. Site ID: {site_id}")
    print("📥 [3] Beginning data extraction...")
    extract_data(site_id)

if __name__ == "__main__":
    main()
