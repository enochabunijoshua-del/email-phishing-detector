import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import pickle

# Step 1: Load dataset
data = pd.read_csv("phishing_dataset1.csv")

# Step 2: Check columns
print(data.head())

# CHANGE THIS depending on your dataset
X = data["text"]
y = data["label"]

# Step 3: Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Step 4: Convert text to numbers
vectorizer = TfidfVectorizer(stop_words="english")
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Step 5: Train model
model = MultinomialNB()
model.fit(X_train_vec, y_train)

# Step 6: Test model
y_pred = model.predict(X_test_vec)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Step 7: Save model
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

# Step 8: Test with your own email
def check_email(text):
    vec = vectorizer.transform([text])
    result = model.predict(vec)
    return "Phishing" if result[0] == 1 else "Safe"

print(check_email("hello, how are you doing today? The meeting is scheduled for 2pm today."))
