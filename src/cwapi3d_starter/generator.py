import os
import subprocess
import sys
from pathlib import Path
from string import Template
import importlib.resources
from rich.console import Console
from rich.panel import Panel

console = Console()

class ProjectGenerator:
    def __init__(self, project_name: str, target_dir: Path):
        self.project_name = project_name
        self.target_dir = target_dir
        self.package_name = project_name.lower().replace("-", "_").replace(" ", "_")
        self.files = importlib.resources.files("cwapi3d_starter").joinpath("templates")
    
    def display_success(self):
        console.print(Panel.fit(
            f"[bold green]Successfully created {self.project_name}![/bold green]\n\n"
            f"cd {self.project_name}\n"
            f"uv sync\n"
            f"code .",
            title="Next Steps"
        ))

    def generate(self):
        console.print(f"[bold green]Creating project: {self.project_name}[/bold green]")
        
        self.create_directories()
        self.create_files()
        
        self.init_git()
        self.setup_environment()
        
        self.display_success()

    def create_directories(self):
        console.print("Creating directories...")
        dirs = [
            self.target_dir,
            self.target_dir / "src" / self.package_name,
            self.target_dir / "src" / self.package_name / "cad",
            self.target_dir / ".vscode",
            self.target_dir / "tests",
            self.target_dir / "docs",
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)

    def _read_template(self, *parts: str) -> str:
        """Reads a template file relative to the templates directory."""
        template_file = self.files
        for part in parts:
            template_file = template_file.joinpath(part)
        
        if hasattr(template_file, "is_file") and not template_file.is_file():
             raise FileNotFoundError(f"Template {'/'.join(parts)} not found.")
        
        return template_file.read_text(encoding="utf-8")

    def _write_file(self, path: Path, content: str):
        console.print(f"Writing {path.relative_to(self.target_dir)}...")
        path.write_text(content, encoding="utf-8")

    def create_files(self):
        context = {
            "project_name": self.project_name,
            "package_name": self.package_name,
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}"
        }

        self._write_file(
            self.target_dir / "pyproject.toml",
            Template(self._read_template("pyproject.toml")).substitute(context)
        )
        
        self._write_file(
            self.target_dir / "README.md",
            Template(self._read_template("README.md")).substitute(context)
        )
        
        self._write_file(
            self.target_dir / ".gitignore",
            self._read_template(".gitignore")
        )
        
        self._write_file(
            self.target_dir / f"{self.project_name}.py",
            Template(self._read_template("entry_point_py.template")).substitute(context)
        )

        (self.target_dir / "src" / self.package_name / "__init__.py").touch()
        
        self._write_file(
            self.target_dir / "src" / self.package_name / "main.py",
            Template(self._read_template("main_py.template")).substitute(context)
        )
        
        self._write_file(
            self.target_dir / "src" / self.package_name / "cad" / "example_geometry.py",
            self._read_template("example_geometry.py")
        )

        self._write_file(
            self.target_dir / ".vscode" / "settings.json",
            self._read_template("vscode", "settings.json")
        )
        
        # self._write_file(
        #     self.target_dir / ".vscode" / "launch.json",
        #     self._read_template("vscode", "launch.json")
        # )

        self._write_file(
            self.target_dir / "tests" / "test_placeholder.py",
            self._read_template("test_placeholder.py")
        )
        
        (self.target_dir / "docs" / "README.md").touch()

    def init_git(self):
        console.print("Initializing git repository...")
        try:
            subprocess.run(["git", "init"], cwd=self.target_dir, check=False) 
        except FileNotFoundError:
             console.print("[yellow]Warning: git command not found. Skipping git init.[/yellow]")
        except Exception as e:
             console.print(f"[yellow]Warning: git init failed: {e}[/yellow]")

    def setup_environment(self):
        try:
             subprocess.run(["uv", "--version"], capture_output=True, check=True)
        except Exception:
             console.print("[yellow]Warning: 'uv' not found. Skipping environment setup.[/yellow]")
             return

        console.print("Creating virtual environment...")
        try:
            subprocess.run(["uv", "venv"], cwd=self.target_dir, check=True)
            console.print("Installing dependencies...")
            subprocess.run(["uv", "sync"], cwd=self.target_dir, check=True)
        except Exception as e:
            console.print(f"[yellow]Warning: environment setup failed: {e}[/yellow]")
