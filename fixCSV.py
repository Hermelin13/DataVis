# fixCSV.py
import codecs

input_file = "Traffic_delays.csv"
output_file = "opraveno_Traffic_delays.csv"

with codecs.open(input_file, "r", encoding="utf-8-sig", errors="ignore") as f:
    bad_text = f.read()

# Re-interpretace jako Latin-1, ignorujeme znaky, které do latin-1 nepatří
fixed_text = bad_text.encode("latin-1", errors="ignore").decode("utf-8", errors="ignore")

with codecs.open(output_file, "w", encoding="utf-8") as f:
    f.write(fixed_text)

print("Hotovo – text je opraven v", output_file)