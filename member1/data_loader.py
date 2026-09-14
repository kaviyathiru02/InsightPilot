from pathlib import Path
import pandas as pd


def load_data(file_path):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    extension = path.suffix.lower()

    if extension == ".csv":
        return pd.read_csv(path)

    if extension == ".xlsx":
        return pd.read_excel(path)

    raise ValueError(
        "Unsupported file format. Please upload a CSV or XLSX file."
    )