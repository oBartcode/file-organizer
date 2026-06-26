import shutil
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

CATEGORIES = {
    "Imagens": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"],
    "Documentos": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm"],
    "Musica": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma"],
    "Codigo": [".py", ".js", ".ts", ".html", ".css", ".java", ".cpp", ".c", ".go", ".rs"],
    "Compactados": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Executaveis": [".exe", ".msi", ".bat", ".sh"],
    "Fontes": [".ttf", ".otf", ".woff", ".woff2"],
}

UNDO_FILE = Path(".undo.json")

def get_category(extension: str) -> str:
    for category, extensions in CATEGORIES.items():
        if extension.lower() in extensions:
            return category
    return "Outros"

def organize(path: str, dry_run: bool = False) -> dict:
    root = Path(path)
    moved = {}
    undo_log = []

    files = [f for f in root.iterdir() if f.is_file() and f.name != ".undo.json"]

    for file in files:
        category = get_category(file.suffix)
        dest_folder = root / category
        dest_file = dest_folder / file.name

        moved.setdefault(category, []).append(file.name)

        if not dry_run:
            dest_folder.mkdir(exist_ok=True)
            shutil.move(str(file), str(dest_file))
            undo_log.append({"from": str(dest_file), "to": str(file)})

    if not dry_run and undo_log:
        UNDO_FILE.write_text(json.dumps(undo_log, indent=2), encoding="utf-8")

    return moved

def undo_organize(path: str):
    undo_path = Path(path) / ".undo.json"
    if not undo_path.exists():
        console.print("[red]Nenhuma organização encontrada para desfazer![/]")
        return

    log = json.loads(undo_path.read_text(encoding="utf-8"))
    for entry in log:
        src = Path(entry["from"])
        dst = Path(entry["to"])
        if src.exists():
            shutil.move(str(src), str(dst))

    undo_path.unlink()
    console.print("[green]✅ Organização desfeita com sucesso![/]")

def show_report(moved: dict):
    if not moved:
        console.print("[yellow]Nenhum arquivo encontrado para organizar.[/]")
        return

    table = Table(title="📁 Relatório de Organização", border_style="bright_blue")
    table.add_column("Categoria", style="cyan")
    table.add_column("Arquivos", style="white")
    table.add_column("Total", style="yellow", justify="right")

    total = 0
    for category, files in sorted(moved.items()):
        table.add_row(category, "\n".join(files), str(len(files)))
        total += len(files)

    console.print(table)
    console.print(f"\n[bold green]✅ Total: {total} arquivo(s) organizados![/]\n")