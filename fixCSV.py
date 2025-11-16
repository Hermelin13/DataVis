# fixCSV.py
# priklad
# python .\\fixCSV.py Traffic_events.csv


import argparse
import codecs
import os
import sys


def resolve_input_path(path_str: str) -> str:
    if os.path.isabs(path_str) or os.path.dirname(path_str):
        return os.path.expanduser(path_str)
    return os.path.join("data", path_str)


def main():
    parser = argparse.ArgumentParser(description="Oprava kódování CSV souboru.")
    parser.add_argument("input", nargs="?", default="Traffic_delays.csv",
                        help="Vstupní CSV soubor (pokud není zadán, použije se 'Traffic_delays.csv' ze složky data/)."
                        )
    args = parser.parse_args()

    input_path = resolve_input_path(args.input)

    if not os.path.exists(input_path):
        print(f"Chyba: soubor nenalezen: {input_path}")
        sys.exit(1)

    input_dir = os.path.dirname(input_path) or "data"
    base = os.path.basename(input_path)
    output_file = os.path.join(input_dir, f"opraveno_{base}")

    # Načíst soubor
    with open(input_path, "rb") as f:
        raw_bytes = f.read()
    
    # Odstranit BOM pokud existuje
    if raw_bytes.startswith(b'\xef\xbb\xbf'):
        raw_bytes = raw_bytes[3:]
        print("Odstraněn UTF-8 BOM")
    
    # Dekódovat jako UTF-8
    try:
        content = raw_bytes.decode('utf-8')
    except UnicodeDecodeError:
        # Fallback na windows-1250
        content = raw_bytes.decode('windows-1250', errors='replace')
    
    # Chybných znaků na správné české znaky
    # Tyto znaky vznikají špatnou interpretací UTF-8 jako Latin-1
    char_map = {
        'Ä\x8d': 'č',   # č
        'Ä�': 'č',      # č - další varianta (replacement char)
        'Ä\x8c': 'Č',   # Č
        'ÄŒ': 'Č',      # Č - další varianta
        'Å™': 'ř',      # ř - POZOR: musí být jako string, ne \x99
        'Å\x99': 'ř',   # ř - alternativa
        'Å\x98': 'Ř',   # Ř
        'Å˜': 'Ř',      # Ř - alternativa
        'Ä\x9b': 'ě',   # ě
        'Ä›': 'ě',      # ě - další varianta
        'Ä\x9a': 'Ě',   # Ě
        'Äš': 'Ě',      # Ě - další varianta
        'Å¡': 'š',      # š
        'Å ': 'Š',      # Š
        'Á ': 'Š',      # Š - další varianta
        'Å\xa0': 'Š',   # Š - varianta s non-breaking space
        'Å¾': 'ž',      # ž
        'Å½': 'Ž',      # Ž
        'Ã¡': 'á',      # á
        'Ã\xa1': 'á',   # á - alternativa
        'Ã': 'Á',       # Á
        'Ã©': 'é',      # é
        'Ã\xa9': 'é',   # é - alternativa
        'Á©': 'é',      # é - další varianta
        'Ã‰': 'É',      # É
        'Á‰': 'É',      # É - další varianta
        'Ã­': 'í',      # í
        'Ã\xad': 'í',   # í - alternativa
        'Á­': 'í',      # í - další varianta
        'ÃŒ': 'Í',      # Í
        'Ã\x8d': 'Í',   # Í - alternativa
        'Ã³': 'ó',      # ó
        'Ã\xb3': 'ó',   # ó - alternativa
        'Ã"': 'Ó',      # Ó
        'Ãº': 'ú',      # ú
        'Ã\xba': 'ú',   # ú - alternativa
        'Ýº': 'ú',      # ú - další varianta
        'Ãš': 'Ú',      # Ú
        'Áš': 'Ú',      # Ú - další varianta
        'Å¯': 'ů',      # ů
        'Å\xaf': 'ů',   # ů - alternativa
        'Å®': 'Ů',      # Ů
        'Ã½': 'ý',      # ý
        'Ã\xbd': 'ý',   # ý - alternativa
        'Á½': 'ý',      # ý - další varianta
        'Ã\x9d': 'Ý',   # Ý
        'Á': 'Ý',       # Ý - další varianta
        'Ä\x8f': 'ď',   # ď
        'Ä\x8e': 'Ď',   # Ď
        'Å¥': 'ť',      # ť
        'Å\xa5': 'ť',   # ť - alternativa
        'Å¤': 'Ť',      # Ť
        'Á¼': 'ü',      # ü - německé u s dvěma tečkami
        'Ý¼': 'ü',      # ü - další varianta
        'Å\x88': 'ň',   # ň
        'Åˆ': 'ň',      # ň - další varianta
        'Å\x87': 'Ň',   # Ň
        'Å‡': 'Ň',      # Ň - další varianta
        'Â': '',        # Odstranit Â
    }
    
    # Opravit znaky
    replacements = 0
    for bad, good in char_map.items():
        if bad in content:
            count = content.count(bad)
            content = content.replace(bad, good)
            replacements += count
    
    # Uložení jako čistý UTF-8 bez BOM
    with open(output_file, "w", encoding="utf-8", newline='') as f:
        f.write(content)
    
    print(f"Text opraven v {output_file}")


if __name__ == "__main__":
    main()