import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

def train_and_save(df, target, filename):
    X = df.drop(target, axis=1)
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # 🔥 MODEL DEFINE KARO
    model = XGBClassifier()

    # TRAIN
    model.fit(X_train, y_train)

    # SAVE
    pickle.dump(model, open(filename, "wb"))

    print(f"{filename} saved successfully")

# ---------------- DIABETES ----------------
df = pd.read_csv("datasets/diabetes.csv")
train_and_save(df, "Outcome", "model/diabetes_model.pkl")

# ---------------- HEART ----------------
df = pd.read_csv("datasets/heart.csv")
train_and_save(df, "target", "model/heart_model.pkl")

# ---------------- PARKINSON ----------------
df = pd.read_csv("datasets/parkinsons.csv")

# remove string column
if "name" in df.columns:
    df = df.drop("name", axis=1)

train_and_save(df, "status", "model/parkinsons_model.pkl")