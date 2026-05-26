import os
import sys

def fix_encoding(file_path, chunk_path, line_count_before):
    # Read the original lines from the main file
    with open(file_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
        lines = f.readlines()
    
    # Keep only the lines before the faulty append
    correct_lines = lines[:line_count_before]
    
    # Read the chunk file
    with open(chunk_path, 'r', encoding='utf-8') as f:
        chunk_lines = f.readlines()
    
    # Combine
    final_content = correct_lines + chunk_lines
    
    # Write back with UTF-8-SIG (BOM)
    with open(file_path, 'w', encoding='utf-8-sig', newline='') as f:
        f.writelines(final_content)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python fix_encoding.py <file_path> <chunk_path> <line_count_before>")
        sys.exit(1)
    
    fix_encoding(sys.argv[1], sys.argv[2], int(sys.argv[3]))
