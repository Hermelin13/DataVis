import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

print("=== ANALÝZA DOPRAVNÍCH ZPOŽDĚNÍ ===\n")

# Načtení dat
print("Načítání datasetu...")
df = pd.read_csv("data/opraveno_Traffic_delays.csv")

print(f"✓ Načteno {len(df):,} záznamů, {len(df.columns)} sloupců")
print(f"✓ Velikost v paměti: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB\n")

# Základní statistiky
print("=== ZÁKLADNÍ PŘEHLED ===")
print(f"Časové rozmezí: {df['pubMillis'].min()} až {df['pubMillis'].max()}")
print(f"Počet měst: {df['city'].nunique()}")
print(f"Počet unikátních ulic: {df['street'].nunique()}")
print(f"Počet úrovní dopravy (level): {df['level'].nunique()}")

# Statistiky zpoždění
print("\n=== STATISTIKY ZPOŽDĚNÍ ===")
total_delay_hours = df['delay'].sum() / 3600
print(f"Celkové zpoždění: {df['delay'].sum():,} sekund ({total_delay_hours:.2f} hodin)")
print(f"Průměrné zpoždění: {df['delay'].mean():.2f} sekund ({df['delay'].mean()/60:.2f} minut)")
print(f"Medián zpoždění: {df['delay'].median():.2f} sekund")
print(f"Maximální zpoždění: {df['delay'].max():,} sekund ({df['delay'].max()/60:.2f} minut)")
print(f"Minimální zpoždění: {df['delay'].min():,} sekund")

# Kvantily
print("\nRozdělení zpoždění (kvantily):")
for q in [0.25, 0.5, 0.75, 0.9, 0.95, 0.99]:
    val = df['delay'].quantile(q)
    print(f"  {int(q*100)}% záznamů má zpoždění ≤ {val:.0f} s ({val/60:.1f} min)")

# Statistiky rychlosti
print("\n=== STATISTIKY RYCHLOSTI ===")
print(f"Průměrná rychlost: {df['speedKMH'].mean():.2f} km/h")
print(f"Medián rychlosti: {df['speedKMH'].median():.2f} km/h")
print(f"Minimální rychlost: {df['speedKMH'].min()} km/h")
print(f"Maximální rychlost: {df['speedKMH'].max()} km/h")

# Kategorie rychlosti
print("\nRozdělení podle rychlosti:")
speed_ranges = [
    (0, 5, "stojící/téměř stojící"),
    (5, 15, "velmi pomalá"),
    (15, 30, "pomalá"),
    (30, 50, "střední"),
    (50, 100, "rychlá")
]
for min_s, max_s, label in speed_ranges:
    count = len(df[(df['speedKMH'] >= min_s) & (df['speedKMH'] < max_s)])
    pct = (count / len(df)) * 100
    print(f"  {min_s:3}-{max_s:3} km/h ({label:20}): {count:>6,} ({pct:>5.1f}%)")

# Statistiky délky
print("\n=== STATISTIKY DÉLKY ÚSEKU ===")
print(f"Průměrná délka: {df['length'].mean():.2f} m")
print(f"Medián délky: {df['length'].median():.2f} m")
print(f"Celková délka ovlivněných úseků: {df['length'].sum()/1000:.2f} km")

# Úrovně dopravy
print("\n=== ÚROVNĚ DOPRAVY (traffic level) ===")
level_stats = df.groupby('level').agg({
    'delay': ['count', 'mean', 'sum'],
    'speedKMH': 'mean'
}).round(2)
level_stats.columns = ['počet', 'prům_zpoždění', 'celk_zpoždění', 'prům_rychlost']
level_stats = level_stats.sort_index()
print("Level | Počet    | Prům. zpoždění | Celk. zpoždění | Prům. rychlost")
print("------|----------|----------------|----------------|---------------")
for level, row in level_stats.iterrows():
    print(f"  {level}   | {int(row['počet']):>8,} | {row['prům_zpoždění']:>11.1f} s | {int(row['celk_zpoždění']):>11,} s | {row['prům_rychlost']:>10.1f} km/h")

