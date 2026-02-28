import sqlite3
import pandas as pd

from settings import Settings


QUERY = """
    SELECT
        A.Name                AS AuthorName,
        A.AuthorID            AS AuthorID,
        W.Name                AS WorkName,
        W.WorkType            AS WorkType,
        W.Series              AS Series,
        W.NumberInSeries      AS NumberInSeries,
        W.PublishedOn         AS PublishedOn,
        W.Genre               AS Genre,
        W.PageCount           AS PageCount,
        R.Score               AS ReadScore,
        W.GoodreadsScore      AS GoodreadsScore,
        W.WorkID              AS WorkID,
        R.StartDate           AS StartDate,
        R.FinishDate          AS FinishDate,
        R.Status              AS ReadStatus
    FROM READS R
    JOIN WORKS W
        ON R.WorkID = W.WorkID
    JOIN AUTHOR_WORK AW
        ON W.WorkID = AW.WorkID
    JOIN AUTHORS A
        ON AW.AuthorID = A.AuthorID
    WHERE R.Status NOT IN ('NEXT')
    ORDER BY A.Name, W.Name, R.StartDate;
    """


def export_read_history(database_path: str) -> None:
    conn = sqlite3.connect(database_path)
    df = pd.read_sql(QUERY, conn)
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
