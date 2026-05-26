import sys

def clean_file(file_path, target_count):
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()

    new_lines = []
    for i, line in enumerate(lines):
        if i > 0 and line == lines[i-1]:
            continue
        new_lines.append(line)

    final_lines = new_lines[:target_count]

    with open(file_path, 'w', encoding='utf-8-sig', newline='') as f:
        f.writelines(final_lines)

    print(f"Cleaned file. Total lines: {len(final_lines)}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python clean_file.py <file_path> <target_count>")
        sys.exit(1)
    clean_file(sys.argv[1], int(sys.argv[2]))
