from flask import Flask, request, render_template
import pickle
import re

app = Flask(__name__)

# Load model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# ---------------------------
# URL SAFETY CHECK FUNCTION
# ---------------------------
def check_url_safety(url):
    suspicious_patterns = [
        "bit.ly", "tinyurl", "@", "-", "login", "verify", "update"
    ]

    for pattern in suspicious_patterns:
        if pattern in url.lower():
            return "Suspicious"
    return "Safe"

# ---------------------------
# HOME ROUTE
# ---------------------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------------------
# PREDICTION ROUTE
# ---------------------------
@app.route("/predict_web", methods=["POST"])
def predict_web():

    # Get input
    email_text = request.form["email"]

    # Convert to ML format
    email_vector = vectorizer.transform([email_text])

    # Predict
    prediction = model.predict(email_vector)
    probability = model.predict_proba(email_vector)

    confidence = max(probability[0]) * 100

    result = "Phishing" if prediction[0] == 1 else "Safe"

    # ---------------------------
    # RISK LEVEL
    # ---------------------------
    if confidence < 50:
        risk = "LOW"
    elif confidence < 80:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    # ---------------------------
    # URL CHECK
    # ---------------------------
    links = re.findall(r'https?://\S+', email_text)

    checked_links = []
    for link in links:
        status = check_url_safety(link)
        checked_links.append({
            "url": link,
            "status": status
        })

    # ---------------------------
    # ATTACHMENT CHECK
    # ---------------------------
    attachment_patterns = [".exe", ".zip", ".rar", ".bat", ".js"]

    attachments_found = []
    for pattern in attachment_patterns:
        if pattern in email_text.lower():
            attachments_found.append(pattern)

    # ---------------------------
    # SEND TO HTML
    # ---------------------------
    return render_template(
        "index.html",
        result=result,
        confidence=f"{confidence:.2f}%",
        risk=risk,
        links=checked_links,
        attachments=attachments_found
    )

# ---------------------------
# RUN SERVER
# ---------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
