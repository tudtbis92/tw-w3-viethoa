import os

def fix_encoding(file_path, chunk_path, line_count_before):
    # Read the main file with detected/standard encoding
    # Based on observation, the file was likely UTF-8 but the append used system default (CP1252/UTF-16)
    # causing Mojibake when read as UTF-8 later.
    
    # We will read the original lines from the main file (up to line_count_before)
    # and then re-append the chunk correctly.
    
    with open(file_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
        lines = f.readlines()
    
    # Keep only the lines before the faulty append
    correct_lines = lines[:line_count_before]
    
    # Read the chunk file (which was written with write_file, so it should be clean UTF-8)
    with open(chunk_path, 'r', encoding='utf-8') as f:
        chunk_lines = f.readlines()
    
    # Combine
    final_content = correct_lines + chunk_lines
    
    # Write back with UTF-8-SIG (BOM)
    with open(file_path, 'w', encoding='utf-8-sig', newline='') as f:
        f.writelines(final_content)

if __name__ == "__main__":
    fix_encoding(
        'text_translated/text/db/advice_levels__.loc.tsv', 
        'chunk_advice_text_8.tmp', 
        2950
    )
