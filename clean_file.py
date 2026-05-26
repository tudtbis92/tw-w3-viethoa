import os
import re

file_path = 'text_translated/text/db/ancillaries__.loc.tsv'
origin_path = 'text_origin/text/db/ancillaries__.loc.tsv'

# Read all original keys in order
origin_keys = []
with open(origin_path, 'r', encoding='utf-8-sig') as f:
    for i, line in enumerate(f):
        if i < 2: continue # skip header
        parts = line.split('\t')
        if parts:
            origin_keys.append(parts[0])

# Read current translated file
with open(file_path, 'rb') as f:
    raw_content = f.read()

if raw_content.startswith(b'\xef\xbb\xbf'):
    raw_content = raw_content[3:]

content = raw_content.decode('utf-8', errors='replace')
# Remove all newlines to make it one flat string for easier tokenization
content = content.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
# Normalize spaces
content = re.sub(r'\s+', ' ', content)

# Create a mapping of key -> (text, tooltip)
translated_map = {}

# Use regex to find all key-textnd-tooltip patterns
# This is tricky because text can contain spaces. 
# But keys always start with 'ancillaries_'.
# Values are usually delimited by tabs.

# Let's split by the origin keys we know
import re
# Build a big regex of all keys (sorted by length descending to match longest first)
# For efficiency, we'll just look for the keys in order in the flat string.

current_pos = 0
for i, key in enumerate(origin_keys):
    # Search for this key starting from current_pos
    idx = content.find(key, current_pos)
    if idx != -1:
        # Found the key. Now find the next key to determine the value range
        next_key = origin_keys[i+1] if i+1 < len(origin_keys) else None
        
        val_start = idx + len(key)
        if next_key:
            val_end = content.find(next_key, val_start)
            if val_end == -1: # fallback
                 val_end = len(content)
        else:
            val_end = len(content)
            
        value_segment = content[val_start:val_end].strip()
        # Segment should contain: TAB [TEXT] TAB [TOOLTIP]
        # Since we flattened spaces, let's try to recover columns.
        # Most of our values end with 'false' or 'true'.
        
        # If the segment ends with 'false' or 'true', that's our tooltip.
        tooltip = ""
        text = ""
        if value_segment.endswith("false"):
            tooltip = "false"
            text = value_segment[:-5].strip()
        elif value_segment.endswith("true"):
            tooltip = "true"
            text = value_segment[:-4].strip()
        else:
            text = value_segment
            
        translated_map[key] = (text, tooltip)
        current_pos = val_end
    else:
        # Key not found in current translation
        pass

# Re-write the file from scratch
with open(file_path, 'w', encoding='utf-8-sig', newline='\r\n') as f:
    f.write("key\ttext\ttooltip\n")
    f.write("#Loc;1;text/db/ancillaries__.loc\t\t\n")
    
    count = 0
    for key in origin_keys:
        if key in translated_map:
            text, tooltip = translated_map[key]
            f.write(f"{key}\t{text}\t{tooltip}\n")
            count += 1
        else:
            # Stop at the first missing key to keep line count correct
            break

print(f"Reconstruction complete. Translated keys: {count}")
