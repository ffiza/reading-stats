import sqlite3
import numpy as np
import pandas as pd
from typing import List
import matplotlib.pyplot as plt

from settings import Settings

WHITE = "#ffffff"
DARKGRAY = "#1f2328"
TITLE_FONTSIZE = 5.5
TICK_LABELS_FONTSIZE = 3.5
FONTNAME = "Segoe UI"
QUERY = """
    SELECT
        R.WorkID,
        W.Name,
        W.Series,
        W.NumberInSeries,
        W.PublishedOn,
        W.PageCount,
        R.StartDate,
        R.FinishDate,
        R.Score,
        R.Status,
        A.Name AS Author
    FROM READS R
    JOIN WORKS W ON R.WorkID = W.WorkID
    JOIN AUTHOR_WORK AW ON R.WorkID = AW.WorkID
    JOIN AUTHORS A ON AW.AuthorID = A.AuthorID
    """


class AuthorsAnalysis:
    def __init__(self, database_path: str):
        conn = sqlite3.connect(database_path)
        self.authors = pd.read_sql("SELECT * FROM AUTHORS", conn)
        self.df = pd.read_sql(QUERY, conn)
        conn.close()

        self.df["PublishedOn"] = self.df["PublishedOn"].astype(np.uint16)
        self.df["StartDate"] = pd.to_datetime(
            self.df["StartDate"], format="%Y-%m-%d", errors="coerce")
        self.df["FinishDate"] = pd.to_datetime(
            self.df["FinishDate"], format="%Y-%m-%d", errors="coerce")
        self.df["Status"] = self.df["Status"].astype("category")

    def get_unique_authors(self) -> List[str]:
        return self.df["Author"].unique().tolist()

    def get_most_read_authors(self, amount: int = 10) -> pd.DataFrame:
        g = self.df[
            self.df["Status"] == "FINISHED"].groupby("Author")[
                "PageCount"].sum().reset_index()
        return g.sort_values("PageCount", ascending=False).iloc[:amount]

    def get_highest_rated_authors(self,
                                  min_pages_read: int = 1000) -> pd.DataFrame:
        df_finished = self.df[self.df["Status"] == "FINISHED"]

        def compute_stats(x):
            weights = x["PageCount"]
            scores = x["Score"]
            weighted_mean = np.average(scores, weights=weights)
            variance = np.average((scores - weighted_mean) ** 2,
                                  weights=weights)
            weighted_std = np.sqrt(variance)
            return pd.Series({
                "TotalPages": weights.sum(),
                "WeightedScore": weighted_mean,
                "WeightedStd": weighted_std
            })

        g = df_finished.groupby("Author", group_keys=False).apply(
            compute_stats, include_groups=False).reset_index()
        g = g[g["TotalPages"] >= min_pages_read]
        g = g.sort_values("WeightedScore", ascending=False)
        g.min_pages_read = min_pages_read
        return g

    def get_author_read(self) -> None:
        pass


def plot_most_read_authors(df: pd.DataFrame) -> None:
    df = df.sort_values("PageCount", ascending=True).reset_index(drop=True)
    positions = range(len(df))

    fig = plt.figure(figsize=(1.8, 1.8))
    gs = fig.add_gridspec(ncols=1, nrows=1, hspace=0, wspace=0)
    ax = fig.add_subplot(gs[0, 0])

    ax.set_ylim(-0.5, len(df) - 0.5)
    ax.set_yticks(positions)
    ax.set_yticklabels(df["Author"])
    ax.set_xlim(0, 25000)
    ax.set_xticks([0, 25000])
    ax.set_xticks([5000, 10000, 15000, 20000], minor=True)
    ax.set_xticklabels(["0", "25k"], fontdict={"fontname": FONTNAME})
    ax.set_xticklabels(["5k", "10k", "15k", "20k"], minor=True,
                       fontdict={"fontname": FONTNAME})

    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')

    ax.tick_params(axis="x", which="major", length=1, width=0.4,
                   labelsize=TICK_LABELS_FONTSIZE, color=DARKGRAY,
                   labelcolor=DARKGRAY)
    ax.tick_params(axis="x", which="minor", length=1, width=0.4,
                   labelsize=TICK_LABELS_FONTSIZE, color=WHITE,
                   labelcolor=DARKGRAY)
    ax.tick_params(axis="y", which="both", labelsize=TICK_LABELS_FONTSIZE,
                   length=0, labelcolor=DARKGRAY)

    for tick in ax.get_yticklabels():
        tick.set_fontname(FONTNAME)

    for spine in ["right", "left", "bottom"]:
        ax.spines[spine].set_visible(False)
    ax.spines["top"].set_color(DARKGRAY)
    ax.spines["top"].set_linewidth(0.4)

    ax.scatter(df["PageCount"], positions, zorder=10,
               color=DARKGRAY, s=5, facecolor="none", linewidths=0.5)

    for i, row in df.iterrows():
        ax.text(row["PageCount"], float(i) - 0.5, row["PageCount"], zorder=11,
                size=2.25, va="center", ha="center", color=DARKGRAY,
                fontname=FONTNAME)

    plt.text(
        -0.4, 1.15, va="bottom", ha="left", fontsize=TITLE_FONTSIZE,
        transform=ax.transAxes, color=DARKGRAY,
        s=f"Top {len(df)} Most Read Authors by Page Count",
        fontname=FONTNAME,
    )

    fig.savefig("images/most_read_authors.png", dpi=500, bbox_inches="tight")


