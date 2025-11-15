import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

print("=== ANALÝZA DOPRAVNÍCH UDÁLOSTÍ ===\n")

# Načtení dat
print("Načítání datasetu...")
df = pd.read_csv("data/opraveno_Traffic_events.csv")

print(f"✓ Načteno {len(df):,} záznamů, {len(df.columns)} sloupců")
print(f"✓ Velikost v paměti: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB\n")

# Základní statistiky
print("=== ZÁKLADNÍ PŘEHLED ===")
print(f"Časové rozmezí: {df['pubMillis'].min()} až {df['pubMillis'].max()}")
print(f"Počet měst: {df['city'].nunique()}")
print(f"Počet unikátních ulic: {df['street'].nunique()}")
print(f"Počet unikátních událostí: {df['uuid'].nunique()}")

# Geografické pokrytí
print(f"\nGeografické rozmezí:")
print(f"  Latitude: {df['latitude'].min():.6f} až {df['latitude'].max():.6f}")
print(f"  Longitude: {df['longitude'].min():.6f} až {df['longitude'].max():.6f}")

# Typy událostí
print("\n=== TYPY UDÁLOSTÍ ===")
type_stats = df['type'].value_counts()
type_mapping = {
    'JAM': 'Dopravní zácpa',
    'HAZARD': 'Nebezpečí na silnici',
    'ACCIDENT': 'Nehoda',
    'ROAD_CLOSED': 'Uzavřená silnice'
}
for event_type, count in type_stats.items():
    pct = (count / len(df)) * 100
    label = type_mapping.get(event_type, event_type)
    print(f"  {label:25} ({event_type:15}): {count:>6,} ({pct:>5.2f}%)")

# Podtypy událostí
print("\n=== TOP 20 PODTYPŮ UDÁLOSTÍ ===")
subtype_stats = df['subtype'].value_counts().head(20)
subtype_mapping = {
    'JAM_HEAVY_TRAFFIC': 'Hustý provoz',
    'JAM_STAND_STILL_TRAFFIC': 'Stojící provoz',
    'HAZARD_ON_SHOULDER_CAR_STOPPED': 'Zastavené auto na krajnici',
    'HAZARD_ON_ROAD_CONSTRUCTION': 'Stavba na silnici',
    'HAZARD_ON_ROAD_POT_HOLE': 'Výmol na silnici',
    'HAZARD_ON_ROAD': 'Nebezpečí na silnici',
    'ROAD_CLOSED_EVENT': 'Uzavřená silnice (událost)',
    'HAZARD_ON_ROAD_OBJECT': 'Překážka na silnici',
    'JAM_MODERATE_TRAFFIC': 'Mírný provoz',
    'HAZARD_ON_ROAD_TRAFFIC_LIGHT_FAULT': 'Porucha semaforu',
    'ACCIDENT_MAJOR': 'Vážná nehoda',
    'HAZARD_WEATHER': 'Počasí',
    'HAZARD_ON_ROAD_CAR_STOPPED': 'Zastavené auto na silnici',
    'ACCIDENT_MINOR': 'Menší nehoda',
    'HAZARD_WEATHER_FLOOD': 'Povodeň'
}
for subtype, count in subtype_stats.items():
    pct = (count / len(df)) * 100
    label = subtype_mapping.get(subtype, subtype)
    print(f"  {label:35} {count:>6,} ({pct:>5.2f}%)")

# Analýza spolehlivosti
print("\n=== SPOLEHLIVOST HLÁŠENÍ (reliability) ===")
print("Škála: 5 (nejnižší) až 10 (nejvyšší)")
reliability_stats = df['reliability'].value_counts().sort_index()
for reliability, count in reliability_stats.items():
    pct = (count / len(df)) * 100
    bar = '█' * int(pct / 2)
    print(f"  Úroveň {reliability:2}: {count:>6,} ({pct:>5.2f}%) {bar}")

# Průměrná spolehlivost podle typu
print("\nPrůměrná spolehlivost podle typu události:")
avg_reliability = df.groupby('type')['reliability'].mean().sort_values(ascending=False)
for event_type, avg in avg_reliability.items():
    label = type_mapping.get(event_type, event_type)
    print(f"  {label:25} {avg:.2f}")

# Důvěryhodnost
print("\n=== DŮVĚRYHODNOST (confidence) ===")
print("Škála: 0 (nejnižší) až 5 (nejvyšší)")
confidence_stats = df['confidence'].value_counts().sort_index()
for confidence, count in confidence_stats.items():
    pct = (count / len(df)) * 100
    bar = '█' * int(pct / 2)
    print(f"  Úroveň {confidence}: {count:>6,} ({pct:>5.2f}%) {bar}")

