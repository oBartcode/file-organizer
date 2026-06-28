🗂️ file-organizer
A CLI tool that automatically organizes files in a folder by type and extension.
✨ Features

📁 Organizes files into categories (Images, Documents, Videos, Music, Code, etc.)
🔍 Dry-run mode to preview without moving files
↩️ Undo the last organization
📊 Detailed report of organized files

🚀 Installation
```bash

git clone https://github.com/oBartcode/file-organizer.git

cd file-organizer

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

```
📖 Usage
```bash
Organize current folder
python main.py run .
Organize specific folder
python main.py run C:\Users\你\Downloads
Preview without moving files
python main.py run . --dry-run
Undo last organization
python main.py undo .

```
🛠️ Tech Stack

Python
Typer
Rich

📝 License
MIT License