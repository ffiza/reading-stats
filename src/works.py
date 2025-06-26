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
        N_WORKS: int = 10
        TEXT_OFFSET: float = -0.03
        df = self.get_unique_works()
        df = df[df["Type"] == work_type]
        df = df.reset_index()

        fig = plt.figure(figsize=(1.8, 1.8))
        gs = fig.add_gridspec(ncols=1, nrows=1, hspace=0, wspace=0)
        ax = fig.add_subplot(gs[0, 0])

        ax.set_ylim(-0.5, N_WORKS - 0.5)
        ax.set_yticks([])
        ax.set_xlim(-0.25, 5)
        ax.set_xticks([])

        for spine in ["right", "left", "bottom", "top"]:
            ax.spines[spine].set_visible(False)

        for i in range(N_WORKS):
            j = N_WORKS - i
            ax.scatter(0, i, s=20, color=Colors.DARKGRAY, zorder=20)
            ax.text(x=0, y=i + TEXT_OFFSET, s=str(j), ha="center", va="center",
                    color=Colors.WHITE, size=3, weight=600, zorder=21,
                    fontname=Settings.FONTNAME,)
            name = df.loc[j]['Name'].replace(' ', '\\ ').replace(
                "-", r"\text{-}")
            year = df.loc[j]['PublishedOn']
            ax.text(x=0.4, y=i + TEXT_OFFSET, s=f"$\\bf{{{name}}}$ ({year})",
                    ha="left", va="center", color=Colors.DARKGRAY, size=4,
                    fontname=Settings.FONTNAME,)
            authors = self.get_work_authors_list(str(df.loc[j]['Name']))
            authors_text = " & ".join(authors)
            ax.text(x=0.4, y=i - 0.4, s=authors_text, style='italic',
                    ha="left", va="center", color=Colors.DARKGRAY, size=3.5,
                    fontname=Settings.FONTNAME,)

        plt.text(
            0, 1.02, va="bottom", ha="left", fontsize=Settings.TITLE_FONTSIZE,
            transform=ax.transAxes, color=Colors.DARKGRAY,
            s=f"Top {N_WORKS} Highest Rated "
              f"{Settings.PLURAL_WORK_NAME[work_type]}",
            fontname=Settings.FONTNAME,
        )

        fig.savefig(
            "images/highest_rated_"
            f"{Settings.PLURAL_WORK_NAME[work_type].lower().replace(' ', '_')}"
            ".png",
            dpi=500, bbox_inches="tight")


if __name__ == "__main__":
    a = WorksAnalysis(Settings.DATABASE_PATH)
    a.plot_highest_rated_works(work_type="Novel")
    a.plot_highest_rated_works(work_type="Short Story")
