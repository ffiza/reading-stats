import pandas as pd
from reading_stats.config import CONFIG


def export_genres_stats(save_csv: bool = False) -> pd.DataFrame:
    df = pd.read_csv(CONFIG["ReadHistory"]["ReadHistoryDataFile"])
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

    if save_csv:
        avg_scores.to_csv(CONFIG["Genres"]["DataOutputFile"],
                          float_format="%.3f", index=False)
    return avg_scores
