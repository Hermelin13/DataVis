import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import sys

# Nastavení pro český výstup
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# Otevření souboru pro zápis výstupu
output_file = open('graphs/nehody/nehody_analyza_report.txt', 'w', encoding='utf-8')

def tiskni(text=""):
    output_file.write(text + '\n')

# Načtení dat
df = pd.read_csv("data/dopravni_nehody.csv", low_memory=False)

# Oprava překlepů v textových sloupcích
typo_map = {"nesprávé": "nesprávné", "přenosti": "přednosti"}
for col in df.select_dtypes(include=["object"]):
    df[col] = df[col].replace(typo_map, regex=True)

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
fig1, ax1 = plt.subplots(figsize=(11, 6))
rok_data = df['rok'].value_counts().sort_index()
usmrceni_rok = df.groupby('rok')['usmrceno_os'].sum().sort_index()

x = range(len(rok_data))
width = 0.35
bars1 = ax1.bar([i - width/2 for i in x], rok_data.values, width, label='Počet nehod', color='coral')
bars2 = ax1.bar([i + width/2 for i in x], usmrceni_rok.values, width, label='Počet usmrcených', color='darkred')

ax1.set_xticks(x)
ax1.set_xticklabels(rok_data.index)
ax1.set_xlabel('Rok')
ax1.set_ylabel('Počet')
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

# Počty nad sloupci
for bar, value in zip(bars1, rok_data.values):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, height * 1.005,
             f"{value:}", ha='center', va='bottom', fontsize=8, rotation=0)
for bar, value in zip(bars2, usmrceni_rok.values):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, height * 1.005,
             f"{value:}", ha='center', va='bottom', fontsize=8, rotation=0)

plt.tight_layout()
plt.savefig("graphs/nehody/nehody_podle_roku.png", dpi=150)
print("Graf 1: graphs/nehody/nehody_podle_roku.png")
plt.close()

# Graf 2: Top 10 lokalit
fig2, ax2 = plt.subplots(figsize=(13, 6))
top_10 = df['zuj'].value_counts().head(10)
usmrceni_lokality = df.groupby('zuj')['usmrceno_os'].sum().reindex(top_10.index)

y_pos = range(len(top_10))
width = 0.35
bars1 = ax2.barh([i - width/2 for i in y_pos], top_10.values, width, label='Počet nehod', color='coral')
bars2 = ax2.barh([i + width/2 for i in y_pos], usmrceni_lokality.values, width, label='Počet usmrcených', color='darkred')

ax2.set_yticks(y_pos)
ax2.set_yticklabels(top_10.index, fontsize=9)
ax2.set_xlabel('Počet')
ax2.legend()
ax2.invert_yaxis()

for bar, value in zip(bars1, top_10.values):
    width = bar.get_width()
    ax2.text(width * 1.01, bar.get_y() + bar.get_height()/2,
             f"{value:}", va='center', ha='left', fontsize=8)
for bar, value in zip(bars2, usmrceni_lokality.values):
    width = bar.get_width()
    ax2.text(width * 1.01, bar.get_y() + bar.get_height()/2,
             f"{value:}", va='center', ha='left', fontsize=8)

plt.tight_layout()
plt.savefig("graphs/nehody/nehody_top_lokality.png", dpi=150)
print("Graf 2: graphs/nehody/nehody_top_lokality.png")
plt.close()

# Graf 3: Hlavní příčiny
if 'hlavni_pricina' in df.columns:
    fig3, ax3 = plt.subplots(figsize=(10, 8))
    priciny_top = df['hlavni_pricina'].value_counts().head(8)
    values = priciny_top.values
    labels = priciny_top.index
    total = values.sum()
    wedges, _, autotexts = ax3.pie(
        values,
        labels=None,
        autopct=lambda pct: f"{pct:.1f}%" if pct >= 5 else '',
        startangle=135,
        pctdistance=0.85,
        textprops={'fontsize': 10}
    )

    for wedge, autotext, val in zip(wedges, autotexts, values):
        pct = (val / total) * 100
        if pct < 5:
            continue

    legend_labels = [f"{lbl} ({(val/total)*100:.1f}%)" for lbl, val in zip(labels, values)]
    ax3.legend(wedges, legend_labels, title='Příčiny', bbox_to_anchor=(0.95, 0.5), loc='center left')
    plt.subplots_adjust(right=0.78)
    plt.tight_layout()
    plt.savefig("graphs/nehody/nehody_priciny.png", dpi=150)
    print("Graf 3: graphs/nehody/nehody_priciny.png")
    plt.close()

