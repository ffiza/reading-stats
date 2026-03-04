import pandas as pd
import matplotlib.pyplot as plt

from settings import Settings
from colors import Colors


def _pick_row(group):
    times_read = len(group)

    if group["ReadDate"].notna().any():
        row = group.loc[group["ReadDate"].idxmax()]
    else:
        row = group.loc[group["ReadScore"].idxmax()]

    row = row.copy()
    row["TimesRead"] = times_read
    return row


def export_top_works() -> None:
    df = pd.read_csv("data/processed/read_history.csv")
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
    result.to_csv("data/results/top_works.csv", index=False)


def plot_works_score_scatter(df: pd.DataFrame) -> None:
    WORKS_TO_HIGHLIGHT = [
        "The Stand",
        "The Brief Wondrous Life of Oscar Wao",
        "A Canticle for Leibowitz",
        "The Martian Chronicles",
        "2001: A Space Odyssey",
        "I Have No Mouth, and I Must Scream"
    ]

    fig = plt.figure(figsize=(7, 5))
    gs = fig.add_gridspec(ncols=1, nrows=1, hspace=0, wspace=0)
    ax = fig.add_subplot(gs[0, 0])

    fig.patch.set_facecolor(Colors.LIGHTGRAY)
    ax.set_facecolor(Colors.LIGHTGRAY)

    ax.set_xlim(0.95, 5.05)
    ax.set_ylim(0.95, 5.05)
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_xlabel("MY SCORE", fontsize=8,
                  fontname=Settings.FONTNAME, color=Colors.DARKGRAY)
    ax.set_ylabel("GOODREADS SCORE", rotation=0, fontsize=8,
                  fontname=Settings.FONTNAME, color=Colors.DARKGRAY)
    ax.yaxis.set_label_coords(0.05, 1.02)
    ax.tick_params(axis='y', length=0, labelsize=9)
    ax.tick_params(axis='x', length=0, labelsize=9)
    ax.grid(visible=True, color=Colors.DARKGRAY, alpha=0.3,
            linestyle=(0, (5, 4)), linewidth=0.5)

    for label in ax.get_yticklabels():
        label.set_fontname(Settings.FONTNAME)

    for label in ax.get_xticklabels():
        label.set_fontname(Settings.FONTNAME)

    for spine in ["right", "top"]:
        ax.spines[spine].set_visible(False)

    plt.text(
        -0.05, 1.18, va="bottom", ha="left", fontsize=14,
        transform=ax.transAxes, color=Colors.DARKGRAY,
        s="Comparing Scores",
        fontname=Settings.FONTNAME, weight=800)
    plt.text(
        -0.05, 1.17, va="top", ha="left", fontsize=10,
        transform=ax.transAxes, color=Colors.DARKGRAY,
        s="This shows how my scores compare to Goodreads scores "
          "for all work types in the database.",
        fontname=Settings.FONTNAME)
    plt.text(
        -0.04, -0.16, s="Source:", fontweight="bold", fontsize=8,
        transform=ax.transAxes, color=Colors.DARKGRAY,
        fontname=Settings.FONTNAME, va="bottom", ha="left")
    plt.text(
        0.04, -0.16, s=" https://github.com/ffiza/reading-stats",
        fontsize=8, transform=ax.transAxes, color=Colors.DARKGRAY,
        fontname=Settings.FONTNAME, va="bottom", ha="left")

    for work_type in ["Novel", "Short Story", "Novella", "Novelette"]:
        df_work_type = df[df["WorkType"] == work_type]
        ax.scatter(df_work_type["ReadScore"], df_work_type["GoodreadsScore"],
                   s=10, color=Settings.COLOR_MAPPING[work_type],
                   marker=Settings.WORK_TYPE_SYMBOLS[work_type],
                   label=Settings.PLURAL_WORK_NAME[work_type])

    ax.legend(loc="lower left", frameon=False,
              prop={"family": Settings.FONTNAME, "size": 9})

    for work in WORKS_TO_HIGHLIGHT:
        df_work = df[df["WorkName"] == work]
        if not df_work.empty:
            ax.scatter(
                df_work["ReadScore"], df_work["GoodreadsScore"],
                s=10, label=work, zorder=20, linewidth=0.5,
                marker=Settings.WORK_TYPE_SYMBOLS[
                    df_work["WorkType"].values[0]],
                facecolor="none", edgecolor=Colors.DARKGRAY,)
            ax.annotate(
                work,
                (df_work["ReadScore"].values[0],
                 df_work["GoodreadsScore"].values[0]),
                textcoords="data",
                xytext=(5.1, df_work["GoodreadsScore"].values[0]), ha='left',
                va="center", arrowprops=dict(arrowstyle='-', lw=0.5,),
                fontsize=8, fontname=Settings.FONTNAME, color=Colors.DARKGRAY,
                zorder=25)

    fig.tight_layout()
    ax.set_position((0.05, 0.12, 0.66, 0.7))
    fig.savefig("images/work_score_scatter.png", dpi=1000)


if __name__ == "__main__":
    export_top_works()
    df = pd.read_csv("data/results/top_works.csv")
    plot_works_score_scatter(df)
