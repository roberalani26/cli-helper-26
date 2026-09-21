# cli-helper-26

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`cli-helper-26` is a lightweight Python library designed to streamline the creation of interactive command-line interfaces. It simplifies user input validation, terminal formatting, and progress tracking so you can focus on building core application logic.

## Features

* **Strict Input Validation:** Prompt users for specific data types (emails, paths, numbers) with automatic retry logic and customizable error messages.
* **Beautiful Terminal Output:** Built-in support for ANSI colors, styled text block banners, and dynamically aligned tables.
* **Non-blocking Progress Indicators:** Simple-to-use terminal spinners and progress bars that run seamlessly during background tasks.

## Installation

Install the package directly from PyPI using pip:

```bash
pip install cli-helper-26
```

## Quick Start

Create interactive prompts and styled outputs in just a few lines of code:

```python
import time
from cli_helper_26 import prompt, Spinner, style

# Get validated input from the user
age = prompt.integer("Enter your age: ", min_value=18, max_value=99)

# Run a task with a visual progress spinner
with Spinner("Processing registration..."):
    time.sleep(1.5)

# Output styled text
print(style.success(f"Successfully registered user (Age: {age})!"))
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.