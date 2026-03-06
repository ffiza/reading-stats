import pandas as pd
import matplotlib.pyplot as plt
from reading_stats.config import CONFIG
from reading_stats.colors import Colors
from reading_stats.settings import Settings
from reading_stats.export.genres import export_genres_stats

GENRES_TO_HIGHLIGHT = [
    "Fiction: Science Fiction",
    "Fiction: Horror",
    "Fiction: Science Fiction: Alternative History"
]


def plot_genre_scatter(
        df: pd.DataFrame,
        genres_to_highlight: list = []) -> None:

    fig = plt.figure(figsize=(7, 5))
    gs = fig.add_gridspec(ncols=1, nrows=1, hspace=0, wspace=0)
    ax = fig.add_subplot(gs[0, 0])

    fig.patch.set_facecolor(Colors.LIGHTGRAY)
    ax.set_facecolor(Colors.LIGHTGRAY)

    ax.set_xlim(0, 5.05)
    ax.set_ylim(100, 32_000)
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_yscale("log")
    ax.set_yticks([100, 1_000, 10_000],
                  labels=["100", "1k", "10k"])
    ax.set_xlabel("AVERAGE SCORE", fontsize=8,
                  fontname=Settings.FONTNAME, color=Colors.DARKGRAY)
    ax.set_ylabel("PAGES READ", rotation=0, fontsize=8,
                  fontname=Settings.FONTNAME, color=Colors.DARKGRAY)
    ax.yaxis.set_label_coords(0.05, 1.02)
    ax.tick_params(axis='y', which="both", length=0, labelsize=9)
    ax.tick_params(axis='x', length=0, labelsize=9)
    ax.grid(visible=True, color=Colors.DARKGRAY, alpha=0.3,
            linestyle=(0, (5, 4)), linewidth=0.5)

    for label in ax.get_yticklabels():
        label.set_fontname(Settings.FONTNAME)

    for label in ax.get_xticklabels():
        label.set_fontname(Settings.FONTNAME)

    for spine in ["right", "top"]:
        ax.spines[spine].set_visible(False)

    for genre in ["Fiction: Fantasy", "Fiction: Horror",
                  "Fiction: Historical",
                  "Fiction: Science Fiction", "Non-Fiction"]:
        df_genre = df[df["Genre"].str.startswith(genre)]
        ax.scatter(df_genre["AverageScore"], df_genre["TotalPages"],
                   s=10, color=Settings.GENRE_COLOR_MAPPING[genre],
                   marker=Settings.GENRE_SYMBOLS[genre], label=genre)

    plt.text(
        -0.05, 1.18, va="bottom", ha="left", fontsize=14,
        transform=ax.transAxes, color=Colors.DARKGRAY,
        s="Top Genres",
        fontname=Settings.FONTNAME, weight=800)
    plt.text(
        -0.05, 1.17, va="top", ha="left", fontsize=10,
        transform=ax.transAxes, color=Colors.DARKGRAY,
        s="This shows both the page-weighted average of all the works read and"
          " the total number\nof pages read for all genres in the database.",
        fontname=Settings.FONTNAME)
    plt.text(
        -0.04, -0.16, s="Source:", fontweight="bold", fontsize=8,
        transform=ax.transAxes, color=Colors.DARKGRAY,
        fontname=Settings.FONTNAME, va="bottom", ha="left")
    plt.text(
        0.04, -0.16, s=" https://github.com/ffiza/reading-stats",
        fontsize=8, transform=ax.transAxes, color=Colors.DARKGRAY,
        fontname=Settings.FONTNAME, va="bottom", ha="left")

    ax.legend(loc="lower left", frameon=False,
              prop={"family": Settings.FONTNAME, "size": 9})

    if len(genres_to_highlight) >= 1:
        for genre in GENRES_TO_HIGHLIGHT:
            df_genre = df[df["Genre"] == genre]
            if not df_genre.empty:
                ax.scatter(
                    df_genre["AverageScore"], df_genre["TotalPages"],
                    s=10, label=genre, zorder=20, linewidth=0.5,
                    marker=Settings.GENRE_SYMBOLS[
                        ":".join(genre.split(":")[0:2])],
                    facecolor="none", edgecolor=Colors.DARKGRAY,)
                ax.annotate(
                    genre,
                    (df_genre["AverageScore"].values[0],
                     df_genre["TotalPages"].values[0]),
                    textcoords="data",
                    xytext=(5.1, df_genre["TotalPages"].values[0]), ha='left',
                    va="center", arrowprops=dict(arrowstyle='-', lw=0.5,),
                    fontsize=8, fontname=Settings.FONTNAME,
                    color=Colors.DARKGRAY,
                    zorder=25)

    fig.tight_layout()
    ax.set_position((0.05, 0.12, 0.66, 0.7))
    fig.savefig(CONFIG["Genres"]["FigOutputFile"], dpi=1000)


if __name__ == "__main__":
    df = export_genres_stats()
    plot_genre_scatter(df, GENRES_TO_HIGHLIGHT)
