from flask import Flask, request, jsonify, send_file,render_template,Response
from test3 import process_frame
import numpy as np
from PIL import Image
import json
import traceback

# Optional: import your model or haze remover
# from haze_removal import HazeRemoval

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("test.html")

@app.route("/process", methods=["POST"])
def process_image():
    try:
        id = int(request.form["image"])
        json_data = process_frame(id)
        return Response(json.dumps(json_data), mimetype="application/json")

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.errorhandler(Exception)
def handle_exception(e):
    print("Flask internal error:", e)
    traceback.print_exc()
    return "Server Error", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)