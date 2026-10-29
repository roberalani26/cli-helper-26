# cli-helper-26

`cli-helper-26` is a lightweight Python utility library designed to streamline the creation of robust command-line interfaces. It abstracts complex argument parsing and provides standardized formatting for console output to help developers build professional tools faster.

## Features

*   **Decorator-based Routing:** Map CLI commands to functions effortlessly using intuitive Python decorators.
*   **Automatic Help Generation:** Dynamically generates clean, readable help documentation based on function docstrings and type hints.
*   **Built-in Color Support:** Integrated logging utilities that provide semantic, ANSI-colored output for info, warning, and error states.
*   **Zero-Dependency Core:** Built using standard library modules to ensure a minimal footprint and maximum compatibility.

## Installation

Install the package directly via pip:

```bash
pip install cli-helper-26
```

If you are working within a virtual environment, ensure it is activated before running the command.

## Usage

Define your CLI tools by decorating your entry functions. The helper will automatically handle command execution and argument mapping.

```python
from cli_helper import CLI

app = CLI()

@app.command()
def greet(name: str, shout: bool = False):
    """Greets the user by name."""
    msg = f"Hello, {name}!"
    print(msg.upper() if shout else msg)

if __name__ == "__main__":
    app.run()
```

Run your script from the terminal:

```bash
python main.py greet --name "Developer" --shout
# Output: HELLO, DEVELOPER!
```

## License

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.