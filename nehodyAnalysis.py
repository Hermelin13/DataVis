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
    usmrceni_mesic = df.groupby('mesic')['usmrceno_os'].sum().sort_index()
    mesice = ['leden', 'únor', 'březen', 'duben', 'květen', 'červen',
              'červenec', 'srpen', 'září', 'říjen', 'listopad', 'prosinec']
    for mesic_num, pocet in mesic_stats.items():
        mesic_nazev = mesice[int(mesic_num)-1] if 1 <= mesic_num <= 12 else f"měsíc {mesic_num}"
        usmrceni = usmrceni_mesic.get(mesic_num, 0)
        tiskni(f"  {mesic_nazev}: {pocet:>6,} nehod, {int(usmrceni):>4} usmrcených")
tiskni()

# Denní čas
tiskni("ROZDĚLENÍ PODLE DOBY DNE")
tiskni("-" * 80)
if 'doba' in df.columns:
    doba_stats = df['doba'].value_counts()
    usmrceni_doba = df.groupby('doba')['usmrceno_os'].sum()
    for doba, pocet in doba_stats.items():
        usmrceni = usmrceni_doba.get(doba, 0)
        tiskni(f"  {doba}: {pocet:>6,} nehod, {int(usmrceni):>4} usmrcených")
tiskni()

# Den v týdnu
tiskni("ROZDĚLENÍ PODLE DNE V TÝDNU")
tiskni("-" * 80)
if 'den_v_tydnu' in df.columns:
    dny = ['pondělí', 'úterý', 'středa', 'čtvrtek', 'pátek', 'sobota', 'neděle']
    den_stats = df['den_v_tydnu'].value_counts()
    usmrceni_dny = df.groupby('den_v_tydnu')['usmrceno_os'].sum()
    dny_order = ['pondělí', 'úterý', 'středa', 'čtvrtek', 'pátek', 'sobota', 'neděle']
    for den_nazev in dny_order:
        if den_nazev in den_stats.index:
            pocet = den_stats[den_nazev]
            usmrceni = usmrceni_dny.get(den_nazev, 0)
            tiskni(f"  {den_nazev}: {pocet:>6,} nehod, {int(usmrceni):>4} usmrcených")
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

# Zavinění
tiskni("NEHODY A USMRCENÍ PODLE ZAVINĚNÍ")
tiskni("-" * 80)
if 'zavineni' in df.columns:
    zavineni_stats = df['zavineni'].value_counts()
    usmrceni_zavineni = df.groupby('zavineni')['usmrceno_os'].sum()
    for zavineni, pocet in zavineni_stats.items():
        usmrceni = usmrceni_zavineni.get(zavineni, 0)
        procento = (pocet / len(df)) * 100
        tiskni(f"  {zavineni:30} {pocet:>6,} nehod ({procento:>5.2f}%), {int(usmrceni):>4} usmrcených")
tiskni()

# Alkohol
tiskni("VLIV ALKOHOLU")
tiskni("-" * 80)
if 'alkohol_vinik' in df.columns:
    def stav_alko_drogy_row(row):
        alko_flag = str(row['alkohol_vinik']).lower() if pd.notna(row['alkohol_vinik']) else ''
        alko_popis = str(row['alkohol']).lower() if 'alkohol' in row and pd.notna(row['alkohol']) else ''
        if 'drog' in alko_popis:
            return 'drogy'
        if alko_flag == 'ano' or 'alkohol' in alko_popis:
            return 'alkohol'
        if alko_flag == 'ne':
            return 'bez alkoholu/drog'
        return 'nezjištěno'

    status_series = df.apply(stav_alko_drogy_row, axis=1)
    status_counts = status_series.value_counts()
    status_usmrceni = df.groupby(status_series)['usmrceno_os'].sum()
    total = len(df)
    for k in ['bez alkoholu/drog', 'alkohol', 'drogy', 'nezjištěno']:
        pocet = status_counts.get(k, 0)
        usmr = status_usmrceni.get(k, 0)
        fatal_rate = (usmr / pocet * 100) if pocet else 0
        podil = (pocet / total * 100) if total else 0
        tiskni(f"  {k:17}: {pocet:>6,} nehod ({podil:>5.2f}%), usmrceno {int(usmr)}, úmrtnost {fatal_rate:>5.2f}%")

    # Úmrtnost při konkrétních hladinách alkoholu (řidič)
    if 'alkohol' in df.columns:
        alkohol_hladina = df['alkohol'].fillna('Nezjištěno')
        hladina_counts = alkohol_hladina.value_counts()
        hladina_usmrceni = df.groupby(alkohol_hladina)['usmrceno_os'].sum()
        hladina_stats = (
            pd.DataFrame({'nehod': hladina_counts, 'usmrceni': hladina_usmrceni})
            .fillna(0)
        )
        hladina_stats['umrtnost_pct'] = (hladina_stats['usmrceni'] / hladina_stats['nehod']) * 100
        # report top 5 dle úmrtnosti pro kategorie s alespoň 20 záznamy
        top_hladiny = hladina_stats[hladina_stats['nehod'] >= 20].sort_values('umrtnost_pct', ascending=False).head(5)
        if not top_hladiny.empty:
            tiskni("  Nejvyšší úmrtnost podle hladiny (min 20 záznamů):")
            for name, row in top_hladiny.iterrows():
                tiskni(f"    {name}: {int(row['nehod'])} nehod, {int(row['usmrceni'])} usmrc., úmrtnost {row['umrtnost_pct']:.2f}%")
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

