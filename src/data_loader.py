"""
data_loader.py
---------------
Funktionen zum Laden und Bereinigen des E-Commerce-Datensatzes.
Getrennt vom Notebook, damit die Logik testbar und wiederverwendbar ist.
"""

from pathlib import Path
import pandas as pd
import numpy as np

RAW_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "online_retail_sales.csv"
PROCESSED_PATH = Path(__file__).resolve().parent.parent / "data" / "processed" / "sales_clean.csv"


def load_raw_data(path: Path = RAW_PATH) -> pd.DataFrame:
    """Lädt die Rohdaten von der Festplatte."""
    df = pd.read_csv(path, parse_dates=["order_date"])
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Bereinigt den Rohdatensatz:
      - entfernt exakte Duplikate
      - normalisiert Kategorienamen (Groß-/Kleinschreibung, Leerzeichen)
      - entfernt unplausible Werte (z.B. negative Mengen)
      - ergänzt fehlende numerische Werte mit dem Median (dokumentiert, nicht "versteckt")
      - berechnet abgeleitete Spalten (Umsatz je Bestellung)
    """
    df = df.copy()

    # 1. Duplikate entfernen
    n_before = len(df)
    df = df.drop_duplicates()
    n_after = len(df)
    print(f"Duplikate entfernt: {n_before - n_after}")

    # 2. Kategorien normalisieren
    df["product_category"] = df["product_category"].str.strip().str.title()

    # 3. Unplausible Werte entfernen (z.B. negative Mengen)
    invalid_qty = df["quantity"] < 0
    print(f"Zeilen mit negativer Menge entfernt: {invalid_qty.sum()}")
    df = df.loc[~invalid_qty].copy()

    # 4. Fehlende Werte behandeln
    df["customer_age"] = df["customer_age"].fillna(df["customer_age"].median())
    df["shipping_cost"] = df["shipping_cost"].fillna(df["shipping_cost"].median())
    # Bewertung: fehlend = keine Bewertung abgegeben -> eigene Kategorie
    df["customer_rating"] = df["customer_rating"].fillna(-1)

    # 5. Abgeleitete Kennzahlen
    df["revenue"] = df["quantity"] * df["unit_price"] * (1 - df["discount_percent"] / 100)
    df["order_month"] = df["order_date"].dt.to_period("M").astype(str)
    df["order_weekday"] = df["order_date"].dt.day_name()

    return df.reset_index(drop=True)


def save_processed(df: pd.DataFrame, path: Path = PROCESSED_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Bereinigte Daten gespeichert unter: {path}")


if __name__ == "__main__":
    raw = load_raw_data()
    clean = clean_data(raw)
    save_processed(clean)