def plot_highest_rated_authors(df: pd.DataFrame) -> None:
    df_filtered = df.sort_values(
        "WeightedScore", ascending=True).reset_index(drop=True)
    positions = range(len(df_filtered))

    fig = plt.figure(figsize=(1.8, 1.8))
    gs = fig.add_gridspec(ncols=1, nrows=1, hspace=0, wspace=0)
    ax = fig.add_subplot(gs[0, 0])

    ax.set_ylim(-0.5, len(df_filtered) - 0.5)
    ax.set_yticks(positions)
    ax.set_yticklabels(df_filtered["Author"])
    ax.set_xlim(0, 5)
    ax.set_xticks([0, 5])
    ax.set_xticks([1, 2, 3, 4], minor=True)
    ax.set_xticklabels(["0", "5"], fontdict={"fontname": FONTNAME})
    ax.set_xticklabels(["1", "2", "3", "4"], minor=True,
                       fontdict={"fontname": FONTNAME})

    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')

    ax.tick_params(axis="x", which="major", length=1, width=0.4,
                   labelsize=TICK_LABELS_FONTSIZE, color=DARKGRAY,
                   labelcolor=DARKGRAY)
    ax.tick_params(axis="x", which="minor", length=1, width=0.4,
                   labelsize=TICK_LABELS_FONTSIZE, color=WHITE,
                   labelcolor=DARKGRAY)
    ax.tick_params(axis="y", which="both", labelsize=TICK_LABELS_FONTSIZE,
                   length=0, labelcolor=DARKGRAY)

    for tick in ax.get_yticklabels():
        tick.set_fontname(FONTNAME)

    for spine in ["right", "left", "bottom"]:
        ax.spines[spine].set_visible(False)
    ax.spines["top"].set_color(DARKGRAY)
    ax.spines["top"].set_linewidth(0.4)

    ax.scatter(df_filtered["WeightedScore"], positions, zorder=10,
               color=DARKGRAY, s=5, facecolor="none", linewidths=0.5)

    for i, score in enumerate(df_filtered["WeightedScore"]):
        ax.text(score, i - 0.5,
                str(round(score, 2)).ljust(4, "0"),
                zorder=11, size=2.25, va="center", ha="center", color=DARKGRAY,
                fontname=FONTNAME,)

    plt.text(
        -0.4, 1.15, va="bottom", ha="left", fontsize=TITLE_FONTSIZE,
        transform=ax.transAxes, color=DARKGRAY,
        s=f"Scores of Authors with {df.min_pages_read}+ Pages Read",
        fontname=FONTNAME,
    )

    fig.savefig("images/authors_scores.png",
                dpi=500, bbox_inches="tight")


if __name__ == "__main__":
    a = AuthorsAnalysis(Settings.DATABASE_PATH)
    plot_most_read_authors(df=a.get_most_read_authors(15))
    plot_highest_rated_authors(
        df=a.get_highest_rated_authors(min_pages_read=1500))
