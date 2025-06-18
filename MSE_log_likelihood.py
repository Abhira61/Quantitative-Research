import pandas as pd
import numpy as np

def log_likelihood(defaults, i, j):
    k, n = np.sum(defaults[i:j+1]), j - i + 1
    if k == 0 or k == n: return 0
    p = k / n
    return k * np.log(p) + (n - k) * np.log(1 - p)

def find_boundaries(fico, defaults, num_buckets):
    idx = np.argsort(fico)
    fico, defaults = fico[idx], defaults[idx]
    n = len(fico)
    dp = np.full((num_buckets, n), -np.inf)
    split = np.full((num_buckets, n), -1)

    for i in range(n): dp[0][i] = log_likelihood(defaults, 0, i)

    for b in range(1, num_buckets):
        for i in range(b, n):
            for j in range(b-1, i):
                score = dp[b-1][j] + log_likelihood(defaults, j+1, i)
                if score > dp[b][i]:
                    dp[b][i], split[b][i] = score, j

    boundaries = []
    i = n - 1
    for b in reversed(range(1, num_buckets)):
        i = split[b][i]
        boundaries.append(fico[i])
    return sorted(boundaries)

def assign_ratings(fico, boundaries):
    return np.digitize(fico, boundaries, right=True)

df = pd.read_csv("loan_data.csv")
fico = df["fico_score"].values
defaults = df["default"].values

boundaries = find_boundaries(fico, defaults, num_buckets=4)
df["risk_rating"] = assign_ratings(fico, boundaries)

print("Boundaries:", boundaries)
print(df[["customer_id", "fico_score", "default", "risk_rating"]])
df.to_csv("loan_data_with_ratings.csv", index=False)
