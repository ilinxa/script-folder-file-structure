import os
import json
import mimetypes
import fnmatch

# Map common extensions to programming languages
EXTENSION_TO_LANGUAGE = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".java": "java",
    ".c": "c",
    ".cpp": "cpp",
    ".cs": "csharp",
    ".rb": "ruby",
    ".go": "go",
    ".php": "php",
    ".html": "html",
    ".css": "css",
    ".sql": "sql",
    ".sh": "bash",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".md": "markdown",
    ".txt": "text"
}

def get_file_language(filename):
    _, ext = os.path.splitext(filename)
    return EXTENSION_TO_LANGUAGE.get(ext.lower(), "text")

def is_text_file(filepath):
    """Check if file is likely text-based."""
    mime, _ = mimetypes.guess_type(filepath)
    if mime and mime.startswith("text/"):
        return True
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            f.read(1024)
        return True
    except Exception:
        return False

def read_ignore_patterns(root_path):
    """Read .folderignore file and return list of patterns."""
    ignore_file = os.path.join(root_path, ".folderignore")
    patterns = []

    if os.path.isfile(ignore_file):
        with open(ignore_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.append(line)

    return patterns

def is_ignored(name, path, patterns):
    """Check if name or path matches any ignore pattern."""
    for pattern in patterns:
        # Match both name and full path
        if fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(path, pattern):
            return True
    return False

def get_folder_structure(root_path, max_depth=3, current_depth=0, check_file=False,
                         max_file_size=1_000_000, ignore_patterns=None):
    """
    Recursively builds a folder structure in a nested dictionary format,
    including file contents as code blocks with language metadata.
    """
    if ignore_patterns is None:
        ignore_patterns = []

    if current_depth >= max_depth:
        return {}

    structure = {}
    try:
        with os.scandir(root_path) as entries:
            for entry in entries:
                name = entry.name
                path = entry.path

                # Skip if ignored
                if is_ignored(name, path, ignore_patterns):
                    continue

                if entry.is_dir():
                    subdir_structure = get_folder_structure(
                        path, max_depth, current_depth + 1, check_file, max_file_size, ignore_patterns
                    )
                    if "__error__" not in subdir_structure:
                        structure[name] = subdir_structure
                elif entry.is_file():
                    file_info = {
                        "type": "file",
                        "name": name,
                        "language": get_file_language(name),
                    }

                    if check_file:
                        if not is_text_file(path):
                            file_info["content"] = "<<BINARY OR NON-TEXT FILE>>"
                        else:
                            try:
                                file_size = os.path.getsize(path)
                                if file_size > max_file_size:
                                    file_info["content"] = f"<<SKIPPED: File too large ({file_size} bytes)>>"
                                else:
                                    with open(path, "r", encoding="utf-8") as f:
                                        file_info["content"] = f.read()
                            except Exception as e:
                                file_info["content"] = f"<<ERROR: {str(e)}>>"

                    structure[name] = file_info

    except PermissionError:
        structure['__error__'] = 'Permission Denied'

    return structure


def generate_folder_json(root_path: str, max_depth: int = 3, check_file: bool = False) -> str:
    ignore_patterns = read_ignore_patterns(root_path)
    structure = get_folder_structure(root_path, max_depth, check_file=check_file, ignore_patterns=ignore_patterns)
    return json.dumps(structure, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate JSON file structure from a folder")
    parser.add_argument("root", type=str, help="Root folder path")
    parser.add_argument("--depth", type=int, default=3, help="Maximum nested depth to scan")
    parser.add_argument("--checkfile", action="store_true", help="Include file contents in output")
    parser.add_argument("--maxfilesize", type=int, default=1_000_000,
                        help="Max file size to read in bytes (default: 1MB)")

    args = parser.parse_args()

    result_json = generate_folder_json(args.root, args.depth, check_file=args.checkfile)

    # 📦 Determine output filename from folder name
    folder_name = os.path.basename(os.path.normpath(args.root))
    output_filename = f"{folder_name}.json"

    # 📁 Save into outputs/
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "outputs")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, output_filename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result_json)

    print(f"✅ Folder structure saved to: {output_path}")
# usage: python folder_check.py "D:\hessam 2 1 2025\MyProjects\modular-ofc\ofc-md1-2-full-authlogic-with-application(5-23-2025)\md1-2-full-auth-logic" --depth 2 --checkfile
# useage: 