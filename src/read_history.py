import sqlite3
import pandas as pd

from settings import Settings


def export_read_history(database_path: str) -> None:
    query = open("./sql/read_history.sql", "r").read()
    conn = sqlite3.connect(database_path)
    df = pd.read_sql(query, conn)
    conn.close()
    df.to_csv("data/processed/read_history.csv", index=False)


def export_recent_reads(amount_to_export: int = 20) -> None:
    df = pd.read_csv("data/processed/read_history.csv")
    recent_reads = df.sort_values(
        "FinishDate", ascending=False).head(amount_to_export)
    recent_reads.to_csv("data/results/recent_reads.csv", index=False)


if __name__ == "__main__":
    export_read_history(Settings.DATABASE_PATH)
    export_recent_reads()
