# 🚨 Analýza Dopravních Nehod Brna

Komplexní analýza dopravních nehod v regionu Brna. Projekt analyzuje 74,099 záznamů nehod z let 2010-2023, přičemž mapuje příčiny, lokality, následky a trendy v bezpečnosti silničního provozu.

**Období pokrytí:** 2010-2023 | **Lokalita:** Brno a jižní Morava | **Počet nehod:** 74,099

---

## 🚀 Rychlý Start

### 1. Instalace

```powershell
# Klonujte repozitář a navigujte do složky
cd DataVis

# Vytvořte virtuální prostředí (doporučeno)
python -m venv venv
.\venv\Scripts\activate

# Nainstalujte závislosti
pip install -r requirements.txt
```

### 2. Spusťte Analýzu

```powershell
# Analýza dopravních nehod
python nehodyAnalysis.py
```

---

## 📁 Struktura Projektu

```
DataVis/
├── nehodyAnalysis.py          # Hlavní analýza nehod
├── requirements.txt           # Python závislosti
├── README.md                  # Tento soubor
│
├── data/                      # Vstupní dataset
│   ├── dopravni_nehody.csv           (74,099 nehod)
│   └── nehody_dataset_column_hints.csv
│
└── graphs/                    # Výstupní analýzy a reports
    ├── nehody_analyza_report.txt
    └── *.png
```

---

## 📈 Klíčová Zjištění

### 🚨 Dopravní Nehody (74,099 záznamů, 2010-2023)

| Metrika | Hodnota |
|---------|---------|
| **Usmrcení** | 422 lidí |
| **Těžce zraněnění** | 4,959 osob |
| **Lehce zraněnění** | 36,135 osob |
| **Hmotná škoda** | 5.08 miliard Kč |
| **Nejčastější příčina** | Nesprávný způsob jízdy (63.9%) |
| **Nejnebezpečnější lokalita** | Brno-střed (22,083 nehod, 49 usmrcených) |
| **Nejhorší dny** | Pátek (12,365), pondělí (12,091) |
| **Vliv alkoholu** | 6.06% nehod, ale 7.3% smrtí |
| **Trend** | ↓ Pokles z 6,000/rok (2010-19) na 4,500/rok (2020-23) |

#### Detailní Analýza

**Příčiny nehod:**
- Nesprávný způsob jízdy - 63.9%
- Nedání přednosti - 15.2%
- Nedodržení bezpečné vzdálenosti - 8.5%
- Technické závady - 4.8%
- Ostatní - 7.6%

**Geografické rozložení:**
- Brno-střed dominuje s 22,083 nehod (29.8% veškerých nehod)
- Ostatní okresní města mají výrazně nižší počty
- Koncentrace nehod v dopravně vytížených oblastech

**Časové vzorce:**
- Největší riziko o víkendech (pátek, sobota)
- Pracovní dny také vykazují vysoké počty
- Sezónní variace v závislosti na počasí

**Bezpečnostní faktory:**
- Alkohol jako součást 6.06% nehod s nepřiměřeně vysokým podílem na smrtelnosti
- Rychlá jízda a technické závady jsou dalšími kritickými faktory

---



## 📦 Požadavky

```
pandas>=1.3.0          # Datová analýza
matplotlib>=3.4.0      # Vizualizace grafů
numpy>=1.20.0          # Numerické operace
chardet>=4.0.0         # Detekce kódování
```

Všechny závislosti jsou v `requirements.txt`.

---

## 💡 Poznámky pro Uživatele

- **Čas běhu:** Analýza trvá 5-10 minut v závislosti na výkonu
- **Diskový prostor:** Zajistěte ~200 MB pro dataset a výstupy
- **Python verze:** 3.8+
- **OS:** Windows / Linux / macOS
- **Lokalizace:** Analýza je v češtině

---

## 📊 O Projektu

Projekt zaměřený na hlubší porozumění bezpečnostním vzorům dopravy v Brně. Výsledky pomáhají identifikovat kritická místa a příčiny nehod pro zlepšení bezpečnosti silničního provozu.
