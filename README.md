![Banner](banner.png)

# misconfig-ConfigLinter
Lints configuration files. YAML files are checked by delegating to the yamllint executable, which must be installed and on the PATH. JSON files are checked for valid syntax only, in process and with the running Python interpreter's json.tool module; no stylistic or formatting rules are applied to JSON. - Focused on Check for misconfigurations in configuration files or infrastructure definitions

## Install
`git clone https://github.com/ShadowStrikeHQ/misconfig-configlinter`

## Usage
`python3 main.py config.yaml` or `python3 main.py config.json [-t yaml|json] [-v] [-q]`

## Parameters
- `config_file`: Path to the configuration file to lint (positional, required).
- `-h`: Show help message and exit
- `-t`, `--filetype`: File type, yaml or json. If not given, it is taken from the file extension.
- `-v`, `--verbose`: Enable verbose output (debug logging).
- `-q`: Suppress all output except for errors.

Prerequisite: the yamllint executable must be installed for YAML files (the yamllint package in requirements.txt provides it). JSON linting needs no external executable. The exit code is the lint result: 0 when the file passes, non-zero when it fails or cannot be linted.

## License
Copyright (c) ShadowStrikeHQ
