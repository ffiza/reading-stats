import pandas as pd
from reading_stats.db import queries


def get_next_reads() -> pd.DataFrame:
    return queries.get_next_reads()


def get_next_reads_for_table() -> pd.DataFrame:
    df = queries.get_next_reads()
    return (
        df.groupby("WorkID", sort=False)
        .agg({
            "AuthorName": lambda authors: " & ".join(authors),
            "WorkName": "first",
            "WorkType": "first",
            "Series": "first",
            "NumberInSeries": "first",
            "GoodreadsScore": "first",
        })
        .reset_index(drop=True)
        .sort_values(by="AuthorName")
        .fillna("")
        .rename(
            columns={
                "AuthorName": "Author",
                "WorkName": "Title",
                "WorkType": "Type",
                "NumberInSeries": "Number in series",
            }
        )
    )
