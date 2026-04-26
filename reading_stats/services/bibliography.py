import pandas as pd
from reading_stats.db import queries
from reading_stats.utils.styles import Styles


def get_author_bibliography(author: str) -> pd.DataFrame:
    df = queries.get_author_bibliography(author)
    return _compute_totals(df)


def get_author_bibliography_for_table(author: str) -> pd.DataFrame:
    df = queries.get_author_bibliography(author)
    cols_to_drop = ["AuthorName", "AuthorID", "Genre", "WorkID", "StartDate"]
    df = df.drop(columns=cols_to_drop)
    df = df.fillna("")
    return (
        df.sort_values(by="PublishedOn", ascending=True)
        .rename(
            columns={
                "WorkName": "Title",
                "WorkType": "Type",
                "Series": "Series",
                "NumberInSeries": "Number in series",
                "PublishedOn": "Published on",
                "PageCount": "Page count",
                "ReadStatus": "Read status",
                "MyScore": "My score",
                "GoodreadsScore": "Goodreads score",
                "LastReadOn": "Last read on",
            }
        ))


def _compute_totals(df: pd.DataFrame) -> pd.DataFrame:
    cols_to_drop = [
        "Title", "Series", "Order", "MyScore", "GoodreadsScore", "LastReadOn",
    ]
    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])
    df["ReadStatus"] = df["ReadStatus"].fillna("NOT READ").astype("category")
    df["Type"] = df["WorkType"].astype("category")

    totals = pd.DataFrame()
    totals["TotalPagesPublished"] = df.groupby(
        "PublishedOn")["PageCount"].sum()
    totals["TotalPagesRead"] = (
        df[df["ReadStatus"] == "FINISHED"]
        .groupby("PublishedOn")["PageCount"]
        .sum()
        .fillna(0)
        .astype(int)
    )

    for work_type in Styles.WORK_TYPE_SYMBOLS:
        col = f"TotalPagesRead_{work_type.replace(' ', '')}"
        totals[col] = (
            df[(df["ReadStatus"] == "FINISHED") & (df["Type"] == work_type)]
            .groupby("PublishedOn")["PageCount"]
            .sum()
            .fillna(0)
            .astype(int)
        )

    for year in range(totals.index.min(), totals.index.max() + 1):
        if year not in totals.index:
            totals.loc[year] = 0
    return totals.sort_index()
