import os
import requests
import csv
from dotenv import load_dotenv
from msal import ConfidentialClientApplication

load_dotenv()

def extract_data(site_id: str):
    print("📦 Starting dynamic data extraction...")

    list_name = os.getenv("SHAREPOINT_LIST_NAME")
    field_string = os.getenv("SHAREPOINT_LIST_FIELDS", "")
    output_file = os.getenv("OUTPUT_FILENAME", "output.csv")

    if not list_name or not field_string:
        print("❌ List name or fields missing in .env")
        return

    fields_to_extract = [f.strip() for f in field_string.split(",")]

    access_token = authenticate()
    if not access_token:
        print("❌ Token retrieval failed.")
        return

    list_id = get_list_id(site_id, list_name, access_token)
    if not list_id:
        print("❌ Could not resolve list ID.")
        return

    items = get_list_items(site_id, list_id, access_token)
    if not items:
        print("❌ No list items found.")
        return

    output_rows = build_output_rows(items, fields_to_extract)

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(fields_to_extract)
        writer.writerows(output_rows)

    print(f"📄 Output written to {output_file}")
    print("✅ Data extraction complete.")

def authenticate():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    tenant_id = os.getenv("TENANT_ID")

    authority = f"https://login.microsoftonline.com/{tenant_id}"
    scope = ["https://graph.microsoft.com/.default"]

    app = ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_secret,
        authority=authority
    )

    token_response = app.acquire_token_for_client(scopes=scope)
    return token_response.get("access_token")

def get_list_id(site_id, list_name, token):
    url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{list_name}"
    headers = { "Authorization": f"Bearer {token}" }
    resp = requests.get(url, headers=headers)

    if resp.status_code != 200:
        print(f"❌ Failed to get list ID: {resp.status_code}")
        return None

    return resp.json().get("id")

def get_list_items(site_id, list_id, token):
    url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{list_id}/items?expand=fields"
    headers = { "Authorization": f"Bearer {token}" }
    resp = requests.get(url, headers=headers)

    if resp.status_code != 200:
        print(f"❌ Failed to get list items: {resp.status_code}")
        return []

    return resp.json().get("value", [])

def build_output_rows(items, fields_to_extract):
    seen = set()
    rows = []

    for item in items:
        fields = item["fields"]
        extracted_values = []

        for field in fields_to_extract:
            value = fields.get(field, "").strip()
            extracted_values.append(value)

        exploded = [val.split(",") if "," in val else [val] for val in extracted_values]

        for row in zip(*exploded):
            clean_row = tuple(col.strip() for col in row)
            if clean_row not in seen:
                rows.append(clean_row)
                seen.add(clean_row)

    return rows
