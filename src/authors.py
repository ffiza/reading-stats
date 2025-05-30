import sqlite3
import numpy as np
import pandas as pd
from typing import List
import matplotlib.pyplot as plt

from settings import Settings

plt.style.use('seaborn-v0_8-pastel')

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

    def get_highest_rated_authors(self, amount: int = 10) -> None:
        pass

    def get_author_read(self) -> None:
        pass


def plot_most_read_authors(df: pd.DataFrame) -> None:
    df = df.sort_values("PageCount", ascending=True).reset_index(drop=True)

    minor_ticks = []
    for base in range(1000, 25000, 5000):
        for offset in range(0, 5000, 1000):
            if offset == 4000:
                continue
            minor_ticks.append(base + offset)

    fig = plt.figure(figsize=(2.5, 3.5))
    gs = fig.add_gridspec(ncols=1, nrows=1, hspace=0, wspace=0)
    ax = gs.subplots(sharex=True, sharey=True)

    ax.set_ylim(-0.5, len(df) - 0.5)
    ax.set_xlim(0, 25000)
    ax.set_xticks([0, 5000, 10000, 15000, 20000, 25000])
    ax.set_xticks(minor_ticks, minor=True)
    ax.set_xticklabels([0, "5k", "10k", "15k", "20k", "25k"])

    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    ax.tick_params(axis="x", which="major", length=2.5, width=0.7, labelsize=4)
    ax.tick_params(axis="x", which="minor", length=2.5, width=0.2, labelsize=5)
    ax.tick_params(axis="y", which="both", labelsize=4.5, length=0)
    for tick in ax.xaxis.get_minorticklines():
        tick.set_alpha(0.3)
    for spine in ["right", "left", "top", "bottom"]:
        ax.spines[spine].set_visible(False)

    ax.barh(df["Author"], df["PageCount"], zorder=10, height=0.7)

    # Add author names and page count values as labels
    for i in range(len(df["Author"])):
        pages_read = df["PageCount"].iloc[i]

        ax.text(pages_read + 200, i, pages_read, zorder=11, size=4,
                va="center", ha="left")

        x_pos = 1000
        while x_pos <= df["PageCount"].max():
            if pages_read >= x_pos:
                ax.plot([x_pos] * 2, [i - 0.7 / 2, i + 0.7 / 2],
                        color="white", lw=0.2, zorder=12, alpha=0.5)
            x_pos += 1000

        x_pos = 5000
        while x_pos <= df["PageCount"].max():
            if pages_read >= x_pos:
                ax.plot([x_pos] * 2, [i - 0.7 / 2, i + 0.7 / 2],
                        color="white", lw=0.7, zorder=12)
            x_pos += 5000

    plt.text(0.3, 0.5, "Most Read Authors", fontsize=10, va="top",
             transform=ax.transAxes)
    plt.text(
        0.3, 0.44, va="top", fontsize=5.5, transform=ax.transAxes,
        s="Visualizing the most read authors\nby the amount of pages read.",
    )

    fig.savefig("images/most_read_authors.pdf", dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    a = AuthorsAnalysis(Settings.DATABASE_PATH)
    plot_most_read_authors(df=a.get_most_read_authors(25))