# Graf 4: Nehody podle měsíců
if 'mesic' in df.columns:
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    mesic_data = df['mesic'].value_counts().sort_index()
    usmrceni_mesic = df.groupby('mesic')['usmrceno_os'].sum().sort_index()
    
    ax4_2 = ax4.twinx()
    ax4.plot(mesic_data.index, mesic_data.values, marker='o', linewidth=2, color='coral', markersize=8, label='Počet nehod')
    ax4_2.plot(usmrceni_mesic.index, usmrceni_mesic.values, marker='s', linewidth=2, color='darkred', markersize=8, label='Počet usmrcených')
    
    ax4.set_xlabel('Měsíc')
    ax4.set_ylabel('Počet nehod', color='coral')
    ax4_2.set_ylabel('Počet usmrcených', color='darkred')
    ax4.set_xticks(range(1, 13))
    ax4.tick_params(axis='y', labelcolor='coral')
    ax4_2.tick_params(axis='y', labelcolor='darkred')
    ax4.grid(True, alpha=0.3)
    lines1, labels1 = ax4.get_legend_handles_labels()
    lines2, labels2 = ax4_2.get_legend_handles_labels()
    ax4.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    plt.tight_layout()
    plt.savefig("graphs/nehody/nehody_podle_mesicu.png", dpi=150)
    print("Graf 4: graphs/nehody/nehody_podle_mesicu.png")
    plt.close()

# Graf 5: Nehody podle dne v týdnu
if 'den_v_tydnu' in df.columns:
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    dny_data = df['den_v_tydnu'].value_counts()
    usmrceni_dny = df.groupby('den_v_tydnu')['usmrceno_os'].sum()
    dny_order = ['pondělí', 'úterý', 'středa', 'čtvrtek', 'pátek', 'sobota', 'neděle']
    
    # Seřadit podle pořadí dní
    dny_data = dny_data.reindex([d for d in dny_order if d in dny_data.index])
    usmrceni_dny = usmrceni_dny.reindex([d for d in dny_order if d in usmrceni_dny.index])
    
    x = range(len(dny_data))
    width = 0.35
    bars1 = ax5.bar([i - width/2 for i in x], dny_data.values, width, label='Počet nehod', color='coral')
    bars2 = ax5.bar([i + width/2 for i in x], usmrceni_dny.values, width, label='Počet usmrcených', color='darkred')
    
    ax5.set_xticks(x)
    ax5.set_xticklabels(dny_data.index, rotation=45, ha='right')
    ax5.set_ylabel('Počet')
    ax5.legend()
    ax5.grid(axis='y', alpha=0.3)
    
    for bar, value in zip(bars1, dny_data.values):
        height = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width()/2, height * 1.005, f"{value:}", ha='center', va='bottom', fontsize=8)
    for bar, value in zip(bars2, usmrceni_dny.values):
        height = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width()/2, height * 1.005, f"{value:}", ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig("graphs/nehody/nehody_podle_dne.png", dpi=150)
    print("Graf 5: graphs/nehody/nehody_podle_dne.png")
    plt.close()

# Graf 6: Mapa nehod (pokud jsou souřadnice)
if 'x' in df.columns and 'y' in df.columns:
    valid_coords = df[(df['x'].notna()) & (df['y'].notna())].copy()
    if len(valid_coords) > 0:
        fig6, ax6 = plt.subplots(figsize=(12, 10))
        
        # Vzorkování pro rychlejší zobrazení
        sample_size = min(10000, len(valid_coords))
        sample = valid_coords.sample(sample_size)
        
        from matplotlib.colors import PowerNorm
        scatter = ax6.scatter(sample['x'], sample['y'], 
                           c=sample['usmrceno_os'], 
                           cmap='magma_r', 
                           norm=PowerNorm(gamma=0.25),
                           alpha=0.4, 
                           s=5)
        ax6.set_xlabel('X souřadnice')
        ax6.set_ylabel('Y souřadnice')
        cbar = plt.colorbar(scatter, label='Počet usmrcených', ax=ax6)
        cbar.ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
        plt.tight_layout()
        plt.savefig("graphs/nehody/nehody_mapa.png", dpi=150)
        print("Graf 6: graphs/nehody/nehody_mapa.png")
        plt.close()

output_file.close()
