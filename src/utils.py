from pathlib import Path


def append_to_readme(text_to_append: str, anchor: str) -> None:
    file_path = Path("README.md")
    anchor = "## To-Read Next"

    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines(keepends=True)

    for i, line in enumerate(lines):
        if line.strip().startswith(anchor):
            new_lines = lines[:i + 1]
            new_lines.append("\n")
            new_lines.append(text_to_append + "\n")
            file_path.write_text("".join(new_lines), encoding="utf-8")
            return

    raise ValueError(f"Anchor '{anchor}' not found.")
