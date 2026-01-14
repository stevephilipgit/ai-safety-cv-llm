import zipfile
import os

def create_zip(zip_path, files):
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for f in files:
            zipf.write(f, arcname=os.path.basename(f))
    return zip_path
