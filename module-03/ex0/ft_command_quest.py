import sys

print("=== Command Quest ===")
print(f"Program name: {sys.argv[0]}")

if len(sys.argv) == 1:
    print("No arguments provided!")
else:
    print(f"Arguments received: {len(sys.argv) - 1}")
    for i, arg in enumerate(sys.argv[1:], 1):
        print(f"Argument {i}: {arg}")

print(f"Total arguments: {len(sys.argv)}")