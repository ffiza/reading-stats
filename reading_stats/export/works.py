import pandas as pd
from reading_stats.config import CONFIG


def _pick_row(group):
    times_read = len(group)

    if group["ReadDate"].notna().any():
        row = group.loc[group["ReadDate"].idxmax()]
    else:
        row = group.loc[group["ReadScore"].idxmax()]

    row = row.copy()
    row["TimesRead"] = times_read
    return row


def export_works_stats(save_csv: bool = False) -> pd.DataFrame:
    df = pd.read_csv(CONFIG["ReadHistory"]["ReadHistoryDataFile"])
    df = df[df["ReadStatus"] == "FINISHED"].copy()
    df["ReadScore"] = pd.to_numeric(df["ReadScore"], errors="coerce")
    df["StartDate"] = pd.to_datetime(df["StartDate"], errors="coerce")
    df["FinishDate"] = pd.to_datetime(df["FinishDate"], errors="coerce")
    df["ReadDate"] = df["FinishDate"].combine_first(df["StartDate"])

    result = df.groupby(
        "WorkID", group_keys=False).apply(
            _pick_row).sort_values("ReadScore", ascending=False)

    result.drop(columns=["ReadStatus", "AuthorID", "StartDate",
                         "FinishDate", "ReadDate"], inplace=True)

    if save_csv:
        result.to_csv(CONFIG["Works"]["DataOutputFile"], index=False)

    return result
