import pickle
import numpy as np
from flask import Flask, request, jsonify
from help import extract_features

app = Flask(__name__)

with open("clickbait_model.pkl", "rb") as f:
    ml_model = pickle.load(f)

@app.route("/predict_clickbait", methods=["POST"])
def predict_clickbait():
    try:
        data = request.json
        
        headline = data.get('headline', '')
        description = data.get('description', '')
        domain = data.get('domain', '')
        
        features = extract_features(headline, description, domain).reshape(1, -1)
        
        prediction = ml_model.predict(features)[0]
        
        return jsonify({"clickbait": bool(prediction)})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
