# Projektplan: Explorative Datenanalyse — Online-Retail-Verkaufsdaten

## 1. Ausgangslage und Motivation

Ein (fiktiver) Online-Händler möchte seine Verkaufsdaten aus den Jahren 2023–2024 besser
verstehen, bevor daraus Reporting-Dashboards oder Vorhersagemodelle (z. B. Umsatzprognose,
Retourenrisiko) abgeleitet werden. Bevor solche Modelle entwickelt werden können, muss die
Datenbasis verstanden, geprüft und bereinigt werden — das ist der Zweck dieser explorativen
Datenanalyse (EDA).

## 2. Zielsetzung

- Datenqualität systematisch bewerten (Vollständigkeit, Konsistenz, Ausreißer, Duplikate)
- Zentrale Geschäftskennzahlen und deren Verteilungen verstehen
- Muster und Zusammenhänge zwischen Variablen aufdecken
- Eine bereinigte, dokumentierte Datenbasis für nachgelagerte Analysen/Modelle bereitstellen
- Ergebnisse reproduzierbar und nachvollziehbar dokumentieren (Code + Notebook + Report)

## 3. Leitfragen

| # | Fragestellung | Analysemethode |
|---|----------------|-----------------|
| 1 | Wie vollständig und konsistent sind die Daten? | Missing-Value-Analyse, Duplikatsprüfung |
| 2 | Wie ist die Umsatzentwicklung über die Zeit? | Zeitreihenanalyse (Liniendiagramm) |
| 3 | Welche Produktkategorien/Regionen sind umsatzstark? | Gruppierung + Balkendiagramme |
| 4 | Gibt es Zusammenhänge zwischen Variablen (z. B. Preis, Menge, Rabatt)? | Korrelationsanalyse, Heatmap |
| 5 | Wie hängen Rabatte mit der Retourenquote zusammen? | Gruppierte Kennzahlen, Balkendiagramm |
| 6 | Welche Ausreißer gibt es (Preis, Lieferzeit)? | IQR-Methode, Boxplots |

## 4. Datenquelle

Da es sich um ein Demonstrationsprojekt handelt, wird ein **synthetischer, aber realistisch
modellierter Datensatz** verwendet (`src/generate_data.py`), der absichtlich typische
Datenqualitätsprobleme enthält (fehlende Werte, Duplikate, inkonsistente Kategorien,
Ausreißer). Das erlaubt es, den kompletten EDA-Workflow inklusive Datenbereinigung realistisch
zu demonstrieren, ohne auf sensible echte Kundendaten angewiesen zu sein.

> Hinweis: Das Vorgehen (Code, Struktur, Methodik) lässt sich 1:1 auf einen echten Datensatz
> übertragen — dazu einfach `data/raw/online_retail_sales.csv` durch die eigene Datei ersetzen
> und ggf. die Spaltennamen in `src/data_loader.py` anpassen.

## 5. Methodisches Vorgehen (CRISP-DM-orientiert)

1. **Datenverständnis**
   - Struktur, Datentypen, Umfang prüfen (`df.info()`, `df.describe()`)
   - Fehlende Werte, Duplikate, unplausible Werte identifizieren
2. **Datenaufbereitung**
   - Duplikate entfernen
   - Kategorienamen normalisieren
   - Unplausible Werte (z. B. negative Mengen) entfernen
   - Fehlende Werte behandeln (Median-Imputation bzw. eigene Kategorie)
   - Abgeleitete Kennzahlen berechnen (z. B. Umsatz je Bestellung)
3. **Explorative Analyse**
   - Univariate Analyse (Verteilungen numerischer & kategorialer Variablen)
   - Bivariate/multivariate Analyse (Korrelationen, Gruppenvergleiche)
   - Zeitreihenanalyse
   - Ausreißererkennung (IQR-Methode)
4. **Dokumentation der Erkenntnisse**
   - Zusammenfassung zentraler Befunde im Notebook
   - Empfehlungen für nächste Schritte (z. B. Modellierung)

## 6. Projektstruktur

```
eda-projekt/
├── README.md                  # Projektübersicht & Anleitung
├── requirements.txt           # Python-Abhängigkeiten
├── docs/
│   └── PROJEKTPLAN.md         # Dieser Plan
├── data/
│   ├── raw/                   # Rohdaten (unverändert)
│   └── processed/             # Bereinigte Daten
├── src/
│   ├── generate_data.py       # Erzeugt den synthetischen Rohdatensatz
│   ├── data_loader.py         # Laden & Bereinigen der Daten
│   └── eda_utils.py           # Wiederverwendbare Plot-/Analysefunktionen
├── notebooks/
│   └── 01_eda.ipynb           # Vollständige EDA (ausgeführt, mit Outputs)
└── reports/
    └── figures/                # Exportierte Diagramme (PNG)
```

## 7. Werkzeuge

- **Sprache:** Python 3.11
- **Bibliotheken:** pandas, numpy, matplotlib, seaborn, jupyter
- **Versionsverwaltung:** Git / GitHub

## 8. Zeitplanung (beispielhaft für Portfolio-Kontext)

| Phase | Aufwand | Inhalt |
|-------|---------|--------|
| Datenverständnis & -aufbereitung | 0,5 Tag | Struktur, Datenqualität, Bereinigung |
| Univariate Analyse | 0,5 Tag | Verteilungen, Häufigkeiten |
| Bivariate/multivariate Analyse | 1 Tag | Korrelationen, Gruppenvergleiche, Zeitreihen |
| Ausreißeranalyse & Dokumentation | 0,5 Tag | IQR-Analyse, Zusammenfassung, README |

## 9. Erfolgskriterien

- Alle Leitfragen (Abschnitt 3) sind im Notebook nachvollziehbar beantwortet
- Der Code ist modular, dokumentiert und reproduzierbar (`pip install -r requirements.txt`
  gefolgt von `python src/generate_data.py` und dem Ausführen des Notebooks funktioniert ohne
  manuelle Eingriffe)
- Ergebnisse sind als Diagramme in `reports/figures/` exportiert
- Zusammenfassung der Erkenntnisse liegt in Textform vor (Notebook-Abschnitt 9 + README)

## 10. Mögliche Erweiterungen (Ausblick)

- Aufbau eines interaktiven Dashboards (z. B. mit Streamlit oder Plotly Dash)
- Prognosemodell für monatlichen Umsatz (z. B. mit Prophet oder einem einfachen Regressionsmodell)
- Klassifikationsmodell zur Vorhersage von Retouren
- Kohorten-/RFM-Analyse der Kunden (Recency, Frequency, Monetary)
