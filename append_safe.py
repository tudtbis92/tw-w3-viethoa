import os
import sys

def append_safe(file_path, chunk_path, line_count_before):
    # Read the main file with UTF-8-SIG to handle existing content correctly
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
            lines = f.readlines()
    else:
        lines = []
    
    # Keep only the lines up to the specified count
    correct_lines = lines[:line_count_before]
    
    # Read the new chunk file (written with write_file, which is UTF-8)
    with open(chunk_path, 'r', encoding='utf-8') as f:
        chunk_lines = f.readlines()
    
    # Combine
    final_content = correct_lines + chunk_lines
    
    # Write back with UTF-8-SIG (BOM)
    with open(file_path, 'w', encoding='utf-8-sig', newline='') as f:
        f.writelines(final_content)
    
    print(f"Successfully appended {len(chunk_lines)} lines to {file_path}. New total: {len(final_content)}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python append_safe.py <file_path> <chunk_path> <line_count_before>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    chunk_path = sys.argv[2]
    line_count_before = int(sys.argv[3])
    
    append_safe(file_path, chunk_path, line_count_before)
