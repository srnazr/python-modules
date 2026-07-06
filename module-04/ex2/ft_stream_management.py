import sys
import typing

def main():
    if len(sys.argv) != 2:
        print("Usage: ft_stream_management.py <filename>")
        return

    filename = sys.argv[1]

    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file '{filename}'")

    try:
        file: typing.IO = open(filename, "r")
    except Exception as e:
        print(f"[STDERR] Error opening file '{filename}': {e}", file=sys.stderr)
        return

    try:
        content = file.read()
        print("---")
        print(content)
        print("---")
    finally:
        file.close()
        print(f"File '{filename}' closed.")

    print("Transform data:")
    lines = content.splitlines()
    new_content = ""
    for line in lines:
        new_content += line + "#\n"

    print("---")
    print(new_content, end="")
    print("---")

    sys.stdout.write("Enter new file name (or empty): ")
    sys.stdout.flush()
    new_filename = sys.stdin.readline().rstrip("\n")

    if new_filename == "":
        print("Not saving data.")
        return

    print(f"Saving data to '{new_filename}'")

    try:
        out_file: typing.IO = open(new_filename, "w")
    except Exception as e:
        print(f"[STDERR] Error opening file '{new_filename}': {e}", file=sys.stderr)
        return

    try:
        out_file.write(new_content)
    finally:
        out_file.close()

    print(f"Data saved in file '{new_filename}'.")

if __name__ == "__main__":
    main()