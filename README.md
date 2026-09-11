# cli-helper-26

`cli-helper-26` is a lightweight Python utility library designed to streamline the creation of robust command-line interfaces. It abstracts boilerplate logic for argument parsing, configuration management, and colorized output to help developers build professional CLI tools in minutes.

### Key Features
* **Intuitive Decorators:** Wrap your functions with `@command` to automatically map arguments and generate help documentation.
* **Smart Config Management:** Built-in support for loading and saving `.json` or `.yaml` configuration files with validation.
* **Context Handling:** Integrated session context to share database connections or API clients across subcommands seamlessly.
* **Formatted Output:** Pre-configured logging helpers for success, warning, and error states using standardized ANSI color codes.

### Installation

Ensure you have Python 3.8+ installed. Install the package directly from PyPI:

```bash
pip install cli-helper-26
```

### Basic Usage

Define your CLI tool in a `main.py` file:

```python
from cli_helper import CLI

app = CLI(name="my-tool")

@app.command()
def greet(name: str, verbose: bool = False):
    """Greets the user."""
    if verbose:
        print(f"DEBUG: Initializing greeting sequence for {name}")
    print(f"Hello, {name}!")

if __name__ == "__main__":
    app.run()
```

Run your new tool from the terminal:

```bash
python main.py greet --name Alice --verbose
```

### License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is licensed under the MIT License. See the `LICENSE` file for details.