# Typy silnic
print("\n=== TYPY SILNIC (roadType) ===")
roadtype_stats = df.groupby('roadType').agg({
    'delay': ['count', 'mean'],
    'speedKMH': 'mean'
}).round(2)
roadtype_stats.columns = ['počet', 'prům_zpoždění', 'prům_rychlost']
roadtype_stats = roadtype_stats.sort_values('počet', ascending=False)
for roadtype, row in roadtype_stats.iterrows():
    print(f"  Typ {roadtype}: {int(row['počet']):>6,} záznamů, {row['prům_zpoždění']:>6.1f} s, {row['prům_rychlost']:>5.1f} km/h")

# Top města
print("\n=== TOP 20 MĚST PODLE CELKOVÉHO ZPOŽDĚNÍ ===")
city_delays = df.groupby('city').agg({
    'delay': ['count', 'sum', 'mean'],
    'speedKMH': 'mean'
}).round(2)
city_delays.columns = ['počet', 'celk_zpoždění', 'prům_zpoždění', 'prům_rychlost']
city_delays = city_delays.sort_values('celk_zpoždění', ascending=False).head(20)
print(f"{'Město':<20} | {'Počet':>7} | {'Celk. zpoždění':>15} | {'Prům. zpoždění':>15} | {'Prům. rychlost':>15}")
print("-" * 85)
for city, row in city_delays.iterrows():
    print(f"{city:<20} | {int(row['počet']):>7,} | {int(row['celk_zpoždění']):>10,} s | {row['prům_zpoždění']:>10.1f} s | {row['prům_rychlost']:>10.1f} km/h")

# Top ulice
print("\n=== TOP 30 ULIC S NEJVĚTŠÍM ZPOŽDĚNÍM ===")
street_delays = df.groupby('street').agg({
    'delay': ['count', 'sum', 'mean'],
    'speedKMH': 'mean',
    'length': 'mean'
}).round(2)
street_delays.columns = ['počet', 'celk_zpoždění', 'prům_zpoždění', 'prům_rychlost', 'prům_délka']
street_delays = street_delays.sort_values('celk_zpoždění', ascending=False).head(30)
print(f"{'Ulice':<30} | {'Počet':>6} | {'Celk. zpožd.':>13} | {'Prům. zpožd.':>12} | {'Rychlost':>9}")
print("-" * 85)
for street, row in street_delays.iterrows():
    print(f"{street:<30} | {int(row['počet']):>6} | {int(row['celk_zpoždění']):>8,} s | {row['prům_zpoždění']:>7.1f} s | {row['prům_rychlost']:>5.1f} km/h")

# Nejpomalejší ulice
print("\n=== TOP 20 NEJPOMALEJŠÍCH ULIC (průměrná rychlost) ===")
slow_streets = df.groupby('street').agg({
    'speedKMH': ['mean', 'count'],
    'delay': 'mean'
}).round(2)
slow_streets.columns = ['prům_rychlost', 'počet', 'prům_zpoždění']
slow_streets = slow_streets[slow_streets['počet'] >= 5]  # Alespoň 5 záznamů
slow_streets = slow_streets.sort_values('prům_rychlost').head(20)
for street, row in slow_streets.iterrows():
    print(f"  {street:<35} {row['prům_rychlost']:>5.1f} km/h ({int(row['počet']):>3}x, {row['prům_zpoždění']:>6.1f} s průměr)")

# Analýza Brna
print("\n=== DETAILNÍ ANALÝZA BRNA ===")
brno = df[df['city'] == 'Brno'].copy()
print(f"Počet záznamů: {len(brno):,} ({len(brno)/len(df)*100:.1f}% všech dat)")
print(f"Celkové zpoždění: {brno['delay'].sum()/3600:.2f} hodin")
print(f"Průměrná rychlost: {brno['speedKMH'].mean():.2f} km/h")

