import json
import geopandas as gpd
from shapely.geometry import shape
import matplotlib.pyplot as plt
from collections import Counter

print("=== ANALÝZA CYKLOTRASY (GeoJSON) ===\n")

# 1) Načtení GeoJSON dat
with open("data/cyklotrasy_4326.geojson", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Typ: {data.get('type')}")
print(f"Počet features: {len(data.get('features', []))}\n")

features_list = data.get('features', [])

# 2) Základní statistiky z properties
print("=== ZÁKLADNÍ STATISTIKY ===")
geom_types = Counter(f['geometry']['type'] for f in features_list if f.get('geometry'))
print(f"Typy geometrie: {dict(geom_types)}")

lengths = [f['properties'].get('Shape_Leng', 0) for f in features_list if f.get('properties')]
if lengths:
    print(f"\nStatistiky délky (Shape_Leng):")
    print(f"  Min: {min(lengths):.2f} m")
    print(f"  Max: {max(lengths):.2f} m")
    print(f"  Průměr: {sum(lengths)/len(lengths):.2f} m")
    print(f"  Celková délka: {sum(lengths)/1000:.2f} km")

# 3) Statistiky obcí
obce = [f['properties'].get('ON_1') for f in features_list if f.get('properties') and f['properties'].get('ON_1')]
unique_obce = set(obce)
print(f"\nPočet unikátních obcí (ON_1): {len(unique_obce)}")
print(f"\nTop 10 obcí podle počtu tras:")
for obec, count in Counter(obce).most_common(10):
    print(f"  {obec}: {count} tras")

# 4) Rozsah souřadnic
all_coords = []
for f in features_list:
    if f.get('geometry') and f['geometry']['type'] == 'LineString':
        all_coords.extend(f['geometry']['coordinates'])

if all_coords:
    lons = [c[0] for c in all_coords]
    lats = [c[1] for c in all_coords]
    print(f"\nRozsah souřadnic (WGS84):")
    print(f"  Longitude: {min(lons):.6f} až {max(lons):.6f}")
    print(f"  Latitude: {min(lats):.6f} až {max(lats):.6f}")

# 5) Převod na GeoDataFrame pro pokročilou analýzu
print("\n=== GEOPANDAS ANALÝZA ===")
gdf_features = []
for f in features_list:
    geom = shape(f["geometry"])
    props = f["properties"].copy()
    props["geometry"] = geom
    gdf_features.append(props)

gdf = gpd.GeoDataFrame(gdf_features, geometry="geometry", crs="EPSG:4326")

# Převod do metrického systému pro přesnější výpočty
gdf_utm = gdf.to_crs("EPSG:5514")  # S-JTSK pro Českou republiku
gdf_utm["length_calculated"] = gdf_utm.geometry.length

print(f"Celková délka (vypočtená v UTM): {gdf_utm['length_calculated'].sum()/1000:.2f} km")
print(f"Průměrná délka trasy: {gdf_utm['length_calculated'].mean():.2f} m")
print(f"Nejdelší trasa: {gdf_utm['length_calculated'].max():.2f} m")
print(f"Nejkratší trasa: {gdf_utm['length_calculated'].min():.2f} m")

# 6) Vzorová data
print("\n=== VZOROVÉ ZÁZNAMY (prvních 5) ===")
print(gdf[["NAZEV", "ON_1", "Shape_Leng"]].head())

# 7) Vizualizace
print("\n=== GENEROVÁNÍ VIZUALIZACE ===")
fig, ax = plt.subplots(1, 1, figsize=(12, 10))
gdf.plot(ax=ax, linewidth=0.8, color='blue', alpha=0.6)
ax.set_title("Mapa cyklotras (WGS84)", fontsize=16)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
plt.tight_layout()
plt.savefig("data/cyklotrasy_mapa.png", dpi=150)
print("Mapa uložena do: data/cyklotrasy_mapa.png")
plt.show()