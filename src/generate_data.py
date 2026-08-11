"""
generate_data.py
-----------------
Erzeugt einen synthetischen, aber realistischen E-Commerce-Verkaufsdatensatz
für das EDA-Projekt. Der Datensatz enthält absichtlich typische
Datenqualitätsprobleme (fehlende Werte, Duplikate, inkonsistente
Kategorien, Ausreißer), damit der komplette EDA-Workflow (inkl.
Datenbereinigung) demonstriert werden kann.

Ausführen mit:
    python src/generate_data.py
"""

import numpy as np
import pandas as pd
from pathlib import Path

RANDOM_SEED = 42
N_ROWS = 5000

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "online_retail_sales.csv"


def generate_dataset(n_rows: int = N_ROWS, seed: int = RANDOM_SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    regions = ["Nord", "Süd", "Ost", "West", "Mitte"]
    categories = {
        "Elektronik": ["Kopfhörer", "Smartphone-Hülle", "USB-Kabel", "Powerbank", "Bluetooth-Lautsprecher"],
        "Mode": ["T-Shirt", "Jeans", "Sneaker", "Jacke", "Mütze"],
        "Haushalt": ["Kaffeemaschine", "Staubsauger", "Bettwäsche", "Pfannenset", "Lampe"],
        "Sport": ["Yogamatte", "Laufschuhe", "Fitnessband", "Trinkflasche", "Hantel"],
        "Bücher": ["Roman", "Sachbuch", "Kochbuch", "Kinderbuch", "Comic"],
    }
    payment_methods = ["Kreditkarte", "PayPal", "Rechnung", "Lastschrift", "Sofortüberweisung"]

    order_dates = pd.date_range("2023-01-01", "2024-12-31", freq="D")

    rows = []
    for i in range(n_rows):
        category = rng.choice(list(categories.keys()), p=[0.28, 0.27, 0.18, 0.15, 0.12])
        product = rng.choice(categories[category])

        base_prices = {"Elektronik": 45, "Mode": 30, "Haushalt": 55, "Sport": 35, "Bücher": 15}
        unit_price = float(np.round(rng.gamma(shape=3.0, scale=base_prices[category] / 3.0), 2))

        # Künstliche Ausreißer bei ca. 1.5% der Zeilen (z.B. Erfassungsfehler)
        if rng.random() < 0.015:
            unit_price *= rng.uniform(8, 20)

        quantity = int(rng.choice([1, 1, 1, 2, 2, 3, 4, 5], p=[0.35, 0.2, 0.1, 0.15, 0.08, 0.06, 0.04, 0.02]))
        discount_percent = float(rng.choice([0, 0, 0, 5, 10, 15, 20, 25], p=[0.4, 0.15, 0.1, 0.1, 0.1, 0.08, 0.05, 0.02]))

        customer_age = int(np.clip(rng.normal(38, 12), 18, 80))
        customer_rating = rng.choice([1, 2, 3, 4, 5], p=[0.03, 0.05, 0.12, 0.35, 0.45])

        delivery_days = int(np.clip(rng.normal(4, 2), 1, 21))
        shipping_cost = round(float(rng.choice([0.0, 2.99, 4.99, 6.99], p=[0.3, 0.3, 0.25, 0.15])), 2)

        order_date = rng.choice(order_dates)

        row = {
            "order_id": 100000 + i,
            "order_date": pd.Timestamp(order_date),
            "customer_id": int(rng.integers(1, 1800)),
            "customer_age": customer_age,
            "customer_region": rng.choice(regions),
            "product_category": category,
            "product_name": product,
            "quantity": quantity,
            "unit_price": unit_price,
            "discount_percent": discount_percent,
            "payment_method": rng.choice(payment_methods),
            "shipping_cost": shipping_cost,
            "delivery_days": delivery_days,
            "customer_rating": customer_rating,
            "is_returned": bool(rng.random() < 0.06),
        }
        rows.append(row)

    df = pd.DataFrame(rows)

    # --- Absichtliche Datenqualitätsprobleme einbauen ---

    # 1) Fehlende Werte
    for col, frac in [("customer_age", 0.04), ("customer_rating", 0.06), ("shipping_cost", 0.02)]:
        idx = rng.choice(df.index, size=int(len(df) * frac), replace=False)
        df.loc[idx, col] = np.nan

    # 2) Inkonsistente Schreibweisen bei Kategorien (Groß/Kleinschreibung, Leerzeichen)
    idx = rng.choice(df.index, size=int(len(df) * 0.05), replace=False)
    df.loc[idx, "product_category"] = df.loc[idx, "product_category"].str.upper()
    idx2 = rng.choice(df.index, size=int(len(df) * 0.03), replace=False)
    df.loc[idx2, "product_category"] = df.loc[idx2, "product_category"].astype(str) + " "

    # 3) Duplikate einfügen
    duplicate_rows = df.sample(n=int(len(df) * 0.01), random_state=seed)
    df = pd.concat([df, duplicate_rows], ignore_index=True)

    # 4) Negative/unrealistische Werte (Erfassungsfehler) bei wenigen Zeilen
    idx3 = rng.choice(df.index, size=5, replace=False)
    df.loc[idx3, "quantity"] = -1

    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)
    return df


if __name__ == "__main__":
    df = generate_dataset()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Datensatz erzeugt: {OUTPUT_PATH} ({len(df)} Zeilen, {df.shape[1]} Spalten)")
