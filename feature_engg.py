import pandas as pd
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

def preprocess(df: pd.DataFrame):
    """Preprocess features and separate target ESG score."""
    if "ESG_Score" in df.columns:
        features = df.drop("ESG_Score", axis=1)
        target = df["ESG_Score"]
    else:
        features = df
        target = None

    features_scaled = scaler.fit_transform(features)
    return features_scaled, target
