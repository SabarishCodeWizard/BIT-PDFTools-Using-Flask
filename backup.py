from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Use a different folder instead of "uploads"
IMAGE_FOLDER = "user_images"
app.config["UPLOAD_FOLDER"] = IMAGE_FOLDER
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif"}

# Ensure the folder exists
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = str(uuid.uuid4()) + "_" + filename
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
        file.save(filepath)
        
        # Generate URL for the uploaded image
        image_url = request.url_root + "images/" + unique_filename
        return jsonify({"success": True, "url": image_url})

    return jsonify({"error": "Invalid file type"})

@app.route("/images/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True)