# Hodnocení uživatelů
print("\n=== HODNOCENÍ UŽIVATELŮ (reportRating) ===")
print("Škála: 0 (nejnižší) až 5 (nejvyšší)")
rating_stats = df['reportRating'].value_counts().sort_index()
for rating, count in rating_stats.items():
    pct = (count / len(df)) * 100
    bar = '★' * rating + '☆' * (5 - rating)
    print(f"  {bar} ({rating}): {count:>6,} ({pct:>5.2f}%)")

avg_rating = df['reportRating'].mean()
print(f"\nPrůměrné hodnocení: {avg_rating:.2f} / 5")

# Thumbs up
print("\n=== POZITIVNÍ REAKCE (thumbs up) ===")
thumbs_up = df['nThumbsUp'].dropna()
if len(thumbs_up) > 0:
    print(f"Události s reakcemi: {len(thumbs_up):,} ({len(thumbs_up)/len(df)*100:.1f}%)")
    print(f"Celkem thumbs up: {int(thumbs_up.sum()):,}")
    print(f"Průměr na událost: {thumbs_up.mean():.2f}")
    print(f"Maximum: {int(thumbs_up.max())}")

# Top města
print("\n=== TOP 20 MĚST PODLE POČTU UDÁLOSTÍ ===")
city_stats = df.groupby('city').agg({
    'type': 'count',
    'reliability': 'mean',
    'reportRating': 'mean'
}).round(2)
city_stats.columns = ['počet', 'spolehlivost', 'hodnocení']
city_stats = city_stats.sort_values('počet', ascending=False).head(20)
print(f"{'Město':<25} | {'Počet':>7} | {'Spolehlivost':>13} | {'Hodnocení':>10}")
print("-" * 70)
for city, row in city_stats.iterrows():
    print(f"{city:<25} | {int(row['počet']):>7,} | {row['spolehlivost']:>13.2f} | {row['hodnocení']:>10.2f}")

# Analýza podle typu události
print("\n=== DETAILNÍ STATISTIKY PODLE TYPU ===")
type_detail = df.groupby('type').agg({
    'uuid': 'count',
    'reliability': 'mean',
    'confidence': 'mean',
    'reportRating': 'mean',
    'nThumbsUp': lambda x: x.dropna().sum()
}).round(2)
type_detail.columns = ['počet', 'spolehlivost', 'důvěryhodnost', 'hodnocení', 'thumbs_up']
type_detail = type_detail.sort_values('počet', ascending=False)
print(f"{'Typ':<15} | {'Počet':>7} | {'Spoleh.':>8} | {'Důvěra':>7} | {'Hod.':>5} | {'👍':>6}")
print("-" * 70)
for event_type, row in type_detail.iterrows():
    label = type_mapping.get(event_type, event_type)[:14]
    print(f"{label:<15} | {int(row['počet']):>7,} | {row['spolehlivost']:>8.2f} | {row['důvěryhodnost']:>7.2f} | {row['hodnocení']:>5.2f} | {int(row['thumbs_up']):>6,}")

# Top ulice
print("\n=== TOP 30 ULIC PODLE POČTU UDÁLOSTÍ ===")
street_stats = df.groupby('street').agg({
    'type': 'count',
    'reliability': 'mean',
    'reportRating': 'mean'
}).round(2)
street_stats.columns = ['počet', 'spolehlivost', 'hodnocení']
street_stats = street_stats.sort_values('počet', ascending=False).head(30)
for idx, (street, row) in enumerate(street_stats.iterrows(), 1):
    print(f"  {idx:2}. {street:<35} {int(row['počet']):>4}x, spoleh: {row['spolehlivost']:.1f}, hod: {row['hodnocení']:.1f}")

# Analýza Brna
print("\n=== DETAILNÍ ANALÝZA BRNA ===")
brno = df[df['city'] == 'Brno'].copy()
print(f"Počet událostí: {len(brno):,} ({len(brno)/len(df)*100:.1f}% všech dat)")
print(f"Průměrná spolehlivost: {brno['reliability'].mean():.2f}")
print(f"Průměrné hodnocení: {brno['reportRating'].mean():.2f}")

print("\nTypy událostí v Brně:")
brno_types = brno['type'].value_counts()
for event_type, count in brno_types.items():
    pct = (count / len(brno)) * 100
    label = type_mapping.get(event_type, event_type)
    print(f"  {label:25} {count:>6,} ({pct:>5.2f}%)")

