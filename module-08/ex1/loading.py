import sys
import importlib.util
import importlib.metadata


def check_one_package(package_name):
    spec = importlib.util.find_spec(package_name)

    if spec is None:
        return (False, None)
    else:
        try:
            version = importlib.metadata.version(package_name)
        except importlib.metadata.PackageNotFoundError:
            version = "unknown"
        return (True, version)


def check_dependencies():
    packages_to_check = ["pandas", "numpy", "requests", "matplotlib"]

    descriptions = {
        "pandas": "Data manipulation ready",
        "numpy": "Numerical computation ready",
        "requests": "Network access ready",
        "matplotlib": "Visualization ready",
    }

    results = {}

    for package_name in packages_to_check:
        is_available, version = check_one_package(package_name)
        results[package_name] = is_available

        if is_available:
            status_line = "[OK] " + package_name
            status_line = status_line + " (" + version + ")"
            status_line = status_line + "- " + descriptions[package_name]
            print(status_line)
        else:
            status_line = "[MISSING] " + package_name
            status_line = status_line + " - " + descriptions[package_name]
            status_line = status_line + " NOT ready"
            print(status_line)

    return results


def print_missing_instructions():
    print("")
    print("ERROR: Some required packages are missing!")
    print("This program needs pandas, numpy and matplotlib to run.")
    print("")
    print("Option 1: Install with pip")
    print("  pip install -r requirements.txt")
    print("")
    print("Option 2: Install with Poetry")
    print("  poetry install")
    print("  poetry run python loading.py")
    print("")


def generate_matrix_data():
    import numpy as np

    np.random.seed(42)
    data_points = np.random.normal(loc=50, scale=15, size=1000)
    return data_points


def analyze_data(data_points):
    import pandas as pd

    data_frame = pd.DataFrame(data_points, columns=["value"])

    mean_value = data_frame["value"].mean()
    min_value = data_frame["value"].min()
    max_value = data_frame["value"].max()

    print("Data summary:")
    print("  mean  = " + str(round(mean_value, 2)))
    print("  min   = " + str(round(min_value, 2)))
    print("  max   = " + str(round(max_value, 2)))

    return data_frame


def create_visualization(data_frame):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.figure()
    plt.hist(data_frame["value"], bins=30, color="green")
    plt.title("Matrix Data Analysis")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.savefig("matrix_analysis.png")
    plt.close()


def compare_pip_poetry():
    print("pip vs Poetry:")
    print("  pip  -> reads requirements.txt, installs packages one")
    print("          by one, does not lock sub-dependencies unless")
    print("          you freeze them yourself with pip freeze.")
    print("  Poetry -> reads pyproject.toml, resolves the whole")
    print("            dependency tree, and writes a poetry.lock")
    print("            file so every install is reproducible.")


def main():
    print("Welcome to the Real World of Data Engineering")
    print("")
    print("LOADING STATUS: Loading programs...")
    print("Checking dependencies:")

    results = check_dependencies()

    core_ready = True
    if not results["pandas"]:
        core_ready = False
    if not results["numpy"]:
        core_ready = False
    if not results["matplotlib"]:
        core_ready = False

    if not core_ready:
        print_missing_instructions()
        sys.exit(1)

    print("")
    print("Analyzing Matrix data...")
    print("Processing 1000 data points...")

    data_points = generate_matrix_data()
    data_frame = analyze_data(data_points)

    print("Generating visualization...")
    create_visualization(data_frame)

    print("Analysis complete!")
    print("Results saved to: matrix_analysis.png")
    print("")

    compare_pip_poetry()


if __name__ == "__main__":
    main()
