from flask import Flask, render_template, request, jsonify
from display import EInkDisplay
import os
import logging

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

display = EInkDisplay()
display.init()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/reset")
def index():
    try:
        display.clear()
        return jsonify({"status": "success", "message": "Display reset"}), 200
    except Exception as e:
        logging.exception("Failed to reset display")
        return jsonify({"status": "error", "message": f"Failed to reset display: {str(e)}"}), 500
    

@app.route("/display", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"status": "error", "message": "No file part in request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"status": "error", "message": "No file selected"}), 400

    if file:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], "image.BMP")
        try:
            file.save(filepath)
            display.show_image(filepath)
            return jsonify({"status": "success", "message": "Image displayed!"}), 200
        except Exception as e:
            logging.exception("Failed to display image")
            return jsonify({"status": "error", "message": f"Failed to display image: {str(e)}"}), 500

    return jsonify({"status": "error", "message": "Unknown error occurred"}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
    display.close()
