from flask import Flask, render_template, request, jsonify
import os
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
# Set the path to the templates folder
template_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "templates"))
app = Flask(__name__, template_folder=template_folder)

@app.route("/")
def index_get():
    return render_template("index.html")

@app.route("/predict", methods=['POST'])
def predict():
    text = request.get_json().get("message")  # Fix the spelling mistake here
    response = text
    message = {"answer": response}
    return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
