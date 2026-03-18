import matplotlib.pyplot as plt
from reading_stats import config
from reading_stats.charts.scatter import (
    apply_base_style,
    add_titles,
    add_source,
    highlight_points,
    )
from reading_stats.services import works
from reading_stats.utils.colors import Colors
from reading_stats.utils.styles import Styles

WORKS_TO_HIGHLIGHT = [
    "The Stand",
    "The Brief Wondrous Life of Oscar Wao",
    "A Canticle for Leibowitz",
    "The Martian Chronicles",
    "2001: A Space Odyssey",
    "I Have No Mouth, and I Must Scream",
]


def run() -> None:
    df = works.get_works_stats()

    fig, ax = plt.subplots(figsize=(7, 5))
    apply_base_style(fig, ax)

    ax.set_xlim(0.95, 5.05)
    ax.set_ylim(0.95, 5.05)
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_xlabel("MY SCORE", fontsize=7, color=Colors.DARKGRAY)
    ax.set_ylabel("GOODREADS SCORE", rotation=0, fontsize=7,
                  color=Colors.DARKGRAY)
    ax.yaxis.set_label_coords(0.05, 1.02)

    for work_type in ["Novel", "Short Story", "Novella", "Novelette"]:
        subset = df[df["WorkType"] == work_type]
        ax.scatter(
            subset["ReadScore"], subset["GoodreadsScore"],
            s=10,
            color=Styles.WORK_TYPE_COLOR_MAPPING[work_type],
            marker=Styles.WORK_TYPE_SYMBOLS[work_type],
            label=Styles.PLURAL_WORK_NAME[work_type],
        )

    ax.legend(
        loc="lower left", frameon=False,
        prop={"family": Styles.FONTNAME, "size": 9},
    )

    add_titles(
        ax,
        title="Comparing Scores",
        subtitle=(
            "This shows how my scores compare to Goodreads scores"
            " for all work types in the database."
        ),
    )
    add_source(ax, "https://github.com/ffiza/reading-stats")
    highlight_points(
        ax, df,
        labels=WORKS_TO_HIGHLIGHT,
        label_col="WorkName",
        x_col="ReadScore",
        y_col="GoodreadsScore",
        annotation_x=5.1,
    )

    fig.tight_layout()
    ax.set_position((0.05, 0.12, 0.66, 0.7))
    fig.savefig(config.works_fig_file, dpi=1000)
    plt.close(fig)


if __name__ == "__main__":
    run()
