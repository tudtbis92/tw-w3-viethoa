import glob

# Load translations from all chunk files
origin_dict = {}
with open("text_origin/text/db/advice_levels__.loc.tsv", "r", encoding="utf-8-sig") as f:
    for line in f:
        parts = line.split("\t")
        if len(parts) >= 2:
            origin_dict[parts[0]] = parts[1]

translated_dict = {}
for file in glob.glob("chunk_advice_text_*.tmp"):
    with open(file, "r", encoding="utf-8-sig") as f:
        for line in f:
            parts = line.split("\t")
            if len(parts) >= 2:
                key = parts[0]
                text = parts[1]
                if key in origin_dict and text != origin_dict[key]:
                    translated_dict[key] = line

# Load current translated file (first 2950 lines)
current_translated_lines = []
with open("text_translated/text/db/advice_levels__.loc.tsv", "r", encoding="utf-8-sig") as f:
    current_translated_lines = f.readlines()

# Load origin file
with open("text_origin/text/db/advice_levels__.loc.tsv", "r", encoding="utf-8-sig") as f:
    origin_lines = f.readlines()

output_lines = current_translated_lines.copy()

translated_count = 0
untranslated_count = 0
# Append the missing lines from length of current up to the end
for i in range(len(current_translated_lines), len(origin_lines)):
    line = origin_lines[i]
    key = line.split("\t")[0]
    if key in translated_dict:
        output_lines.append(translated_dict[key])
        translated_count += 1
    else:
        output_lines.append(line)
        untranslated_count += 1

with open("text_translated/text/db/advice_levels__.loc.tsv", "w", encoding="utf-8-sig", newline="") as f:
    f.writelines(output_lines)

print(f"Recovered {translated_count} translated lines. {untranslated_count} lines remain untranslated.")
print(f"New total length: {len(output_lines)}")
