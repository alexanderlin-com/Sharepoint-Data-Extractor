import os
import platform
from tkinter import filedialog

def get_secure_credentials_path():
    """
    Returns the OS-appropriate secure path for credentials.txt.
    Does not check if the file exists — this is just a locator.
    """
    system = platform.system()

    if system == "Windows":
        return os.path.expandvars(r"%APPDATA%\SharePointExtractor\credentials.txt")
    elif system == "Darwin":  # macOS
        return os.path.expanduser("~/Library/Application Support/SharePointExtractor/credentials.txt")
    else:  # Assume Linux or Unix
        return os.path.expanduser("~/.sharepoint_extractor/credentials.txt")

def credentials_file_exists():
    """
    Utility function to check if the credentials file actually exists.
    """
    path = get_secure_credentials_path()
    return os.path.isfile(path)

def read_credentials_path():
    """
    Ensures the secure path exists before returning it.
    Raises FileNotFoundError if the file is missing.
    """
    path = get_secure_credentials_path()
    if not os.path.isfile(path):
        raise FileNotFoundError(f"credentials.txt not found at: {path}")
    return path

def prompt_user_for_credentials():
    """
    Opens a file dialog for the user to manually select a credentials.txt file.
    Returns the path if selected, else None.
    """
    return filedialog.askopenfilename(
        title="Select credentials.txt",
        filetypes=[("Text Files", "*.txt")]
    )