y_pos = range(len(top_10))
width = 0.35
bars1 = ax2.barh([i - width/2 for i in y_pos], top_10.values, width, label='Počet nehod', color='coral')
ax2.set_yticks(y_pos)
ax2.set_yticklabels(top_10.index, fontsize=9)
ax2.set_xlabel('Počet')
ax2.legend()
ax2.invert_yaxis()

for bar, value in zip(bars1, top_10.values):
    width = bar.get_width()
    ax2.text(width * 1.01, bar.get_y() + bar.get_height()/2,
             f"{value:}", va='center', ha='left', fontsize=8)

plt.tight_layout()
plt.savefig("graphs/nehody/nehody_top_lokality.png", dpi=150)
print("Graf 2: graphs/nehody/nehody_top_lokality.png")
plt.close()

# Graf 2b: Top 10 lokalit podle počtu usmrcených
fig2b, ax2b = plt.subplots(figsize=(14, 6))
top_10_usmrceni = df.groupby('zuj')['usmrceno_os'].sum().nlargest(10)

y_pos = range(len(top_10_usmrceni))
width = 0.35
bars2 = ax2b.barh([i + width/2 for i in y_pos], top_10_usmrceni.values, width, label='Počet usmrcených', color='darkred')

ax2b.set_yticks(y_pos)
ax2b.set_yticklabels(top_10_usmrceni.index, fontsize=9)
ax2b.set_xlabel('Počet usmrcených')
ax2b.legend()
ax2b.invert_yaxis()

for bar, usmr in zip(bars2, top_10_usmrceni.values):
    width = bar.get_width()
    ax2b.text(width * 1.01, bar.get_y() + bar.get_height()/2,
              f"{int(usmr)}", va='center', ha='left', fontsize=8)

plt.tight_layout()
plt.savefig("graphs/nehody/nehody_top_lokality_usmrceni.png", dpi=150)
print("Graf 2b: graphs/nehody/nehody_top_lokality_usmrceni.png")
plt.close()

# Graf 2c: Top 10 lokalit - procento usmrcených na nehodu (podle procent)
fig2c, ax2c = plt.subplots(figsize=(14, 6))
all_procenta = df.groupby('zuj')['usmrceno_os'].sum() / df['zuj'].value_counts() * 100
top_10_procenta = all_procenta.nlargest(10)
pocet_nehod_top = df['zuj'].value_counts().reindex(top_10_procenta.index)
usmrceni_top = df.groupby('zuj')['usmrceno_os'].sum().reindex(top_10_procenta.index)

y_pos = range(len(top_10_procenta))
bars3 = ax2c.barh(y_pos, top_10_procenta.values, height=0.6, color='darkred')

ax2c.set_yticks(y_pos)
ax2c.set_yticklabels(top_10_procenta.index, fontsize=9)
ax2c.set_xlabel('Procento usmrcených na nehodu (%)')
ax2c.invert_yaxis()

for bar, procento, nehod, usmr in zip(bars3, top_10_procenta.values, pocet_nehod_top.values, usmrceni_top.values):
    width = bar.get_width()
    ratio = usmr / nehod if nehod else 0
    ax2c.text(
        width * 1.01,
        bar.get_y() + bar.get_height() / 2,
        f"{procento:.2f}% \n({int(usmr)}/{int(nehod)})",
        va='center',
        ha='left',
        fontsize=7
    )

plt.tight_layout()
plt.savefig("graphs/nehody/nehody_top_lokality_procenta_usmrceni.png", dpi=150)
print("Graf 2c: graphs/nehody/nehody_top_lokality_procenta_usmrceni.png")
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