print("\nTop 15 ulic v Brně podle zpoždění:")
brno_streets = brno.groupby('street').agg({
    'delay': ['count', 'sum', 'mean'],
    'speedKMH': 'mean'
}).round(2)
brno_streets.columns = ['počet', 'celk_zpoždění', 'prům_zpoždění', 'prům_rychlost']
brno_streets = brno_streets.sort_values('celk_zpoždění', ascending=False).head(15)
for idx, (street, row) in enumerate(brno_streets.iterrows(), 1):
    print(f"  {idx:2}. {street:<30} {int(row['počet']):>4}x, {int(row['celk_zpoždění']):>7} s, {row['prům_zpoždění']:>6.1f} s, {row['prům_rychlost']:>5.1f} km/h")

# Vizualizace
print("\n=== GENEROVÁNÍ VIZUALIZACÍ ===")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Graf 1: Rozdělení zpoždění (histogram)
axes[0, 0].hist(df['delay'], bins=50, color='steelblue', edgecolor='black', alpha=0.7)
axes[0, 0].set_title('Rozdělení zpoždění', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('Zpoždění (sekundy)')
axes[0, 0].set_ylabel('Počet záznamů')
axes[0, 0].grid(axis='y', alpha=0.3)

# Graf 2: Top 15 měst
top_cities = city_delays.head(15).sort_values('celk_zpoždění')
axes[0, 1].barh(range(len(top_cities)), top_cities['celk_zpoždění']/3600, color='coral')
axes[0, 1].set_yticks(range(len(top_cities)))
axes[0, 1].set_yticklabels(top_cities.index, fontsize=9)
axes[0, 1].set_title('Top 15 měst podle celkového zpoždění', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('Celkové zpoždění (hodiny)')
axes[0, 1].grid(axis='x', alpha=0.3)

# Graf 3: Rychlost vs zpoždění
sample = df.sample(min(2000, len(df)))
axes[1, 0].scatter(sample['speedKMH'], sample['delay'], alpha=0.4, s=20, color='green')
axes[1, 0].set_title('Závislost zpoždění na rychlosti', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Rychlost (km/h)')
axes[1, 0].set_ylabel('Zpoždění (sekundy)')
axes[1, 0].grid(True, alpha=0.3)

# Graf 4: Úrovně dopravy
level_data = df['level'].value_counts().sort_index()
axes[1, 1].bar(level_data.index, level_data.values, color='purple', alpha=0.7)
axes[1, 1].set_title('Rozdělení podle úrovně dopravy', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('Úroveň dopravy (level)')
axes[1, 1].set_ylabel('Počet záznamů')
axes[1, 1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig("data/delays_analyza.png", dpi=150)
print("✓ Grafy uloženy do: data/delays_analyza.png")

# Dodatečné grafy
fig2, axes2 = plt.subplots(1, 2, figsize=(16, 6))

# Graf 5: Top 20 ulic v Brně
if len(brno_streets) > 0:
    top_brno = brno_streets.head(20).sort_values('celk_zpoždění')
    axes2[0].barh(range(len(top_brno)), top_brno['celk_zpoždění']/60, color='teal')
    axes2[0].set_yticks(range(len(top_brno)))
    axes2[0].set_yticklabels(top_brno.index, fontsize=8)
    axes2[0].set_title('Top 20 ulic v Brně podle zpoždění', fontsize=14, fontweight='bold')
    axes2[0].set_xlabel('Celkové zpoždění (minuty)')
    axes2[0].grid(axis='x', alpha=0.3)

# Graf 6: Rozdělení rychlosti
axes2[1].hist(df['speedKMH'], bins=40, color='orange', edgecolor='black', alpha=0.7)
axes2[1].set_title('Rozdělení rychlosti', fontsize=14, fontweight='bold')
axes2[1].set_xlabel('Rychlost (km/h)')
axes2[1].set_ylabel('Počet záznamů')
axes2[1].axvline(df['speedKMH'].mean(), color='red', linestyle='--', linewidth=2, label=f'Průměr: {df["speedKMH"].mean():.1f} km/h')
axes2[1].axvline(df['speedKMH'].median(), color='green', linestyle='--', linewidth=2, label=f'Medián: {df["speedKMH"].median():.1f} km/h')
axes2[1].legend()
axes2[1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig("data/delays_detail.png", dpi=150)
print("✓ Detailní grafy uloženy do: data/delays_detail.png")

print("\n=== ANALÝZA DOKONČENA ===")
