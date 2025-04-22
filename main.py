#!/usr/bin/env python3

import argparse
import logging
import os
import subprocess
import sys
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def setup_argparse():
    """
    Sets up the argument parser for the command-line interface.

    Returns:
        argparse.ArgumentParser: The argument parser object.
    """
    parser = argparse.ArgumentParser(description="misconfig-ConfigLinter: Identifies stylistic or best-practice violations in configuration files.")
    parser.add_argument("config_file", help="Path to the configuration file to lint.")
    parser.add_argument("-t", "--filetype", choices=['yaml', 'json'], help="Specify the file type (yaml or json).  If not specified, will attempt to determine from the file extension.", default=None)
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output (debug logging).")
    parser.add_argument("-q", "--quiet", action="storetrue", help="Suppress all output except for errors.")

    return parser


def lint_yaml(config_file):
    """
    Lints a YAML configuration file using yamllint.

    Args:
        config_file (str): Path to the YAML configuration file.

    Returns:
        int: 0 if no errors, non-zero otherwise.
    """
    try:
        result = subprocess.run(["yamllint", config_file], capture_output=True, text=True, check=False)

        if result.returncode == 0:
            logging.info(f"YAML linting successful for {config_file}.")
            if result.stdout:
                print(result.stdout)  # Still print output if any warnings or info messages are present.
            return 0
        else:
            logging.error(f"YAML linting failed for {config_file}.")
            print(result.stderr)
            return result.returncode

    except FileNotFoundError:
        logging.error("yamllint is not installed. Please install it.")
        return 1
    except Exception as e:
        logging.exception(f"An unexpected error occurred during YAML linting: {e}")
        return 1


def lint_json(config_file):
    """
    Lints a JSON configuration file using json.tool.

    Args:
        config_file (str): Path to the JSON configuration file.

    Returns:
        int: 0 if no errors, non-zero otherwise.
    """
    try:
        with open(config_file, 'r') as f:
            try:
                json.load(f)  # Check for valid JSON syntax.
            except json.JSONDecodeError as e:
                logging.error(f"JSON decoding error in {config_file}: {e}")
                print(f"JSON decoding error in {config_file}: {e}")
                return 1

        # If JSON is valid, run the json.tool to check formatting.
        result = subprocess.run(["python", "-m", "json.tool", config_file], capture_output=True, text=True, check=False)

        if result.returncode == 0:
            logging.info(f"JSON linting successful for {config_file}.")
            #if result.stdout:
            #    print(result.stdout) # Suppress stdout for clean JSON format
            return 0
        else:
            logging.error(f"JSON formatting check failed for {config_file}.")
            print(result.stderr)
            return result.returncode

    except FileNotFoundError:
        logging.error(f"Config file not found: {config_file}")
        return 1
    except Exception as e:
        logging.exception(f"An unexpected error occurred during JSON linting: {e}")
        return 1


def determine_filetype(config_file):
    """
    Determines the file type based on the file extension.

    Args:
        config_file (str): Path to the configuration file.

    Returns:
        str: 'yaml' or 'json' if the file type can be determined, None otherwise.
    """
    _, ext = os.path.splitext(config_file)
    ext = ext.lstrip('.').lower()

    if ext in ['yaml', 'yml']:
        return 'yaml'
    elif ext == 'json':
        return 'json'
    else:
        return None


def main():
    """
    Main function to execute the configuration file linter.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Verbose mode enabled.")
    if args.quiet:
        logging.getLogger().setLevel(logging.ERROR)
        logging.debug("Quiet mode enabled.")

    config_file = args.config_file

    # Input Validation: Check if the file exists
    if not os.path.exists(config_file):
        logging.error(f"File not found: {config_file}")
        print(f"Error: File not found: {config_file}")  # Always print error to console
        sys.exit(1)
    if not os.path.isfile(config_file):
        logging.error(f"Not a file: {config_file}")
        print(f"Error: Not a file: {config_file}")
        sys.exit(1)

    # Determine file type
    filetype = args.filetype
    if not filetype:
        filetype = determine_filetype(config_file)
        if not filetype:
            logging.error("Could not determine file type. Please specify using --filetype.")
            print("Error: Could not determine file type. Please specify using --filetype (yaml or json).")
            sys.exit(1)
    logging.debug(f"Detected filetype: {filetype}")

    # Lint the file
    if filetype == 'yaml':
        result = lint_yaml(config_file)
    elif filetype == 'json':
        result = lint_json(config_file)
    else:
        logging.error(f"Unsupported file type: {filetype}")
        print(f"Error: Unsupported file type: {filetype}")
        sys.exit(1)

    sys.exit(result)


if __name__ == "__main__":
    main()


# Usage Examples:
#
# 1. Lint a YAML file:
#    python main.py config.yaml
#
# 2. Lint a JSON file:
#    python main.py config.json
#
# 3. Specify the file type explicitly:
#    python main.py config.txt -t yaml
#
# 4. Enable verbose mode:
#    python main.py config.yaml -v
#
# 5. Suppress all output except for errors:
#    python main.py config.yaml -q