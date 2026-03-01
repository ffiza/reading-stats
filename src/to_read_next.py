import sqlite3
import pandas as pd

from settings import Settings
from utils import append_to_readme


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


if __name__ == "__main__":
    text = get_to_read_next_in_markdown(Settings.DATABASE_PATH)
    append_to_readme(text_to_append=text, anchor="## To-Read Next")
