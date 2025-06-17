from flask import Flask, request, Response
from datetime import datetime
import os
import requests

app = Flask(__name__)
SCRIPTS_FOLDER = "scripts"
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycby_QpaF75QTHhXWxpNPmjsnylyM_8RBDGIbHT3-FygJPGLs1kikJDEkufHHe18kJ1o7vg/exec"
PASSWORD = "FG@RL5851"

@app.route("/get_script")
def get_script():
    script_name = request.args.get("script", "").strip()
    guid = request.args.get("guid", "").strip()
    password = request.args.get("password", "").strip()

    if not script_name or not guid or not password:
        return Response("Missing script, guid or password", 400)

    if password != PASSWORD:
        return Response("AUTH FAILED: Wrong password.", 403)

    # Step 2: Validate with Google Sheet
    try:
        res = requests.get(GOOGLE_SCRIPT_URL, params={"script": script_name, "guid": guid})
        if res.status_code != 200:
            return Response("Cannot reach Google Script", 502)

        data = res.json()
        run = data.get("run", False)
        shutdown = data.get("shutdown", False)

        if shutdown:
            return Response("SHUTDOWN", 403)

        if not run:
            return Response("NOT ALLOWED TO RUN", 403)

    except Exception as e:
        return Response(f"ERROR contacting Google Script: {str(e)}", 500)

    # Step 3: Get Python script content
    script_path = os.path.join(SCRIPTS_FOLDER, f"{script_name}.py")
    if not os.path.isfile(script_path):
        return Response("Script not found", 404)

    with open(script_path, "r", encoding="utf-8") as f:
        logic = f.read()

    print(f"[{datetime.utcnow()}] Script: {script_name} | GUID: {guid} | AUTHORIZED")
    return Response(logic, mimetype="text/plain")

@app.route("/")
def home():
    return "Python central script server running."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
