from flask import Flask, request, jsonify, send_file,render_template
from test3 import process_frame
import numpy as np
from PIL import Image

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
        print(id)
        json_data = process_frame(id)
        print(json_data, flush=True)


        return jsonify(json_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)