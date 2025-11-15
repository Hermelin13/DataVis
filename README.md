# DataVis

Python projekt pro analýzu dopravních dat - nehod, zpoždění a cyklotras v oblasti Brna.

## Datasety
- **dopravni_nehody.csv** - 74,099 záznamů dopravních nehod (2010-2023)
- **cyklotrasy_4326.geojson** - 487 cyklotras (7,913 km celkem)
- **Traffic_delays.csv** - Data o dopravních zpožděních
- **Traffic_events.csv** - Data o dopravních událostech

## Analytické skripty

### `nehodyAnalysis.py`
Komplexní analýza dopravních nehod:
- 74,099 záznamů nehod z let 2010-2023
- 422 usmrcených, 4,959 těžce zraněných, 36,135 lehce zraněných
- Celková hmotná škoda: 5.08 miliard Kč
- Statistiky podle lokalit, příčin, času, počasí
- Generuje grafy a mapu nehod

```powershell
python nehodyAnalysis.py
```

### `cykloAnalysis.py`
Analýza cyklotras v regionu:
- 487 cyklotras pokrývajících 7,913 km
- 186 obcí
- Geografická analýza a vizualizace
- Generuje mapu cyklotras

```powershell
python cykloAnalysis.py
```

### `delaysAnalysis.py`
Analýza dopravních zpoždění:
- 10,000 záznamů zpoždění z let 2024-2025
- Celkové zpoždění: 348 hodin
- 47 měst, 897 unikátních ulic
- Brno tvoří 86.5% všech dat
- Průměrná rychlost: 10.6 km/h
- Statistiky podle měst, ulic, úrovní dopravy
- Generuje grafy a detailní analýzy

```powershell
python delaysAnalysis.py
```

### `eventsAnalysis.py`
Analýza dopravních událostí (user-reported):
- 10,000 záznamů z období 2023-2024
- Typy: Zácpy (69.6%), Nebezpečí (26.1%), Nehody (2.3%), Uzavírky (1.9%)
- Brno: 62.7% všech událostí
- Průměrné hodnocení uživatelů: 2.61/5
- 61,348 pozitivních reakcí (thumbs up)
- Nejčastější: D1 (1,541 záznamů), Vídeská (353x)

```powershell
python eventsAnalysis.py
```

### `fixCSV.py`
Nástroj pro opravu kódování CSV souborů:
```powershell
# Použití defaultního souboru (data/Traffic_delays.csv)
python fixCSV.py

# Vlastní soubor ze složky data/
python fixCSV.py Traffic_events.csv

# Vlastní cesta
python fixCSV.py cesta/k/souboru.csv
```

## Instalace
1. Vytvořte si virtuální prostředí (doporučeno):
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
2. Nainstalujte závislosti:
   ```powershell
   pip install -r requirements.txt
   ```

## Klíčová zjištění

### Dopravní nehody
- **Nejčastější příčina**: Nesprávný způsob jízdy (63.9%)
- **Nejnebezpečnější lokalita**: Brno-střed (22,083 nehod, 49 usmrcených)
- **Nejvíce nehod**: Pátek (12,365) a pondělí (12,091)
- **Alkohol**: 6.06% nehod, ale 7.3% úmrtí
- **Trend**: Pokles z ~6,000 nehod/rok (2010-2019) na ~4,500 nehod/rok (2020-2023)

### Cyklotrasy
- **Celková délka**: 7,913 km
- **Nejdelší trasa**: 278 km
- **Top lokalita**: Křenov (5 tras)
- **Pokrytí**: Jižní Morava (15.42°-17.75° E, 48.57°-49.72° N)

### Dopravní zpoždění
- **Celkové zpoždění**: 348.42 hodin (10,000 záznamů)
- **Průměrné zpoždění**: 2.09 minut (medián: 1.6 min)
- **Nejpomalejší město**: Brno (86.5% všech zpoždění, průměrná rychlost 9.7 km/h)
- **Nejhorší ulice**: Vídeská (212 záznamů, 75,689 s celkem, 11.8 km/h)
- **Kritická rychlost**: 76.6% provozu pod 15 km/h (stojící/velmi pomalý)
- **D1**: 217 záznamů, průměrné zpoždění 5.4 min, 40.7 km/h

### Dopravní události
- **Nejčastější typ**: Dopravní zácpy (69.6%)
- **Nejvíce hlášená ulice**: D1 (1,541 událostí), Vídeská (353x)
- **Průměrná spolehlivost**: 6.47/10 (Brno)
- **Nejspolehlivější typ**: Nebezpečí na silnici (8.91/10)
- **Pozitivní reakce**: 61,348 thumbs up, průměr 17.6 na událost
- **Top podtypy**: Hustý provoz (28.7%), Stojící provoz (15%), Zastavená auta (10%)

## Výstupy
Analýzy generují:
- `data/nehody_analyza.png` - Souhrnné grafy nehod
- `data/nehody_mapa.png` - Mapa rozložení nehod
- `data/cyklotrasy_mapa.png` - Vizualizace cyklotras
- `data/delays_analyza.png` - Souhrnné grafy zpoždění
- `data/delays_detail.png` - Detailní analýza zpoždění
- `data/events_analyza.png` - Souhrnné grafy událostí
- `data/events_detail.png` - Detailní analýza událostí
- `data/opraveno_*.csv` - Opravené CSV soubory

## Požadavky
```
requests
beautifulsoup4
pandas
geopandas
matplotlib
shapely
selenium
webdriver-manager
```
