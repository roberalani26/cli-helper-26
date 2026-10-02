[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# cli-helper-26

`cli-helper-26` is a lightweight Python library designed to streamline the creation of interactive command-line tools. It automates argument parsing, provides rich terminal formatting, and manages persistent user configurations with zero boilerplate.

## Features

- **Declarative Command Routing:** Define CLI options and subcommands directly using Python type hints and decorators.
- **Rich Terminal Formatting:** Built-in support for ANSI colors, progress bars, spin indicators, and structured table outputs.
- **Session State Management:** Read and write JSON or YAML configuration files automatically across execution cycles.
- **Interactive Prompts:** Collect user input with built-in validation, secure password masking, and fuzzy-search selection menus.

## Installation

Install the package directly from PyPI using `pip`:

```bash
pip install cli-helper-26
```

Or install the latest development version via Git:

```bash
pip install git+https://github.com/Developer/cli-helper-26.git
```

## Quick Start

Create a script named `app.py`:

```python
from cli_helper_26 import CLIApp, command, prompt

app = CLIApp(name="task-runner")

@command(help="Initialize a new project environment")
def init(env_name: str, verbose: bool = False):
    if verbose:
        app.log.info(f"Setting up environment: {env_name}")
    
    role = prompt.select("Select primary role:", ["developer", "tester", "admin"])
    app.print(f"Successfully initialized {env_name} for {role}!", style="green")

if __name__ == "__main__":
    app.run()
```

Run the command in your terminal:

```bash
python app.py init my-project --verbose
```

## License

Distributed under the MIT License. See `LICENSE` for details.