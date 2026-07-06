import sys

print("=== Command Quest ===")
print("Program name:", sys.argv[0])
if len(sys.argv) > 1:
    print("Arguments received:", len(sys.argv) - 1)
    for i in range(1, len(sys.argv)):
        print(f"Argument {i}: {sys.argv[i]}")
else:
    print("No arguments provided!")
print("Total arguments: ", len(sys.argv))

# alternate ways to skip name:
# program_name, *args = sys.argv --> program_name = sys.argv[0], args = rest
# args = sys.argv[1:] --> args = everything except sys.argv[0]
