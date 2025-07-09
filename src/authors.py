import sqlite3
import numpy as np
import pandas as pd
from typing import List
import matplotlib.pyplot as plt

from colors import Colors
from settings import Settings


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
        A.Country,
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

    def get_authors_df(self) -> pd.DataFrame:
        df_finished = self.df[self.df["Status"] == "FINISHED"]
        grouped = df_finished.groupby("Author").apply(
            lambda x: pd.Series({
                "PagesRead": x["PageCount"].sum(),
                "Country": x["Country"].iloc[0],
                "WeightedAvgScore": np.average(x["Score"],
                                               weights=x["PageCount"])
            })
        ).reset_index()
        grouped = grouped.rename(columns={"Author": "AuthorName"})
        grouped["PagesRead"] = grouped["PagesRead"].astype(int)
        return grouped


def plot_most_read_authors(df: pd.DataFrame) -> None:
    N_WORKS: int = 20
    SEPARATION: float = 0.5
    df = df.sort_values("PagesRead", ascending=False).reset_index(drop=True)

    fig = plt.figure(figsize=(1.8, 2.5))
    gs = fig.add_gridspec(ncols=1, nrows=1, hspace=0, wspace=0)
    ax = fig.add_subplot(gs[0, 0])

    ax.set_ylim(-0.6, 29.1)
    ax.set_yticks([])
    ax.set_xlim(-0.25, 5)
    ax.set_xticks([])
    plt.gca().invert_yaxis()

    for spine in ["right", "left", "bottom", "top"]:
        ax.spines[spine].set_visible(False)

    for i in range(N_WORKS):
        ax.annotate(
            str(i + 1), xy=(0.02, i + SEPARATION * i),
            ha="center", va="center", color=Colors.DARKGRAY,
            size=4, weight=800, zorder=21, fontname=Settings.FONTNAME)
        name = df.loc[i]['AuthorName'].replace(' ', '\\ ').replace(
            "-", r"\text{-}")
        ax.text(x=0.2, y=i + SEPARATION * i,
                s=f"$\\bf{{{name}}}$",
                ha="left", va="bottom", color=Colors.DARKGRAY, size=3.5,
                fontname='Segoe UI Emoji',)
        pages_txt: str = str(df.loc[i]["PagesRead"]) + " pages read"
        ax.text(x=0.2, y=i + SEPARATION * i, s=pages_txt,
                style='italic', fontname=Settings.FONTNAME,
                ha="left", va="top", color=Colors.DARKGRAY, size=3)

    plt.text(
        0.02, 1.06, va="bottom", ha="left", fontsize=6,
        transform=ax.transAxes, color=Colors.DARKGRAY,
        s=f"Top 20 Most Read Authors",
        fontname=Settings.FONTNAME, weight=800,
    )

    plt.subplots_adjust(left=0, right=1, bottom=0)
    fig.savefig("images/most_read_authors.png", dpi=1000)


def plot_highest_rated_authors(df: pd.DataFrame) -> None:
    N_WORKS: int = 20
    SEPARATION: float = 0.5
    MIN_PAGES_READ: int = 500
    df = df.sort_values("WeightedAvgScore",
                        ascending=False).reset_index(drop=True)
    df_filtered = df[df["PagesRead"] >= MIN_PAGES_READ].copy().reset_index(
        drop=True)

    fig = plt.figure(figsize=(1.8, 1.8))
    gs = fig.add_gridspec(ncols=1, nrows=1, hspace=0, wspace=0)
    ax = fig.add_subplot(gs[0, 0])

    fig = plt.figure(figsize=(1.8, 2.5))
    gs = fig.add_gridspec(ncols=1, nrows=1, hspace=0, wspace=0)
    ax = fig.add_subplot(gs[0, 0])

    ax.set_ylim(-0.6, 29.1)
    ax.set_yticks([])
    ax.set_xlim(-0.25, 5)
    ax.set_xticks([])
    plt.gca().invert_yaxis()

    for spine in ["right", "left", "bottom", "top"]:
        ax.spines[spine].set_visible(False)

    for i in range(N_WORKS):
        ax.annotate(
            str(i + 1), xy=(0.02, i + SEPARATION * i),
            ha="center", va="center", color=Colors.DARKGRAY,
            size=4, weight=800, zorder=21, fontname=Settings.FONTNAME)
        name = df_filtered.loc[i]['AuthorName'].replace(' ', '\\ ').replace(
            "-", r"\text{-}")
        pages_txt: str = str(df_filtered.loc[i]["PagesRead"]) + " pages read"
        ax.text(x=0.2, y=i + SEPARATION * i,
                s=f"$\\bf{{{name}}}$ ({pages_txt})",
                ha="left", va="bottom", color=Colors.DARKGRAY, size=3.5,
                fontname='Segoe UI Emoji',)
        score_txt: str = "Score: " \
            + str(int(df_filtered.loc[i]["WeightedAvgScore"] / 5 * 100))
        ax.text(x=0.2, y=i + SEPARATION * i, s=score_txt,
                style='italic', fontname=Settings.FONTNAME,
                ha="left", va="top", color=Colors.DARKGRAY, size=3)

    plt.text(
        0.02, 1.06, va="bottom", ha="left", fontsize=6,
        transform=ax.transAxes, color=Colors.DARKGRAY,
        s=f"Top 20 Highest Rated Authors",
        fontname=Settings.FONTNAME, weight=800,
    )

    plt.subplots_adjust(left=0, right=1, bottom=0)
    fig.savefig("images/highest_rated_authors.png", dpi=1000)


if __name__ == "__main__":
    a = AuthorsAnalysis(Settings.DATABASE_PATH)
    plot_most_read_authors(df=a.get_authors_df())
    plot_highest_rated_authors(df=a.get_authors_df())
