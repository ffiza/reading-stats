import sqlite3
import pandas as pd
from reading_stats.config import CONFIG


def get_next_reads_in_markdown(database_path: str) -> str:
    query = open(CONFIG["NextReads"]["QueryPath"], "r").read()
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
    text = text.replace("nan", "   ")
    return text


if __name__ == "__main__":
    text = get_next_reads_in_markdown(CONFIG["Database"]["FilePath"])
    with open(CONFIG["NextReads"]["OutputFile"], "w", encoding="utf-8") as f:
        f.write(text)
        f.close()
