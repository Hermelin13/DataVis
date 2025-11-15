import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

print("=== ANALÝZA DOPRAVNÍCH NEHOD ===\n")

# Načtení dat
print("Načítání datasetu...")
df = pd.read_csv("data/dopravni_nehody.csv", low_memory=False)

print(f"✓ Načteno {len(df):,} záznamů, {len(df.columns)} sloupců")
print(f"✓ Velikost v paměti: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB\n")

# Základní statistiky
print("=== ZÁKLADNÍ PŘEHLED ===")
print(f"Časové rozmezí: {df['datum'].min()} až {df['datum'].max()}")
print(f"Počet unikátních lokalit: {df['zuj'].nunique()}")
print(f"Počet unikátních nehod: {df['id_nehody'].nunique()}")
print(f"Počet zaznamenaných osob: {len(df)}")

# Statistiky následků
print("\n=== STATISTIKY NÁSLEDKŮ ===")
print(f"Celkem usmrcených osob: {df['usmrceno_os'].sum()}")
print(f"Celkem těžce zraněných: {df['tezce_zran_os'].sum()}")
print(f"Celkem lehce zraněných: {df['lehce_zran_os'].sum()}")
print(f"Celková hmotná škoda: {df['hmotna_skoda'].sum():,.0f} Kč")
print(f"Průměrná škoda na nehodu: {df['hmotna_skoda'].mean():,.0f} Kč")

# Časové trendy
print("\n=== ROZDĚLENÍ PODLE ROKŮ ===")
rok_stats = df['rok'].value_counts().sort_index()
for rok, pocet in rok_stats.items():
    usmrceni = df[df['rok'] == rok]['usmrceno_os'].sum()
    print(f"  {rok}: {pocet:>6,} nehod, {usmrceni:>4} usmrcených")

# Měsíční statistiky
print("\n=== ROZDĚLENÍ PODLE MĚSÍCŮ ===")
if 'mesic' in df.columns:
    mesic_stats = df['mesic'].value_counts().sort_index()
    mesice = ['leden', 'únor', 'březen', 'duben', 'květen', 'červen',
              'červenec', 'srpen', 'září', 'říjen', 'listopad', 'prosinec']
    for mesic_num, pocet in mesic_stats.items():
        mesic_nazev = mesice[int(mesic_num)-1] if 1 <= mesic_num <= 12 else f"měsíc {mesic_num}"
        print(f"  {mesic_nazev}: {pocet:,} nehod")

# Denní čas
print("\n=== ROZDĚLENÍ PODLE DOBY DNE ===")
if 'doba' in df.columns:
    doba_stats = df['doba'].value_counts()
    for doba, pocet in doba_stats.items():
        print(f"  {doba}: {pocet:,} nehod")

# Den v týdnu
print("\n=== ROZDĚLENÍ PODLE DNE V TÝDNU ===")
if 'den_v_tydnu' in df.columns:
    dny = ['pondělí', 'úterý', 'středa', 'čtvrtek', 'pátek', 'sobota', 'neděle']
    den_stats = df['den_v_tydnu'].value_counts().sort_index()
    for den_num, pocet in den_stats.items():
        try:
            den_int = int(den_num)
            den_nazev = dny[den_int-1] if 1 <= den_int <= 7 else f"den {den_num}"
        except (ValueError, TypeError, IndexError):
            den_nazev = str(den_num)
        print(f"  {den_nazev}: {pocet:,} nehod")

# Top lokality
print("\n=== TOP 15 LOKALIT PODLE POČTU NEHOD ===")
top_lokality = df['zuj'].value_counts().head(15)
for idx, (lokace, pocet) in enumerate(top_lokality.items(), 1):
    usmrceni = df[df['zuj'] == lokace]['usmrceno_os'].sum()
    print(f"  {idx:2}. {lokace:25} {pocet:>6,} nehod, {usmrceni:>4} usmrcených")

# Hlavní příčiny
print("\n=== HLAVNÍ PŘÍČINY NEHOD ===")
if 'hlavni_pricina' in df.columns:
    priciny = df['hlavni_pricina'].value_counts().head(10)
    for pricina, pocet in priciny.items():
        procento = (pocet / len(df)) * 100
        print(f"  {pricina:35} {pocet:>6,} ({procento:>5.2f}%)")

# Alkohol
print("\n=== VLIV ALKOHOLU ===")
if 'alkohol_vinik' in df.columns:
    alkohol_stats = df['alkohol_vinik'].value_counts()
    celkem_s_alkoholem = alkohol_stats.get('ano', 0)
    procento_alkohol = (celkem_s_alkoholem / len(df)) * 100
    print(f"  Nehody s alkoholem: {celkem_s_alkoholem:,} ({procento_alkohol:.2f}%)")
    
    # Úmrtnost při alkoholu
    usmrceni_alkohol = df[df['alkohol_vinik'] == 'ano']['usmrceno_os'].sum()
    usmrceni_celkem = df['usmrceno_os'].sum()
    if usmrceni_celkem > 0:
        procento_smrti = (usmrceni_alkohol / usmrceni_celkem) * 100
        print(f"  Usmrcení při alkoholu: {usmrceni_alkohol} ({procento_smrti:.1f}% všech úmrtí)")

