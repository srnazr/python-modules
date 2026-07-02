import sys
import typing

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 ft_ancient_text.py <filename>")
        return
    
    filename = sys.argv[1]

    print("=== Cyber Archives Recovery ===")
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
        print(f"File '{filename}' closed")

if __name__ == "__main__":
    main()