print("\nTop 15 ulic v Brně:")
brno_streets = brno.groupby('street').agg({
    'type': 'count',
    'reliability': 'mean'
}).round(2)
brno_streets.columns = ['počet', 'spolehlivost']
brno_streets = brno_streets.sort_values('počet', ascending=False).head(15)
for idx, (street, row) in enumerate(brno_streets.iterrows(), 1):
    print(f"  {idx:2}. {street:<35} {int(row['počet']):>4}x, spoleh: {row['spolehlivost']:.1f}")

# Typy silnic
print("\n=== TYPY SILNIC (roadType) ===")
roadtype_stats = df.groupby('roadType').agg({
    'type': 'count',
    'reliability': 'mean'
}).round(2)
roadtype_stats.columns = ['počet', 'spolehlivost']
roadtype_stats = roadtype_stats.sort_values('počet', ascending=False).head(10)
for roadtype, row in roadtype_stats.iterrows():
    pct = (row['počet'] / len(df)) * 100
    print(f"  Typ {roadtype:2}: {int(row['počet']):>6,} ({pct:>5.2f}%), spolehlivost: {row['spolehlivost']:.2f}")

# Vizualizace
print("\n=== GENEROVÁNÍ VIZUALIZACÍ ===")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Graf 1: Typy událostí
type_counts = df['type'].value_counts()
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
axes[0, 0].pie(type_counts.values, labels=[type_mapping.get(t, t) for t in type_counts.index], 
               autopct='%1.1f%%', startangle=90, colors=colors)
axes[0, 0].set_title('Rozdělení typů událostí', fontsize=14, fontweight='bold')

# Graf 2: Top 15 podtypů
top_subtypes = df['subtype'].value_counts().head(15)
axes[0, 1].barh(range(len(top_subtypes)), top_subtypes.values, color='coral')
axes[0, 1].set_yticks(range(len(top_subtypes)))
axes[0, 1].set_yticklabels([subtype_mapping.get(s, s)[:25] for s in top_subtypes.index], fontsize=9)
axes[0, 1].set_title('Top 15 podtypů událostí', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('Počet událostí')
axes[0, 1].invert_yaxis()
axes[0, 1].grid(axis='x', alpha=0.3)

# Graf 3: Spolehlivost
reliability_data = df['reliability'].value_counts().sort_index()
axes[1, 0].bar(reliability_data.index, reliability_data.values, color='steelblue', alpha=0.7)
axes[1, 0].set_title('Rozdělení spolehlivosti hlášení', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Úroveň spolehlivosti (5-10)')
axes[1, 0].set_ylabel('Počet událostí')
axes[1, 0].grid(axis='y', alpha=0.3)

# Graf 4: Hodnocení uživatelů
rating_data = df['reportRating'].value_counts().sort_index()
axes[1, 1].bar(rating_data.index, rating_data.values, color='green', alpha=0.7)
axes[1, 1].set_title('Hodnocení uživatelů', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('Hodnocení (0-5)')
axes[1, 1].set_ylabel('Počet událostí')
axes[1, 1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig("data/events_analyza.png", dpi=150)
print("✓ Grafy uloženy do: data/events_analyza.png")

# Dodatečné grafy
fig2, axes2 = plt.subplots(1, 2, figsize=(16, 6))

# Graf 5: Top 15 měst
top_cities = city_stats.head(15).sort_values('počet')
axes2[0].barh(range(len(top_cities)), top_cities['počet'], color='teal')
axes2[0].set_yticks(range(len(top_cities)))
axes2[0].set_yticklabels(top_cities.index, fontsize=9)
axes2[0].set_title('Top 15 měst podle počtu událostí', fontsize=14, fontweight='bold')
axes2[0].set_xlabel('Počet událostí')
axes2[0].grid(axis='x', alpha=0.3)

# Graf 6: Mapa událostí
sample = df.sample(min(5000, len(df)))
scatter = axes2[1].scatter(sample['longitude'], sample['latitude'], 
                          c=sample['type'].map({'JAM': 0, 'HAZARD': 1, 'ACCIDENT': 2, 'ROAD_CLOSED': 3}),
                          cmap='viridis', alpha=0.5, s=20)
axes2[1].set_title('Geografické rozložení událostí', fontsize=14, fontweight='bold')
axes2[1].set_xlabel('Longitude')
axes2[1].set_ylabel('Latitude')
axes2[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("data/events_detail.png", dpi=150)
print("✓ Detailní grafy uloženy do: data/events_detail.png")

print("\n=== ANALÝZA DOKONČENA ===")
