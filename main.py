import typer
from rich.console import Console
from organizer import organize, undo_organize, show_report

app = typer.Typer(help="File Organizer CLI — Organize sua pasta automaticamente 🗂️")
console = Console()

@app.command()
def run(
    path: str = typer.Argument(".", help="Caminho da pasta a organizar"),
    dry_run: bool = typer.Option(False, "--dry-run", "-d", help="Simula sem mover arquivos")
):
    """Organiza os arquivos de uma pasta por tipo."""
    if dry_run:
        console.print(f"\n[yellow]🔍 Simulando organização em:[/] {path}\n")
    else:
        console.print(f"\n[bold cyan]🗂️ Organizando pasta:[/] {path}\n")

    moved = organize(path, dry_run=dry_run)
    show_report(moved)

    if dry_run:
        console.print("[yellow]⚠️ Modo simulação — nenhum arquivo foi movido.[/]\n")

@app.command()
def undo(
    path: str = typer.Argument(".", help="Caminho da pasta a desfazer")
):
    """Desfaz a última organização."""
    console.print(f"\n[bold red]↩️ Desfazendo organização em:[/] {path}\n")
    undo_organize(path)

if __name__ == "__main__":
    app()