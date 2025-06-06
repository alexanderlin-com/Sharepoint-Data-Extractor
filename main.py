import tkinter as tk
import threading
from tkinter import scrolledtext
from env_loader import load_credentials
from navigator import resolve_site_id
from extractors import extract_data
from dotenv import load_dotenv
import os

class SharePointMain:
    def __init__(self, root):
        self.root = root
        self.root.title("SharePoint Data Extractor")
        self.root.geometry("600x400")

        tk.Label(root, text="SharePoint Extractor", font=("Arial", 16)).pack(pady=10)

        tk.Button(root, text="▶ Run Program", font=("Arial", 12), command=self.run_pipeline).pack(pady=5)

        self.status = tk.Label(root, text="", fg="green")
        self.status.pack(pady=5)

        self.console = scrolledtext.ScrolledText(root, height=15, bg="black", fg="lime", font=("Courier", 10))
        self.console.pack(padx=10, pady=10, fill="both", expand=True)
        self.console.config(state="disabled")

    def log_output(self, message):
        self.console.config(state="normal")
        self.console.insert(tk.END, message + "\n")
        self.console.see(tk.END)
        self.console.config(state="disabled")

    def run_pipeline(self):
        def task():
            try:
                self.status.config(text="🔄 Running pipeline...", fg="blue")
                self.console.config(state="normal")
                self.console.delete(1.0, tk.END)

                self.log_output("📄 Loading credentials.txt...")
                if not load_credentials():
                    self.log_output("❌ Failed to load credentials.")
                    self.status.config(text="❌ Failed", fg="red")
                    return

                load_dotenv(override=True)

                self.log_output("🧭 Resolving site ID...")
                site_id = resolve_site_id()
                if not site_id:
                    self.log_output("❌ Site ID resolution failed.")
                    self.status.config(text="❌ Failed", fg="red")
                    return

                self.log_output(f"✅ Site ID: {site_id}")
                self.log_output("📥 Extracting professor data...")
                extract_data(site_id)

                self.status.config(text="✅ Completed successfully", fg="green")

            except Exception as e:
                self.status.config(text=f"❌ Exception occurred", fg="red")
                self.log_output(f"Exception: {str(e)}")

        threading.Thread(target=task).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = SharePointMain(root)
    root.mainloop()
