import sqlite3
import pandas as pd
from pathlib import Path

from settings import Settings


def get_to_read_next_in_markdown(database_path: str) -> str:
    query = open("./sql/to_read_next.sql", "r").read()
    conn = sqlite3.connect(database_path)
    df = pd.read_sql(query, conn)
    conn.close()
    df_grouped = (
        df.groupby(
            ["WorkID", "WorkType", "Series", "NumberInSeries",
             "GoodreadsScore", "WorkName"],
            dropna=False
        )["AuthorName"]
        .agg(" & ".join)
        .reset_index()
    )
    df_grouped.drop(columns=["WorkID"], inplace=True)
    df_grouped = df_grouped[[
        "AuthorName", "WorkName", "WorkType", "Series",
        "NumberInSeries", "GoodreadsScore"]]
    df_grouped = df_grouped.sort_values("GoodreadsScore", ascending=False)
    text = df_grouped.to_markdown(index=False, buf=None)
    return text


def append_to_readme(text_to_append: str) -> None:
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




if __name__ == "__main__":
    text = get_to_read_next_in_markdown(Settings.DATABASE_PATH)
    append_to_readme(text)
