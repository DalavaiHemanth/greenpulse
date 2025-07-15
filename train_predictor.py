import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle
import os

# --- Generate synthetic training data ---
data = []
for i in range(1000):
    usage = round(0.5 + 2.5 * (i % 100) / 100, 2)
    overuse = 1 if usage > 2.0 else 0
    data.append([usage, overuse])

df = pd.DataFrame(data, columns=["usage", "overuse"])

# --- Split data ---
X = df[["usage"]]
y = df["overuse"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Train model ---
model = LogisticRegression()
model.fit(X_train, y_train)

# --- Evaluate ---
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# --- Save model ---
os.makedirs("model", exist_ok=True)
with open("model/predictor.pkl", "wb") as f:
    pickle.dump(model, f)
print("Model saved to model/predictor.pkl")
