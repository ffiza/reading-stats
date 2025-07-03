import sqlite3
import numpy as np
import pandas as pd
from typing import List
import matplotlib.pyplot as plt

from settings import Settings
from colors import Colors

QUERY = """
    SELECT
        R.WorkID,
        W.Name,
        W.PublishedOn,
        R.Score,
        W.Type,
        A.Name AS Author
    FROM READS R
    JOIN WORKS W ON R.WorkID = W.WorkID
    JOIN AUTHOR_WORK AW ON R.WorkID = AW.WorkID
    JOIN AUTHORS A ON AW.AuthorID = A.AuthorID
    WHERE R.Status = "FINISHED"
    """


class WorksAnalysis:
    def __init__(self, database_path: str):
        conn = sqlite3.connect(database_path)
        self.authors = pd.read_sql("SELECT * FROM AUTHORS", conn)
        self.df = pd.read_sql(QUERY, conn)
        conn.close()

        self.df["PublishedOn"] = self.df["PublishedOn"].astype(np.uint16)
        self.df["Type"] = self.df["Type"].astype("category")
        self.df = self.df.sort_values(
            by="Score", ascending=False).reset_index()

    def get_unique_works(self) -> pd.DataFrame:
        df = self.df.drop_duplicates(subset=["Name"]).reset_index()
        df = df.drop(columns=["level_0", "index"])
        return df

    def get_work_authors_list(self, title: str) -> List[str]:
        if title not in self.df["Name"].unique():
            print(f"Title `{title}` not found in database.")
            return []
        return list(self.df[self.df["Name"] == title]["Author"].unique())

    def plot_highest_rated_works(self, work_type: str) -> None:
        N_WORKS: int = 20
        SEPARATION: float = 0.5
        df = self.get_unique_works()
        df = df[df["Type"] == work_type]
        df = df.reset_index()

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
            name = df.loc[i]['Name'].replace(' ', '\\ ').replace(
                "-", r"\text{-}")
            year = df.loc[i]['PublishedOn']
            ax.text(x=0.2, y=i + SEPARATION * i,
                    s=f"$\\bf{{{name}}}$ ({year})",
                    ha="left", va="bottom", color=Colors.DARKGRAY, size=3.5,
                    fontname=Settings.FONTNAME,)
            authors = self.get_work_authors_list(str(df.loc[i]['Name']))
            authors_text = " & ".join(authors)
            ax.text(x=0.2, y=i + SEPARATION * i, s=authors_text,
                    style='italic', fontname=Settings.FONTNAME,
                    ha="left", va="top", color=Colors.DARKGRAY, size=3)

        plt.text(
            0.02, 1.06, va="bottom", ha="left", fontsize=6,
            transform=ax.transAxes, color=Colors.DARKGRAY,
            s=f"Top 20 Highest Rated {Settings.PLURAL_WORK_NAME[work_type]}",
            fontname=Settings.FONTNAME, weight=800,
        )

        plt.subplots_adjust(left=0, right=1, bottom=0)
        fig.savefig(
            "images/highest_rated_"
            f"{Settings.PLURAL_WORK_NAME[work_type].lower().replace(' ', '_')}"
            ".png", dpi=500)


if __name__ == "__main__":
    a = WorksAnalysis(Settings.DATABASE_PATH)
    a.plot_highest_rated_works(work_type="Novel")
    a.plot_highest_rated_works(work_type="Short Story")
