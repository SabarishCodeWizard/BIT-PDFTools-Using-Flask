from flask import Blueprint, render_template, request, send_from_directory, jsonify
import os
import uuid
from werkzeug.utils import secure_filename
import requests

# Create a Blueprint for image upload
image_upload_bp = Blueprint("image_upload", __name__)

# Define the upload folder (renamed from "uploads" to "user_images")
IMAGE_FOLDER = "user_images"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# Ensure the folder exists
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@image_upload_bp.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if "file" not in request.files:
            return jsonify({"error": "No file part"})

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No selected file"})

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = str(uuid.uuid4()) + "_" + filename
            filepath = os.path.join(IMAGE_FOLDER, unique_filename)
            file.save(filepath)

            # Generate a shareable link
            image_url = request.url_root + "images/" + unique_filename

            # Shorten the URL using is.gd API
            short_url_response = requests.get(f"https://is.gd/create.php?format=simple&url={image_url}")
            short_url = short_url_response.text

            return jsonify({
                "success": True,
                "url": image_url,
                "short_url": short_url
            })

    return render_template("upload.html")

@image_upload_bp.route("/images/<filename>")
def uploaded_file(filename):
    return send_from_directory(IMAGE_FOLDER, filename)
