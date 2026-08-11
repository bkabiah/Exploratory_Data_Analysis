"""
eda_utils.py
-------------
Wiederverwendbare Hilfsfunktionen für die explorative Datenanalyse (EDA):
Plots und einfache statistische Auswertungen.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

FIGURES_DIR = Path(__file__).resolve().parent.parent / "reports" / "figures"


def _save(fig, filename: str):
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURES_DIR / filename, bbox_inches="tight", dpi=120)


def missing_values_overview(df: pd.DataFrame) -> pd.DataFrame:
    """Gibt eine Tabelle mit Anzahl & Anteil fehlender Werte je Spalte zurück."""
    missing = df.isna().sum()
    percent = (missing / len(df) * 100).round(2)
    result = pd.DataFrame({"fehlende_werte": missing, "anteil_prozent": percent})
    return result[result["fehlende_werte"] > 0].sort_values("fehlende_werte", ascending=False)


def plot_missing_values(df: pd.DataFrame, filename: str = "missing_values.png"):
    fig, ax = plt.subplots(figsize=(8, 4))
    missing = df.isna().mean().sort_values(ascending=False)
    missing = missing[missing > 0]
    if missing.empty:
        ax.text(0.5, 0.5, "Keine fehlenden Werte", ha="center", va="center")
    else:
        sns.barplot(x=missing.values * 100, y=missing.index, ax=ax, color="#4C72B0")
        ax.set_xlabel("Anteil fehlender Werte (%)")
    ax.set_title("Fehlende Werte je Spalte")
    _save(fig, filename)
    plt.show()


def plot_numeric_distributions(df: pd.DataFrame, columns: list, filename: str = "distributions.png"):
    n = len(columns)
    ncols = 3
    nrows = int(np.ceil(n / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 4 * nrows))
    axes = np.array(axes).reshape(-1)
    for i, col in enumerate(columns):
        sns.histplot(df[col].dropna(), kde=True, ax=axes[i], color="#55A868")
        axes[i].set_title(f"Verteilung: {col}")
    for j in range(i + 1, len(axes)):
        axes[j].axis("off")
    fig.tight_layout()
    _save(fig, filename)
    plt.show()


def plot_correlation_heatmap(df: pd.DataFrame, columns: list, filename: str = "correlation_heatmap.png"):
    fig, ax = plt.subplots(figsize=(7, 6))
    corr = df[columns].corr(numeric_only=True)
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax)
    ax.set_title("Korrelationsmatrix")
    _save(fig, filename)
    plt.show()


def plot_categorical_counts(df: pd.DataFrame, column: str, filename: str = None, top_n: int = 10):
    fig, ax = plt.subplots(figsize=(7, 4))
    counts = df[column].value_counts().head(top_n)
    sns.barplot(x=counts.values, y=counts.index, ax=ax, color="#C44E52")
    ax.set_xlabel("Anzahl")
    ax.set_title(f"Häufigkeit: {column}")
    _save(fig, filename or f"counts_{column}.png")
    plt.show()


def plot_revenue_over_time(df: pd.DataFrame, date_col: str = "order_month", value_col: str = "revenue",
                            filename: str = "revenue_over_time.png"):
    fig, ax = plt.subplots(figsize=(9, 4))
    ts = df.groupby(date_col)[value_col].sum().sort_index()
    ts.plot(ax=ax, marker="o", color="#4C72B0")
    ax.set_ylabel("Umsatz (€)")
    ax.set_xlabel("Monat")
    ax.set_title("Umsatzentwicklung über die Zeit")
    plt.xticks(rotation=45)
    _save(fig, filename)
    plt.show()


def detect_outliers_iqr(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Erkennt Ausreißer mittels IQR-Methode (1.5*IQR-Regel) und gibt die betroffenen Zeilen zurück."""
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    outliers = df[(df[column] < lower) | (df[column] > upper)]
    print(f"{column}: {len(outliers)} Ausreißer außerhalb [{lower:.2f}, {upper:.2f}]")
    return outliers


def plot_boxplot(df: pd.DataFrame, column: str, by: str = None, filename: str = None):
    fig, ax = plt.subplots(figsize=(7, 4))
    if by:
        sns.boxplot(data=df, x=by, y=column, ax=ax)
        plt.xticks(rotation=30)
    else:
        sns.boxplot(data=df, y=column, ax=ax)
    ax.set_title(f"Boxplot: {column}" + (f" nach {by}" if by else ""))
    _save(fig, filename or f"boxplot_{column}.png")
    plt.show()
