import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from .generator import ProjectGenerator

app = typer.Typer(help="cwapi3d Project Scaffolding CLI")
console = Console()

@app.command()
def init(
    project_name: str = typer.Argument(..., help="Name of the project to create"),
    directory: Optional[Path] = typer.Option(
        None, "--directory", "-d", help="Target directory (defaults to project name)"
    ),
):
    """
    Initialize a new cwapi3d project.
    """
    if directory is None:
        target_dir = Path.cwd() / project_name
    else:
        target_dir = directory

    if target_dir.exists() and any(target_dir.iterdir()):
        console.print(f"[bold red]Error:[/] Directory '{target_dir}' is not empty.")
        raise typer.Exit(code=1)

    generator = ProjectGenerator(project_name, target_dir)
    generator.generate()

def main():
    app()

if __name__ == "__main__":
    main()
