import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import sys

# Nastavení pro český výstup
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

## fix nesprávé, přenosti

# Otevření souboru pro zápis výstupu
output_file = open('graphs/nehody/nehody_analyza_report.txt', 'w', encoding='utf-8')

def tiskni(text=""):
    output_file.write(text + '\n')

# Načtení dat
df = pd.read_csv("data/dopravni_nehody.csv", low_memory=False)

# Základní statistiky
tiskni("ZÁKLADNÍ PŘEHLED")
tiskni("-" * 80)
tiskni(f"Časové rozmezí: {df['datum'].min()} až {df['datum'].max()}")
tiskni(f"Počet unikátních lokalit: {df['zuj'].nunique()}")
tiskni(f"Počet unikátních nehod: {df['id_nehody'].nunique()}")
tiskni(f"Počet zaznamenaných záznamů: {len(df):,}")
tiskni()

# Statistiky následků
tiskni("STATISTIKY NÁSLEDKŮ")
tiskni("-" * 80)
tiskni(f"Celkem usmrcených osob: {df['usmrceno_os'].sum():,}")
tiskni(f"Celkem těžce zraněných: {df['tezce_zran_os'].sum():,}")
tiskni(f"Celkem lehce zraněných: {df['lehce_zran_os'].sum():,}")
tiskni(f"Celková hmotná škoda: {df['hmotna_skoda'].sum():,.0f} Kč")
tiskni(f"Průměrná škoda na nehodu: {df['hmotna_skoda'].mean():,.0f} Kč")
tiskni()

# Časové trendy
tiskni("ROZDĚLENÍ PODLE ROKŮ")
tiskni("-" * 80)
rok_stats = df['rok'].value_counts().sort_index()
for rok, pocet in rok_stats.items():
    usmrceni = df[df['rok'] == rok]['usmrceno_os'].sum()
    tiskni(f"  {rok}: {pocet:>6,} nehod, {usmrceni:>4} usmrcených")
tiskni()

# Měsíční statistiky
tiskni("ROZDĚLENÍ PODLE MĚSÍCŮ")
tiskni("-" * 80)
if 'mesic' in df.columns:
    mesic_stats = df['mesic'].value_counts().sort_index()
    mesice = ['leden', 'únor', 'březen', 'duben', 'květen', 'červen',
              'červenec', 'srpen', 'září', 'říjen', 'listopad', 'prosinec']
    for mesic_num, pocet in mesic_stats.items():
        mesic_nazev = mesice[int(mesic_num)-1] if 1 <= mesic_num <= 12 else f"měsíc {mesic_num}"
        tiskni(f"  {mesic_nazev}: {pocet:,} nehod")
tiskni()

# Denní čas
tiskni("ROZDĚLENÍ PODLE DOBY DNE")
tiskni("-" * 80)
if 'doba' in df.columns:
    doba_stats = df['doba'].value_counts()
    for doba, pocet in doba_stats.items():
        tiskni(f"  {doba}: {pocet:,} nehod")
tiskni()

# Den v týdnu
tiskni("ROZDĚLENÍ PODLE DNE V TÝDNU")
tiskni("-" * 80)
if 'den_v_tydnu' in df.columns:
    dny = ['pondělí', 'úterý', 'středa', 'čtvrtek', 'pátek', 'sobota', 'neděle']
    den_stats = df['den_v_tydnu'].value_counts().sort_index()
    for den_num, pocet in den_stats.items():
        try:
            den_int = int(den_num)
            den_nazev = dny[den_int-1] if 1 <= den_int <= 7 else f"den {den_num}"
        except (ValueError, TypeError, IndexError):
            den_nazev = str(den_num)
        tiskni(f"  {den_nazev}: {pocet:,} nehod")
tiskni()

# Top lokality
tiskni("TOP 15 LOKALIT PODLE POČTU NEHOD")
tiskni("-" * 80)
top_lokality = df['zuj'].value_counts().head(15)  
for idx, (lokace, pocet) in enumerate(top_lokality.items(), 1):
    usmrceni = df[df['zuj'] == lokace]['usmrceno_os'].sum()
    tiskni(f"  {idx:2}. {lokace:25} {pocet:>6,} nehod, {usmrceni:>4} usmrcených")
tiskni()

# Hlavní příčiny
tiskni("HLAVNÍ PŘÍČINY NEHOD")
tiskni("-" * 80)
if 'hlavni_pricina' in df.columns:
    priciny = df['hlavni_pricina'].value_counts().head(10)
    for pricina, pocet in priciny.items():
        procento = (pocet / len(df)) * 100
        tiskni(f"  {pricina:35} {pocet:>6,} ({procento:>5.2f}%)")
tiskni()

# Alkohol
tiskni("VLIV ALKOHOLU")
tiskni("-" * 80)
if 'alkohol_vinik' in df.columns:
    alkohol_stats = df['alkohol_vinik'].value_counts()
    celkem_s_alkoholem = alkohol_stats.get('ano', 0)
    procento_alkohol = (celkem_s_alkoholem / len(df)) * 100
    tiskni(f"  Nehody s alkoholem: {celkem_s_alkoholem:,} ({procento_alkohol:.2f}%)")
    
    # Úsmrtnost při alkoholu
    usmrceni_alkohol = df[df['alkohol_vinik'] == 'ano']['usmrceno_os'].sum()
    usmrceni_celkem = df['usmrceno_os'].sum()
    if usmrceni_celkem > 0:
        procento_smrti = (usmrceni_alkohol / usmrceni_celkem) * 100
        tiskni(f"  Usmrcení při alkoholu: {usmrceni_alkohol} ({procento_smrti:.1f}% všech úmrtí)")
