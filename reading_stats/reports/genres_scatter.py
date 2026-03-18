import matplotlib.pyplot as plt
from reading_stats import config
from reading_stats.charts.scatter import (
    apply_base_style,
    add_titles,
    add_source,
)
from reading_stats.services import genres
from reading_stats.utils.colors import Colors
from reading_stats.utils.styles import Styles

GENRES_TO_HIGHLIGHT = [
    "Fiction: Science Fiction",
    "Fiction: Horror",
    "Fiction: Horror: Cosmic",
    "Fiction: Fantasy: Grimdark",
    "Fiction: Science Fiction: Cyberpunk",
    "Fiction: Horror: Folk",
    "Fiction: Science Fiction: Apocalyptic",
]

TOP_LEVEL_GENRES = [
    "Fiction: Fantasy",
    "Fiction: Horror",
    "Fiction: Historical",
    "Fiction: Science Fiction",
    "Non-Fiction",
]


def run() -> None:
    df = genres.get_genre_stats()

    fig, ax = plt.subplots(figsize=(7, 5))
    apply_base_style(fig, ax)

    ax.set_xlim(0, 5.05)
    ax.set_ylim(100, 32_000)
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_yscale("log")
    ax.set_yticks([100, 1_000, 10_000], labels=["100", "1k", "10k"])
    ax.set_xlabel("AVERAGE SCORE", fontsize=7, color=Colors.DARKGRAY)
    ax.set_ylabel("PAGES READ", rotation=0, fontsize=7, color=Colors.DARKGRAY)
    ax.yaxis.set_label_coords(0.05, 1.02)

    for genre in TOP_LEVEL_GENRES:
        subset = df[df["Genre"].str.startswith(genre)]
        ax.scatter(
            subset["AverageScore"], subset["TotalPages"],
            s=10,
            color=Styles.GENRE_COLOR_MAPPING[genre],
            marker=Styles.GENRE_SYMBOLS[genre],
            label=genre,
        )

    ax.legend(
        loc="lower left", frameon=False,
        prop={"family": Styles.FONTNAME, "size": 9},
    )

    add_titles(
        ax,
        title="Top Genres",
        subtitle=(
            "This shows both the page-weighted average of all the works read"
            " and the total number\nof pages read for all genres in the"
            " database."
        ),
    )
    add_source(ax, "https://github.com/ffiza/reading-stats")

    for genre in GENRES_TO_HIGHLIGHT:
        subset = df[df["Genre"] == genre]
        if subset.empty:
            continue
        top_level = ":".join(genre.split(":")[:2]).strip()
        ax.scatter(
            subset["AverageScore"], subset["TotalPages"],
            s=10, label=genre, zorder=20, linewidth=0.5,
            marker=Styles.GENRE_SYMBOLS[top_level],
            facecolor="none", edgecolor=Colors.DARKGRAY,
        )
        ax.annotate(
            genre,
            (subset["AverageScore"].values[0], subset["TotalPages"].values[0]),
            textcoords="data",
            xytext=(5.1, subset["TotalPages"].values[0]),
            ha="left", va="center",
            arrowprops=dict(arrowstyle="-", lw=0.5),
            fontsize=8, fontname=Styles.FONTNAME,
            color=Colors.DARKGRAY, zorder=25,
        )

    fig.tight_layout()
    ax.set_position((0.05, 0.12, 0.66, 0.7))
    fig.savefig(config.genres_fig_file, dpi=1000)
    plt.close(fig)


if __name__ == "__main__":
    run()
