import pandas as pd
from reading_stats.config import CONFIG


def export_authors_stats(save_csv: bool = False) -> pd.DataFrame:
    df = pd.read_csv(CONFIG["ReadHistory"]["ReadHistoryDataFile"])
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

    if save_csv:
        avg_scores.to_csv(CONFIG["Authors"]["DataOutputFile"], index=False)
    return avg_scores
