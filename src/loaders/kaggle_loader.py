
import pandas as pd

def load_security_misconfig_dataset(file_path: str) -> pd.DataFrame:
    """Load misconfiguration dataset from Kaggle CSV."""
    df = pd.read_csv(file_path)
    df.dropna(subset=['description'], inplace=True)
    return df
