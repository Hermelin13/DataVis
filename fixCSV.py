# fixCSV.py
# priklad
# python .\\fixCSV.py Traffic_events.csv


import argparse
import codecs
import os
import sys


def resolve_input_path(path_str: str) -> str:
    # Pokud uživatel zadal cestu (obsahuje složku) nebo absolutní cestu, použijeme ji přímo
    if os.path.isabs(path_str) or os.path.dirname(path_str):
        return os.path.expanduser(path_str)
    # Jinak hledáme v lokální složce `data/`
    return os.path.join("data", path_str)


def main():
    parser = argparse.ArgumentParser(description="Oprava kódování CSV souboru (zopakování chybných znaků).")
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

    with codecs.open(input_path, "r", encoding="utf-8-sig", errors="ignore") as f:
        bad_text = f.read()

    # Re-interpretace jako Latin-1, ignorujeme znaky, které do latin-1 nepatří
    fixed_text = bad_text.encode("latin-1", errors="ignore").decode("utf-8", errors="ignore")

    with codecs.open(output_file, "w", encoding="utf-8") as f:
        f.write(fixed_text)

    print("Hotovo – text je opraven v", output_file)


if __name__ == "__main__":
    main()