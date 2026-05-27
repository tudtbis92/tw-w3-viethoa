import sys
import os
import glob
import re

def merge_chunks(file_name_no_ext):
    chunk_dir = "chunks"
    if not os.path.exists(chunk_dir):
        print(f"Error: Chunk directory {chunk_dir} not found.")
        return

    output_path = os.path.join("text_translated", "text", "db", f"{file_name_no_ext}.tsv")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Find all translated chunk files: filename_chunk_translated_x.tsv
    translated_pattern = os.path.join(chunk_dir, f"{file_name_no_ext}_chunk_translated_*.tsv")
    translated_files = glob.glob(translated_pattern)
    
    if not translated_files:
        print(f"Error: No translated chunks found for {file_name_no_ext} in {chunk_dir}.")
        return

    # Sort numerically based on the 'x' at the end
    def get_chunk_num(filename):
        match = re.search(r'chunk_translated_(\d+)\.tsv$', filename)
        return int(match.group(1)) if match else 0

    translated_files.sort(key=get_chunk_num)

    first_file = True
    with open(output_path, 'w', encoding='utf-8') as outfile:
        for chunk_file in translated_files:
            with open(chunk_file, 'r', encoding='utf-8') as infile:
                lines = infile.readlines()
                if not lines:
                    continue
                
                if first_file:
                    # Write everything from the first file
                    outfile.writelines(lines)
                    first_file = False
                else:
                    # Skip the first 2 header lines for subsequent files
                    if len(lines) > 2:
                        outfile.writelines(lines[2:])

    print(f"Merged {len(translated_files)} chunks into {output_path}")

    # Cleanup: Delete origin chunks and translated chunks for this file
    # Patterns: filename_chunk_x.tsv and filename_chunk_translated_x.tsv
    # We use a pattern that matches both original and translated chunks
    all_chunks_pattern = os.path.join(chunk_dir, f"{file_name_no_ext}_chunk_*.tsv")
    files_to_delete = glob.glob(all_chunks_pattern)
    for f in files_to_delete:
        try:
            os.remove(f)
        except OSError as e:
            print(f"Error deleting {f}: {e}")
    
    print(f"Cleaned up chunk files for {file_name_no_ext}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python merge_chunks.py <file_name_no_ext>")
    else:
        merge_chunks(sys.argv[1])
