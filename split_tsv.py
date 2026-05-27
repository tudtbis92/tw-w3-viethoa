import sys
import os

def split_tsv(file_path, chunk_size=200):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return

    base_name = os.path.basename(file_path)
    file_name_no_ext = os.path.splitext(base_name)[0]
    output_dir = "chunks"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    if len(lines) < 2:
        print(f"Error: File {file_path} is too short.")
        return

    header = lines[0]
    sub_header = lines[1]
    data_lines = lines[2:]

    chunk_idx = 1
    for i in range(0, len(data_lines), chunk_size):
        chunk = data_lines[i:i + chunk_size]
        write_chunk(output_dir, file_name_no_ext, chunk_idx, header, sub_header, chunk)
        chunk_idx += 1

    print(f"Split {file_path} into {chunk_idx - 1} chunks in {output_dir}")

def write_chunk(output_dir, file_name, idx, header, sub_header, data):
    chunk_file = os.path.join(output_dir, f"{file_name}_chunk_{idx}.tsv")
    with open(chunk_file, 'w', encoding='utf-8') as f:
        f.write(header)
        f.write(sub_header)
        for line in data:
            f.write(line)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python split_tsv.py <path_to_tsv>")
    else:
        split_tsv(sys.argv[1])
