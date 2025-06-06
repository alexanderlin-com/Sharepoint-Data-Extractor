import os
import requests
from dotenv import load_dotenv
from msal import ConfidentialClientApplication

load_dotenv()

def resolve_site_id():
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    TENANT_ID = os.getenv("TENANT_ID")
    SHAREPOINT_HOSTNAME = os.getenv("SHAREPOINT_HOSTNAME")
    SHAREPOINT_SITE_NAME = os.getenv("SHAREPOINT_SITE_NAME")

    if not all([CLIENT_ID, CLIENT_SECRET, TENANT_ID, SHAREPOINT_HOSTNAME, SHAREPOINT_SITE_NAME]):
        print("❌ Missing one or more required environment variables.")
        return None

    AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
    SCOPE = ["https://graph.microsoft.com/.default"]

    app = ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=AUTHORITY
    )

    token_response = app.acquire_token_for_client(scopes=SCOPE)
    if "access_token" not in token_response:
        print("❌ Failed to get access token")
        return None

    ACCESS_TOKEN = token_response["access_token"]
    headers = { "Authorization": f"Bearer {ACCESS_TOKEN}" }

    search_url = f"https://graph.microsoft.com/v1.0/sites/{SHAREPOINT_HOSTNAME}/sites?search={SHAREPOINT_SITE_NAME}"
    response = requests.get(search_url, headers=headers)

    if response.status_code != 200:
        print("❌ Site search failed:", response.status_code)
        print(response.json())
        return None

    sites = response.json().get("value", [])
    if not sites:
        print(f"❌ No site found matching '{SHAREPOINT_SITE_NAME}'")
        return None

    # Return the first matching site
    site_id = sites[0]["id"]
    print(f"✅ Found site: {sites[0]['name']} — {site_id}")
    return site_id
