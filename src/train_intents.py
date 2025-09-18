import json
import random
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load intents dataset
with open("data/research/intents.json", "r") as f:   # change to "data/intents.json" if you rename the file
    data = json.load(f)["intents"]

X, y, responses = [], [], {}
for intent in data:
    for p in intent["patterns"]:
        X.append(p)
        y.append(intent["tag"])
    responses[intent["tag"]] = intent["responses"]

# Train vectorizer + classifier
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)
clf = LogisticRegression(max_iter=1000).fit(X_vec, y)

# Ensure models directory exists
os.makedirs("models", exist_ok=True)

# Save model + vectorizer + responses
joblib.dump((vectorizer, clf, responses), "models/intent_model.pkl")

print("✅ Intent model trained and saved at models/intent_model.pkl")
