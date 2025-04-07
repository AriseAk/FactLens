import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

# Load dataset
data = pd.read_csv("clickbait_dataset.csv")  # Columns: headline, description, domain, label

# Feature extraction using helpers.py functions
from help import extract_features

data['features'] = data.apply(lambda row: extract_features(row['headline'], row['description'], row['domain']), axis=1)

# Split data into training and testing sets
X = list(data['features'])
y = data['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train Random Forest Classifier
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Save trained model
with open("clickbait_model.pkl", "wb") as f:
    pickle.dump(model, f)
