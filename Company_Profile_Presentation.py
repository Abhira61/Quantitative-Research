import pandas as pd
from sklearn.ensemble import RandomForestClassifier

data = pd.read_csv("Loan_Data.csv")

X = data.drop(columns=["customer_id", "default"])
y = data["default"]

model = RandomForestClassifier(random_state=42)
model.fit(X, y)

raw_probs = model.predict_proba(X)[:, 1]
min_prob = 0.05 

adjusted_probs = [max(prob, min_prob) for prob in raw_probs]
data["predicted_prob"] = adjusted_probs

recovery_rate = 0.10
data["expected_loss"] = (data["predicted_prob"] * (1 - recovery_rate) * data["loan_amt_outstanding"]).round(2)

print(data[["customer_id", "default", "predicted_prob", "loan_amt_outstanding", "expected_loss"]].head(10))

data.to_csv("Loan_Data_with_Expected_Loss.csv", index=False)
