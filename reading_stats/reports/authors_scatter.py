import matplotlib.pyplot as plt
from reading_stats import config
from reading_stats.charts.scatter import (
    apply_base_style,
    add_titles,
    add_source,
    highlight_points,
    )
from reading_stats.services import authors
from reading_stats.utils.colors import Colors

AUTHORS_TO_HIGHLIGHT = [
        "Stephen King",
        "Dan Simmons",
        "George R. R. Martin",
        "J. R. R. Tolkien",
        "Michael Chabon",
        "Octavia E. Butler",
        "Margaret Atwood",
        "Harlan Ellison",
    ]


def run() -> None:
    df = authors.get_author_stats()

    fig, ax = plt.subplots(figsize=(7, 5))
    apply_base_style(fig, ax)

    ax.set_xlim(0, 5.05)
    ax.set_ylim(1, 25_000)
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_yscale("log")
    ax.set_yticks(
        [1, 10, 100, 1_000, 10_000],
        labels=["0", "10", "100", "1k", "10k"],
    )
    ax.set_xlabel("AVERAGE SCORE", fontsize=7, color=Colors.DARKGRAY)
    ax.set_ylabel("PAGES READ", rotation=0, fontsize=7, color=Colors.DARKGRAY)
    ax.yaxis.set_label_coords(0.05, 1.02)

    ax.scatter(df["WeightedReadScore"], df["TotalPages"],
               s=10, color=Colors.PURPLE, zorder=15)

    add_titles(
        ax,
        title="Top Rated, Most Read",
        subtitle=(
            "This shows both the page-weighted average of all the works read"
            " and the total number\nof pages read for all authors in the"
            " database."
        ),
    )
    add_source(ax, "https://github.com/ffiza/reading-stats")
    highlight_points(
        ax, df,
        labels=AUTHORS_TO_HIGHLIGHT,
        label_col="AuthorName",
        x_col="WeightedReadScore",
        y_col="TotalPages",
        annotation_x=5.1,
    )

    fig.tight_layout()
    ax.set_position((0.05, 0.12, 0.66, 0.7))
    fig.savefig(config.authors_fig_file, dpi=1000)
    plt.close(fig)


if __name__ == "__main__":
    run()
