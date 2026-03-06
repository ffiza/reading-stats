import sqlite3
import pandas as pd
from reading_stats.config import CONFIG


def export_read_history(database_path: str) -> None:
    query = open(CONFIG["ReadHistory"]["QueryPath"], "r").read()
    conn = sqlite3.connect(database_path)
    df = pd.read_sql(query, conn)
    conn.close()
    df.to_csv(CONFIG["ReadHistory"]["ReadHistoryDataFile"], index=False)


def export_recent_reads(amount_to_export: int = 20) -> None:
    df = pd.read_csv(CONFIG["ReadHistory"]["ReadHistoryDataFile"])
    recent_reads = df.sort_values(
        "FinishDate", ascending=False).head(amount_to_export)
    recent_reads.to_csv(
        CONFIG["ReadHistory"]["RecentReadsDataFile"],
        index=False)


if __name__ == "__main__":
    export_read_history(CONFIG["Database"]["FilePath"])
    export_recent_reads()
