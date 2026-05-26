import sys
import os
import csv

def split_tsv(file_path, chunk_size=200):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return

    base_name = os.path.basename(file_path)
    file_name_no_ext = os.path.splitext(base_name)[0]
    output_dir = "chunks"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(file_path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f, delimiter='\t')
        try:
            header = next(reader)
            sub_header = next(reader)
        except StopIteration:
            print(f"Error: File {file_path} is empty or malformed.")
            return

        chunk = []
        chunk_idx = 1
        
        for row in reader:
            chunk.append(row)
            if len(chunk) >= chunk_size:
                write_chunk(output_dir, file_name_no_ext, chunk_idx, header, sub_header, chunk)
                chunk = []
                chunk_idx += 1
        
        if chunk or chunk_idx == 1:
            write_chunk(output_dir, file_name_no_ext, chunk_idx, header, sub_header, chunk)

    print(f"Split {file_path} into chunks in {output_dir}")

def write_chunk(output_dir, file_name, idx, header, sub_header, data):
    # Format: filename_chunk_x.tsv
    chunk_file = os.path.join(output_dir, f"{file_name}_chunk_{idx}.tsv")
    with open(chunk_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(header)
        writer.writerow(sub_header)
        writer.writerows(data)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python split_tsv.py <path_to_tsv>")
    else:
        split_tsv(sys.argv[1])
