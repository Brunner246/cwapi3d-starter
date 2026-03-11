# cwapi3d-starter

Project scaffolding CLI for cwapi3d users.

## Prerequisites

- [uv](https://github.com/astral-sh/uv) installed.
- Python 3.12+

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Brunner246/cwapi3d-starter.git
   cd cwapi3d-starter
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

## Usage

To generate a new project using the CLI from the source:

```bash
uv run cwapi3d-starter <project_name> --directory <target_directory>
```
Or simply:
```bash
uv run cwapi3d-starter <project_name> # Directory defaults to <project_name> in current folder
```

### Example

```bash
# Generate a project named "my_script" in the specified directory
# Note: name and directory name need to be the same name for the generated project to work correctly.
uv run cwapi3d-starter my_script --directory "D:\cadwork\userprofil_2026\3d\API.x64\my_script"
```

This will generate a ready-to-use project structure for developing Python scripts using the `cwapi3d` Python stubs for cadwork 3d, including:
- Virtual environment setup (`uv`)
- VS Code configuration (`settings.json`)
- Sample code (`main.py`, `example_geometry.py`)
- Python package structure
