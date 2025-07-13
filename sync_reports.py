import os
import shutil

# Define paths
SOURCE_DIR = os.path.join(os.path.dirname(__file__), "forecasts")
DEST_DIR = os.path.join(os.path.dirname(__file__), "..", "forecasting_webapp", "static", "reports")

def sync_reports():
    for root, _, files in os.walk(SOURCE_DIR):
        for f in files:
            if f.endswith(".txt"):
                source_file = os.path.join(root, f)
                rel_path = os.path.relpath(source_file, SOURCE_DIR)
                dest_file = os.path.join(DEST_DIR, rel_path)

                dest_folder = os.path.dirname(dest_file)
                os.makedirs(dest_folder, exist_ok=True)

                # Copy only if new or changed
                if not os.path.exists(dest_file) or os.path.getmtime(source_file) > os.path.getmtime(dest_file):
                    shutil.copy2(source_file, dest_file)
                    print(f"Copied: {rel_path}")

if __name__ == "__main__":
    sync_reports()
    print("✅ Sync complete.")
