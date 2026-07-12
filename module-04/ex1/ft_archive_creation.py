import typing
import sys


def main():
    if len(sys.argv) != 2:
        print("Usage: ft_archive_creation.py <filename>")
        return

    filename = sys.argv[1]

    print("=== Cyber Archives Recovery & Creation ===")
    print(f"Accessing file '{filename}'")

    try:
        file: typing.IO = open(filename, "r")
    except Exception as e:
        print(f"Error opening file '{filename}': {e}")
        return

    try:
        content = file.read()
        print("---\n")
        print(content)
        print("\n---")
    finally:
        file.close()
        print(f"File '{filename}' closed.\n")

    print("Transform data:")
    lines = content.splitlines()
    new_content = ""
    for line in lines:
        new_content += line + "#\n"

    print("---\n")
    print(new_content)
    print("---")

    new_filename = input("Enter new filename (or empty): ")

    if new_filename == "":
        print("Not saving data.")
        return

    print(f"Saving data to '{new_filename}'")

    try:
        out_file: typing.IO = open(new_filename, "w")
    except Exception as e:
        print(f"Error opening file '{new_filename}': {e}")
        return

    try:
        out_file.write(new_content)
    finally:
        out_file.close()

    print(f"Data saved in file '{new_filename}'")


if __name__ == "__main__":
    main()
