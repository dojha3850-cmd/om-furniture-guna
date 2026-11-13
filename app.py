import os, sqlite3, uuid
from pathlib import Path
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename

ROOT = Path(__file__).resolve().parent
UPLOADS = ROOT / "static" / "uploads"
UPLOADS.mkdir(parents=True, exist_ok=True)
DB = ROOT / "om_furniture.db"
ALLOWED = {"jpg", "jpeg", "png", "webp", "gif"}

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 12 * 1024 * 1024

def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with db() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS enquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
            phone TEXT NOT NULL, message TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
        con.execute("""CREATE TABLE IF NOT EXISTS photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT NOT NULL,
            caption TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/api/enquiries")
def enquiry():
    data = request.get_json(silent=True) or {}
    name, phone, message = (str(data.get(k, "")).strip() for k in ("name", "phone", "message"))
    if not name or not phone or not message:
        return jsonify(error="Name, phone and message are required"), 400
    with db() as con:
        con.execute("INSERT INTO enquiries(name, phone, message) VALUES(?,?,?)", (name[:100], phone[:30], message[:3000]))
    return jsonify(ok=True), 201

@app.get("/api/photos")
def photos():
    with db() as con:
        rows = con.execute("SELECT filename, caption, created_at FROM photos ORDER BY id DESC").fetchall()
    return jsonify([{"url": f"/static/uploads/{r['filename']}", "caption": r["caption"] or "", "created_at": r["created_at"]} for r in rows])

@app.post("/api/photos")
def upload_photo():
    f = request.files.get("photo")
    if not f or not f.filename:
        return jsonify(error="Choose a photo"), 400
    ext = f.filename.rsplit(".", 1)[-1].lower() if "." in f.filename else ""
    if ext not in ALLOWED:
        return jsonify(error="Only JPG, PNG, WEBP and GIF images are allowed"), 400
    filename = f"{uuid.uuid4().hex}.{ext}"
    f.save(UPLOADS / secure_filename(filename))
    caption = str(request.form.get("caption", "")).strip()[:180]
    with db() as con:
        con.execute("INSERT INTO photos(filename, caption) VALUES(?,?)", (filename, caption))
    return jsonify(ok=True), 201

@app.get("/health")
def health():
    return jsonify(status="ok")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
