import os

def load_credentials(file_path="credentials.txt", env_path=".env"):
    if not os.path.exists(file_path):
        print(f"❌ Credentials file not found: {file_path}")
        return False

    print(f"📄 Loading credentials from: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    env_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "=" not in stripped:
            print(f"⚠️ Invalid line (skipped): {stripped}")
            continue
        key, value = stripped.split("=", 1)
        env_lines.append(f"{key.strip()}={value.strip()}")

    # Write to .env (overwrite safely)
    with open(env_path, "w", encoding="utf-8") as env_file:
        env_file.write("\n".join(env_lines) + "\n")

    print(f"✅ .env file updated with credentials.")
    return True
