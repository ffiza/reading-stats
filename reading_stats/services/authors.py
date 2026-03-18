import pandas as pd
from reading_stats.db import queries


def get_author_stats() -> pd.DataFrame:
    df = queries.get_read_history()
    df = df[df["ReadStatus"].isin(["FINISHED", "NOT FINISHED"])]
    df["WeightedScore"] = df["ReadScore"] * df["PageCount"]

    avg_scores = (
        df.groupby(["AuthorID", "AuthorName"])
        .agg(WeightedReadScore=("WeightedScore", "sum"),
             TotalPages=("PageCount", "sum")))

    avg_scores["WeightedReadScore"] = (
        avg_scores["WeightedReadScore"] / avg_scores["TotalPages"])

    avg_scores = (avg_scores.reset_index().sort_values("WeightedReadScore",
                                                       ascending=False))
    return avg_scores
