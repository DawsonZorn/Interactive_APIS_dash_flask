from flask import Flask, jsonify, request, send_file
from fake_useragent import UserAgent
from PIL import Image
import io

app = Flask(__name__)

# Instructions to display on the index route
instructions = {
    "title": "Welcome to the Image Conversion and User-Agent Generator App",
    "description": "Available routes:",
    "routes": [
        {
            "method": "GET",
            "route": "/",
            "description": "Shows these instructions."
        },
        {
            "method": "POST",
            "route": "/convert",
            "description": "Upload an image to convert to a new format.",
            "supported_formats": ["JPEG", "PNG", "BMP", "TIFF"],
            "request_parameters": [
                {"parameter": "file", "description": "The image file to be converted."},
                {"parameter": "format", "description": "Desired output format (JPEG, PNG, BMP, TIFF)."}
            ]
        },
        {
            "method": "GET",
            "route": "/fake_user_agent",
            "description": "Generates a fake user-agent string.",
            "request_parameters": [
                {"parameter": "browser", "description": "Specify a browser type to generate a fake user agent for that browser. Options: chrome, firefox, safari, etc."}
            ]
        }
    ]
}

# Index route to display instructions in JSON format
@app.route("/", methods=["GET"])
def index():
    return jsonify(instructions)

# Route for image conversion
@app.route("/convert", methods=["POST"])
def convert_image():
    if "file" not in request.files or "format" not in request.form:
        return jsonify({"error": "Both file and format parameters are required."}), 400

    file = request.files["file"]
    output_format = request.form["format"].upper()

    # Validate output format
    if output_format not in ["JPEG", "PNG", "BMP", "TIFF"]:
        return jsonify({"error": f"Unsupported format '{output_format}'."}), 400

    # Convert the image using Pillow
    img = Image.open(file.stream)
    img_io = io.BytesIO()
    img.save(img_io, output_format)
    img_io.seek(0)

    return send_file(img_io, mimetype=f"image/{output_format.lower()}")

# Route for generating a fake user-agent
@app.route("/fake_user_agent", methods=["GET"])
def fake_user_agent():
    ua = UserAgent()
    browser = request.args.get("browser", "random")
    try:
        user_agent = getattr(ua, browser)
    except AttributeError:
        return jsonify({"error": "Invalid browser type."}), 400

    return jsonify({"browser": browser, "user_agent": user_agent})

if __name__ == "__main__":
    app.run(debug=True)
