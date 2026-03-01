import sqlite3
import pandas as pd

from settings import Settings
from utils import append_to_readme


def get_sk_bibliography_in_markdown(database_path: str) -> str:
    query = open("./sql/stephen_king.sql", "r").read()
    conn = sqlite3.connect(database_path)
    df = pd.read_sql(query, conn)
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
    text = get_sk_bibliography_in_markdown(Settings.DATABASE_PATH)
    append_to_readme(text_to_append=text, anchor="## Stephen King")
