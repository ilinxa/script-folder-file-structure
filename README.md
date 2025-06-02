# 📁 Folder Structure Scanner

A Python script that scans a folder recursively and generates a structured JSON representation of its contents — including file names, folder structure, and optionally file contents with syntax metadata.

Great for documenting programming projects!

---

## ✅ Features

- Recursively scans folders up to a specified depth
- Optionally includes **file contents** (e.g., source code)
- Supports `.folderignore` to skip unwanted files/folders (like `.gitignore`)
- Detects file types and programming languages based on extension
- Skips large or binary files safely
- Outputs a clean, structured JSON file

---

## 🧰 Requirements

- Python 3.6+
- No external dependencies

---

## 🚀 Usage

```bash
python folder_check.py <folder-path> [OPTIONS]

```
Example:
```bash
python folder_check.py "./my-project" --depth 3 --checkfile
```

## Options
1. `--depth N` => Maximum folder depth to scan (default: 3)
2. `--checkfile` => Include file contents in output
3. `--maxfilesize N` => Max file size to read (in bytes, default: 1MB)

## file or folder ignore:
Create a .folderignore file at the root of your project to exclude files and folders:
```
__pycache__
node_modules
venv
.env
*.log
.*
**/build
```
Lines starting with # are treated as comments.

Ignored items will not appear in the output JSON.

## 📄 Output
The script saves the result in a JSON file inside the outputs/ directory, named after the scanned folder:
```
outputs/my-project.json
```
### Example output snippet:
```json
"app.py": {
  "type": "file",
  "name": "app.py",
  "language": "python",
  "content": "from flask import Flask\napp = Flask(__name__)\n..."
}
```
## 💡 Tips
- Use this to generate documentation snapshots of your codebase
- Integrate into CI/CD or versioning workflows
- Combine with Markdown generators for beautiful project summaries

## 🛠️ License
MIT – Feel free to modify and reuse!
