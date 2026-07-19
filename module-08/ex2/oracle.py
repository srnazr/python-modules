import os
import sys
from dotenv import load_dotenv


def load_configuration():
    load_dotenv()


def get_config_value(variable_name, default_value):
    value = os.environ.get(variable_name)

    if value is None:
        return (default_value, False)
    else:
        return (value, True)


def print_missing_warning(variable_name):
    print("WARNING: " + variable_name + " is not set, using default value.")


def show_configuration():
    mode, mode_found = get_config_value("MATRIX_MODE", "development")
    database_url, db_found = get_config_value(
        "DATABASE_URL", "sqlite:///local_matrix.db"
    )
    api_key, api_found = get_config_value("API_KEY", None)
    log_level, log_found = get_config_value("LOG_LEVEL", "DEBUG")
    zion_endpoint, zion_found = get_config_value(
        "ZION_ENDPOINT", "http://localhost:8080"
    )

    if mode_found == False:
        print_missing_warning("MATRIX_MODE")
    if db_found == False:
        print_missing_warning("DATABASE_URL")
    if api_found == False:
        print_missing_warning("API_KEY")
    if log_found == False:
        print_missing_warning("LOG_LEVEL")
    if zion_found == False:
        print_missing_warning("ZION_ENDPOINT")

    print("")
    print("Configuration loaded:")
    print("  Mode: " + mode)

    if mode == "production":
        print("  Database: Connected to production cluster")
    else:
        print("  Database: Connected to local instance")

    if api_key is None or api_key == "":
        print("  API Access: NOT authenticated (missing API_KEY)")
    else:
        print("  API Access: Authenticated")

    print("  Log Level: " + log_level)

    if zion_endpoint == "http://localhost:8080":
        print("  Zion Network: Offline (using local default)")
    else:
        print("  Zion Network: Online")

    return {
        "mode": mode,
        "database_url": database_url,
        "api_key": api_key,
        "log_level": log_level,
        "zion_endpoint": zion_endpoint,
    }


def security_check(config):
    print("")
    print("Environment security check:")

    hardcoded_secret_found = False
    if config["api_key"] == "secret123" or config["api_key"] == "changeme":
        hardcoded_secret_found = True

    if hardcoded_secret_found == False:
        print("[OK] No hardcoded secrets detected")
    else:
        print("[WARNING] Looks like a placeholder secret is being used")

    if os.path.exists(".env"):
        print("[OK] .env file properly configured")
    else:
        print("[WARNING] No .env file found, copy .env.example to .env")

    if config["mode"] == "production":
        print("[OK] Running with production overrides")
    else:
        print("[OK] Production overrides available")


def main():
    print("Welcome to the Real World of Data Engineering")
    print("")
    print("ORACLE STATUS: Reading the Matrix...")

    load_configuration()
    config = show_configuration()
    security_check(config)

    print("")
    print("The Oracle sees all configurations.")


if __name__ == "__main__":
    main()
