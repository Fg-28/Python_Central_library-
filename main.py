from flask import Flask, request, send_file, Response
from datetime import datetime
import os, io, zipfile

app = Flask(__name__)
FOLDER_NAME = "AHK_Python"  # name of the folder to serve

@app.route("/")
def home():
    return f"{FOLDER_NAME} Python Setup Server is Running!"

@app.route("/get_python_setup")
def get_python_setup():
    script = request.args.get("script", "UNKNOWN")
    guid = request.args.get("guid", "UNKNOWN")

    print(f"[{datetime.utcnow()}] Setup requested | Script: {script} | GUID: {guid}")

    if not os.path.exists(FOLDER_NAME):
        return f"{FOLDER_NAME} folder not found on server", 404

    # Create zip in memory
    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(FOLDER_NAME):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, FOLDER_NAME)
                z.write(full_path, arcname=rel_path)
    mem_zip.seek(0)

    return send_file(mem_zip, mimetype="application/zip", as_attachment=True,
                     download_name=f"{FOLDER_NAME}.zip")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
