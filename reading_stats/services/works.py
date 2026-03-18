import pandas as pd
from reading_stats.db import queries


def get_works_stats() -> pd.DataFrame:
    df = queries.get_read_history()
    df = df[df["ReadStatus"] == "FINISHED"].copy()
    df["ReadScore"] = pd.to_numeric(df["ReadScore"], errors="coerce")
    df["StartDate"] = pd.to_datetime(df["StartDate"], errors="coerce")
    df["FinishDate"] = pd.to_datetime(df["FinishDate"], errors="coerce")
    df["ReadDate"] = df["FinishDate"].combine_first(df["StartDate"])

    result = df.groupby(
        ["WorkID"], group_keys=False).apply(
            _pick_row).sort_values("ReadScore", ascending=False)

    result.drop(columns=["ReadStatus", "AuthorID", "StartDate",
                         "FinishDate", "ReadDate"], inplace=True)

    return result


def get_next_reads() -> pd.DataFrame:
    return queries.get_next_reads()


def _pick_row(group):
    times_read = len(group)

    if group["ReadDate"].notna().any():
        row = group.loc[group["ReadDate"].idxmax()]
    else:
        row = group.loc[group["ReadScore"].idxmax()]

    row = row.copy()
    row["TimesRead"] = times_read
    return row