tiskni()

# Stav vozovky
tiskni("VLIV STAVU VOZOVKY")
tiskni("-" * 80)
if 'stav_vozovky' in df.columns:
    stav_stats = df['stav_vozovky'].value_counts().head(10)
    for stav, pocet in stav_stats.items():
        procento = (pocet / len(df)) * 100
        tiskni(f"  {stav:25} {pocet:>6,} ({procento:>5.2f}%)")
tiskni()

# Počasí
tiskni("VLIV POVĚTRNOSTNÍCH PODMÍNEK")
tiskni("-" * 80)
if 'povetrnostni_podm' in df.columns:
    pocasi_stats = df['povetrnostni_podm'].value_counts().head(10)
    for pocasi, pocet in pocasi_stats.items():
        procento = (pocet / len(df)) * 100
        tiskni(f"  {pocasi:25} {pocet:>6,} ({procento:>5.2f}%)")
tiskni()

# Geografická analýza
tiskni("GEOGRAFICKÁ DATA")
tiskni("-" * 80)
if 'x' in df.columns and 'y' in df.columns:
    # Filtrovat validní souřadnice
    valid_coords = df[(df['x'].notna()) & (df['y'].notna())]
    tiskni(f"Záznamy s platnou GPS: {len(valid_coords):,} ({len(valid_coords)/len(df)*100:.1f}%)")
    if len(valid_coords) > 0:
        tiskni(f"Rozsah X: {valid_coords['x'].min():,.0f} až {valid_coords['x'].max():,.0f}")
        tiskni(f"Rozsah Y: {valid_coords['y'].min():,.0f} až {valid_coords['y'].max():,.0f}")
tiskni()

# Vizualizace
# Graf 1: Nehody podle roků
fig1, ax1 = plt.subplots(figsize=(10, 6))
rok_data = df['rok'].value_counts().sort_index()
ax1.bar(rok_data.index, rok_data.values, color='steelblue')
ax1.set_title('Počet nehod podle roků', fontsize=14, fontweight='bold')
ax1.set_xlabel('Rok')
ax1.set_ylabel('Počet nehod')
ax1.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("graphs/nehody/nehody_podle_roku.png", dpi=150)
print("Graf 1: graphs/nehody/nehody_podle_roku.png")
plt.close()

# Graf 2: Top 10 lokalit
fig2, ax2 = plt.subplots(figsize=(10, 6))
top_10 = df['zuj'].value_counts().head(10)
ax2.barh(range(len(top_10)), top_10.values, color='coral')
ax2.set_yticks(range(len(top_10)))
ax2.set_yticklabels(top_10.index, fontsize=9)
ax2.set_title('Top 10 lokalit podle počtu nehod', fontsize=14, fontweight='bold')
ax2.set_xlabel('Počet nehod')
ax2.invert_yaxis()
plt.tight_layout()
plt.savefig("graphs/nehody/nehody_top_lokality.png", dpi=150)
print("Graf 2: graphs/nehody/nehody_top_lokality.png")
plt.close()

# Graf 3: Hlavní příčiny
if 'hlavni_pricina' in df.columns:
    fig3, ax3 = plt.subplots(figsize=(10, 8))
    priciny_top = df['hlavni_pricina'].value_counts().head(8)
    ax3.pie(priciny_top.values, labels=priciny_top.index, autopct='%1.1f%%', startangle=90)
    ax3.set_title('Hlavní příčiny nehod', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig("graphs/nehody/nehody_priciny.png", dpi=150)
    print("Graf 3: graphs/nehody/nehody_priciny.png")
    plt.close()

# Graf 4: Nehody podle měsíců
if 'mesic' in df.columns:
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    mesic_data = df['mesic'].value_counts().sort_index()
    ax4.plot(mesic_data.index, mesic_data.values, marker='o', linewidth=2, color='green', markersize=8)
    ax4.set_title('Nehody podle měsíců', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Měsíc')
    ax4.set_ylabel('Počet nehod')
    ax4.set_xticks(range(1, 13))
    ax4.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("graphs/nehody/nehody_podle_mesicu.png", dpi=150)
    print("Graf 4: graphs/nehody/nehody_podle_mesicu.png")
    plt.close()

# Graf 5: Mapa nehod (pokud jsou souřadnice)
if 'x' in df.columns and 'y' in df.columns:
    valid_coords = df[(df['x'].notna()) & (df['y'].notna())].copy()
    if len(valid_coords) > 0:
        fig5, ax5 = plt.subplots(figsize=(12, 10))
        
        # Vzorkování pro rychlejší zobrazení
        sample_size = min(10000, len(valid_coords))
        sample = valid_coords.sample(sample_size)
        
        scatter = ax5.scatter(sample['x'], sample['y'], 
                           c=sample['usmrceno_os'], 
                           cmap='YlOrRd', 
                           alpha=0.3, 
                           s=5)
        ax5.set_title(f'Mapa nehod (vzorek {sample_size:,} z {len(valid_coords):,})', fontsize=16, fontweight='bold')
        ax5.set_xlabel('X souřadnice')
        ax5.set_ylabel('Y souřadnice')
        plt.colorbar(scatter, label='Počet usmrcených', ax=ax5)
        plt.tight_layout()
        plt.savefig("graphs/nehody/nehody_mapa.png", dpi=150)
        print("Graf 5: graphs/nehody/nehody_mapa.png")
        plt.close()

output_file.close()
