from flask import Flask, render_template, request, jsonify
import os
from analyzer.chehredekhkebatane import shape_of_her

app=Flask(__name__, template_folder="../templates",static_folder="../static")

UPLOAD_FOLDER="uploads"
app.config["UPLOAD_FOLDER"]=UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")

def home():
    return render_template("recognise.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    if "image" not in request.files:
        return jsonify({"error":"No image uploaded"}),400
    
    file= request.files["image"]

    filepath=os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    result={
        "face_shape": "Analyzing...",
        "body_type": "Analyzing...",
        "skin_tone": "Analyzing...",
        "gender": "Detecting..."
    }
    return jsonify(result)

if __name__=="__main__":
    app.run(debug=True)