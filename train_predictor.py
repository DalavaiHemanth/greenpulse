import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Simulated usage data
data = pd.DataFrame({
    'usage': [0.6, 1.5, 2.9, 3.2, 0.8, 1.0, 2.7, 3.5],
    'overuse': [0, 0, 1, 1, 0, 0, 1, 1]
})

model = RandomForestClassifier()
model.fit(data[['usage']], data['overuse'])

# Save the model
with open('model/predictor.pkl', 'wb') as f:
    pickle.dump(model, f)
