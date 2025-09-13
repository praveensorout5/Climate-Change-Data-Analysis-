import pandas as pd

def load_data(file_path: str):
    """Load ESG dataset from CSV and drop missing values."""
    df = pd.read_csv(file_pathpython)
    df.dropna(inplace=True)
    return df

if __name__ == "__main__":
    df = load_data("../data/esg_data.csv")
    print("Sample Data:")
    print(df.head())
