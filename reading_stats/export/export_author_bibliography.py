import sqlite3
import argparse
import pandas as pd
from reading_stats.config import CONFIG


def export_author_bibliography(database_path: str, author_name: str) -> str:
    query = open(CONFIG["AuthorBibliography"]["QueryPath"], "r").read()

    conn = sqlite3.connect(database_path)
    df = pd.read_sql_query(
        query,
        conn,
        params=(author_name,)
        )
    conn.close()
    df = df.drop(columns=["AuthorName", "AuthorID", "WorkID",
                          "StartDate", "Genre"])
    df = df.rename(columns={
        "WorkName": "Title",
        "WorkType": "Type",
        "NumberInSeries": "Order",
        "ReadScore": "MyScore",
        "FinishDate": "LastReadOn"})
    df = df.sort_values(by="PublishedOn", ascending=True)
    text = df.to_markdown(index=False, buf=None)
    text = text.replace("nan", "   ")
    return text


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--author", help="Author name.")
    args = parser.parse_args()

    text = export_author_bibliography(
        CONFIG["Database"]["FilePath"],
        args.author)
    filename = args.author.replace(".", "").replace(" ", "_").lower() \
        + ".md"
    with open(CONFIG["AuthorBibliography"]["DataOutputFilePrefix"] + filename,
              "w", encoding="utf-8") as f:
        f.write(text)
        f.close()