# Graf 6: Nehody podle času ve dne (hodinové intervaly)
if 'hodina' in df.columns:
    # Filtrovat: vzít jen platné hodiny (0-23), vyloučit 25 a NaN
    df_cas = df[(df['hodina'].notna()) & (df['hodina'] < 24)].copy()
    df_cas['hodina_int'] = df_cas['hodina'].astype(int)
    
    fig6, ax6 = plt.subplots(figsize=(14, 6))
    cas_data = df_cas['hodina_int'].value_counts().sort_index()
    usmrceni_cas = df_cas.groupby('hodina_int')['usmrceno_os'].sum().sort_index()
    
    x = range(len(cas_data))
    width = 0.35
    bars1 = ax6.bar([i - width/2 for i in x], cas_data.values, width, label='Počet nehod', color='coral')
    bars2 = ax6.bar([i + width/2 for i in x], usmrceni_cas.values, width, label='Počet usmrcených', color='darkred')
    
    ax6.set_xticks(x)
    ax6.set_xticklabels([f"{int(h):02d}:00" for h in cas_data.index], rotation=45, ha='right')
    ax6.set_xlabel('Čas')
    ax6.set_ylabel('Počet')
    ax6.legend()
    ax6.grid(axis='y', alpha=0.3)
    
    for bar, value in zip(bars1, cas_data.values):
        height = bar.get_height()
        ax6.text(bar.get_x() + bar.get_width()/2, height * 1.005, f"{value:}", ha='center', va='bottom', fontsize=7)
    for bar, value in zip(bars2, usmrceni_cas.values):
        height = bar.get_height()
        ax6.text(bar.get_x() + bar.get_width()/2, height * 1.005, f"{value:}", ha='center', va='bottom', fontsize=7)
    
    plt.tight_layout()
    plt.savefig("graphs/nehody/nehody_podle_casu.png", dpi=150)
    print("Graf 6: graphs/nehody/nehody_podle_casu.png")
    plt.close()

# Graf 7: Typ auta účastníků nehody
if 'typ_vozidla' in df.columns or 'vozidlo' in df.columns:
    fig7, ax7 = plt.subplots(figsize=(12, 7))
    
    # Pokus najít správný sloupec
    vozidlo_col = 'typ_vozidla' if 'typ_vozidla' in df.columns else 'vozidlo'
    typ_data = df[vozidlo_col].value_counts().head(15)
    usmrceni_typ = df.groupby(vozidlo_col)['usmrceno_os'].sum().reindex(typ_data.index)
    
    x = range(len(typ_data))
    width = 0.35
    bars1 = ax7.barh([i - width/2 for i in x], typ_data.values, width, label='Počet nehod', color='coral')
    bars2 = ax7.barh([i + width/2 for i in x], usmrceni_typ.values, width, label='Počet usmrcených', color='darkred')
    
    ax7.set_yticks(x)
    ax7.set_yticklabels(typ_data.index, fontsize=9)
    ax7.set_xlabel('Počet')
    ax7.legend()
    ax7.invert_yaxis()
    
    for bar, value in zip(bars1, typ_data.values):
        width = bar.get_width()
        ax7.text(width * 1.01, bar.get_y() + bar.get_height()/2,
                 f"{value:}", va='center', ha='left', fontsize=8)
    for bar, value in zip(bars2, usmrceni_typ.values):
        width = bar.get_width()
        ax7.text(width * 1.01, bar.get_y() + bar.get_height()/2,
                 f"{value:}", va='center', ha='left', fontsize=8)
    
    plt.tight_layout()
    plt.savefig("graphs/nehody/nehody_typ_vozidla.png", dpi=150)
    print("Graf 7: graphs/nehody/nehody_typ_vozidla.png")
    plt.close()

# Graf 8: Mapa nehod (pokud jsou souřadnice)
if 'x' in df.columns and 'y' in df.columns:
    valid_coords = df[(df['x'].notna()) & (df['y'].notna())].copy()
    if len(valid_coords) > 0:
        fig8, ax8 = plt.subplots(figsize=(12, 10))
        
        # Vzorkování pro rychlejší zobrazení
        sample_size = min(10000, len(valid_coords))
        sample = valid_coords.sample(sample_size)
        
        from matplotlib.colors import PowerNorm
        scatter = ax8.scatter(sample['x'], sample['y'], 
                           c=sample['usmrceno_os'], 
                           cmap='magma_r', 
                           norm=PowerNorm(gamma=0.25),
                           alpha=0.4, 
                           s=5)
        ax8.set_xlabel('X souřadnice')
        ax8.set_ylabel('Y souřadnice')
        cbar = plt.colorbar(scatter, label='Počet usmrcených', ax=ax8)
        cbar.ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
        plt.tight_layout()
        plt.savefig("graphs/nehody/nehody_mapa.png", dpi=150)
        print("Graf 8: graphs/nehody/nehody_mapa.png")
        plt.close()

output_file.close()