# Stav vozovky
print("\n=== STAV VOZOVKY ===")
if 'stav_vozovky' in df.columns:
    stav_stats = df['stav_vozovky'].value_counts().head(10)
    for stav, pocet in stav_stats.items():
        procento = (pocet / len(df)) * 100
        print(f"  {stav:25} {pocet:>6,} ({procento:>5.2f}%)")

# Počasí
print("\n=== POVĚTRNOSTNÍ PODMÍNKY ===")
if 'povetrnostni_podm' in df.columns:
    pocasi_stats = df['povetrnostni_podm'].value_counts().head(10)
    for pocasi, pocet in pocasi_stats.items():
        procento = (pocet / len(df)) * 100
        print(f"  {pocasi:25} {pocet:>6,} ({procento:>5.2f}%)")

# Geografická analýza
print("\n=== GEOGRAFICKÁ DATA ===")
if 'x' in df.columns and 'y' in df.columns:
    # Filtrovat validní souřadnice
    valid_coords = df[(df['x'].notna()) & (df['y'].notna())]
    print(f"Záznamy s platnou GPS: {len(valid_coords):,} ({len(valid_coords)/len(df)*100:.1f}%)")
    if len(valid_coords) > 0:
        print(f"Rozsah X: {valid_coords['x'].min():,.0f} až {valid_coords['x'].max():,.0f}")
        print(f"Rozsah Y: {valid_coords['y'].min():,.0f} až {valid_coords['y'].max():,.0f}")

# Vizualizace 1: Trend v čase
print("\n=== GENEROVÁNÍ VIZUALIZACÍ ===")
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Graf 1: Nehody podle roků
rok_data = df['rok'].value_counts().sort_index()
axes[0, 0].bar(rok_data.index, rok_data.values, color='steelblue')
axes[0, 0].set_title('Počet nehod podle roků', fontsize=14)
axes[0, 0].set_xlabel('Rok')
axes[0, 0].set_ylabel('Počet nehod')
axes[0, 0].grid(axis='y', alpha=0.3)

# Graf 2: Top 10 lokalit
top_10 = df['zuj'].value_counts().head(10)
axes[0, 1].barh(range(len(top_10)), top_10.values, color='coral')
axes[0, 1].set_yticks(range(len(top_10)))
axes[0, 1].set_yticklabels(top_10.index, fontsize=9)
axes[0, 1].set_title('Top 10 lokalit podle počtu nehod', fontsize=14)
axes[0, 1].set_xlabel('Počet nehod')
axes[0, 1].invert_yaxis()

# Graf 3: Hlavní příčiny
if 'hlavni_pricina' in df.columns:
    priciny_top = df['hlavni_pricina'].value_counts().head(8)
    axes[1, 0].pie(priciny_top.values, labels=priciny_top.index, autopct='%1.1f%%', startangle=90)
    axes[1, 0].set_title('Hlavní příčiny nehod', fontsize=14)

# Graf 4: Nehody podle měsíců
if 'mesic' in df.columns:
    mesic_data = df['mesic'].value_counts().sort_index()
    axes[1, 1].plot(mesic_data.index, mesic_data.values, marker='o', linewidth=2, color='green')
    axes[1, 1].set_title('Nehody podle měsíců', fontsize=14)
    axes[1, 1].set_xlabel('Měsíc')
    axes[1, 1].set_ylabel('Počet nehod')
    axes[1, 1].set_xticks(range(1, 13))
    axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("data/nehody_analyza.png", dpi=150)
print("✓ Grafy uloženy do: data/nehody_analyza.png")

# Mapa nehod (pokud jsou souřadnice)
if 'x' in df.columns and 'y' in df.columns:
    valid_coords = df[(df['x'].notna()) & (df['y'].notna())].copy()
    if len(valid_coords) > 0:
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Vzorkování pro rychlejší zobrazení
        sample_size = min(10000, len(valid_coords))
        sample = valid_coords.sample(sample_size)
        
        scatter = ax.scatter(sample['x'], sample['y'], 
                           c=sample['usmrceno_os'], 
                           cmap='YlOrRd', 
                           alpha=0.3, 
                           s=5)
        ax.set_title(f'Mapa nehod (vzorek {sample_size:,} z {len(valid_coords):,})', fontsize=16)
        ax.set_xlabel('X souřadnice')
        ax.set_ylabel('Y souřadnice')
        plt.colorbar(scatter, label='Počet usmrcených', ax=ax)
        plt.tight_layout()
        plt.savefig("data/nehody_mapa.png", dpi=150)
        print("✓ Mapa nehod uložena do: data/nehody_mapa.png")

print("\n=== ANALÝZA DOKONČENA ===")
