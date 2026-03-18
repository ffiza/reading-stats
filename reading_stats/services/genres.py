import pandas as pd
from reading_stats.db import queries


def get_genre_stats() -> pd.DataFrame:
    df = queries.get_read_history()
    df = df[df["ReadStatus"].isin(["FINISHED", "NOT FINISHED"])]
    df["WeightedScore"] = df["ReadScore"] * df["PageCount"]

    avg_scores = (
        df.groupby(["Genre"])
        .agg(WeightedScore=("WeightedScore", "sum"),
             TotalPages=("PageCount", "sum")))
    avg_scores["AverageScore"] = (
        avg_scores["WeightedScore"] / avg_scores["TotalPages"])
    avg_scores = avg_scores.drop(columns=["WeightedScore"])
    avg_scores = (avg_scores.reset_index().sort_values("AverageScore",
                                                       ascending=False))

    return avg_scores
