import argparse
import matplotlib.pyplot as plt
from reading_stats import config
from reading_stats.charts.bar import apply_base_style
from reading_stats.charts.scatter import add_titles, add_source
from reading_stats.services.bibliography import (
    get_author_bibliography,
    get_author_bibliography_for_table,
    )
from reading_stats.utils.colors import Colors
from reading_stats.utils.styles import Styles
from reading_stats.charts.table import to_markdown


def run(author: str) -> None:
    totals = get_author_bibliography(author)

    fig, ax = plt.subplots(figsize=(7, 5))
    apply_base_style(fig, ax)

    ax.set_xlim(totals.index.min() - 1, totals.index.max() + 1)
    ax.set_ylim(0, totals["TotalPagesPublished"].max() + 200)
    ax.set_xlabel("YEAR", fontsize=7, color=Colors.DARKGRAY)
    ax.set_ylabel("PAGES", rotation=0, fontsize=7, color=Colors.DARKGRAY)
    ax.yaxis.set_label_coords(0, 1.02)

    bottom = 0
    for work_type in Styles.WORK_TYPE_SYMBOLS:
        col = f"TotalPagesRead_{work_type.replace(' ', '')}"
        ax.bar(
            totals.index, totals[col], 1,
            bottom=bottom,
            color=Styles.WORK_TYPE_COLOR_MAPPING[work_type],
            label=work_type,
        )
        bottom += totals[col]

    ax.step(
        totals.index, totals["TotalPagesPublished"],
        where="mid", color=Colors.DARKGRAY,
        label="Pages Published", linewidth=1,
    )
    ax.legend(loc="upper right", fontsize=8, frameon=False, ncol=1)

    add_titles(
        ax,
        title=f"{author} Bibliography History",
        subtitle=(
            "This shows the total amount of pages published by year (black"
            " line) and the total pages I've read,\ncoloured by work type."
        ),
    )
    add_source(ax, "https://github.com/ffiza/reading-stats",
               source_text_xanchor=0.03)

    fig.tight_layout()
    ax.set_position((0.05, 0.12, 0.9, 0.7))

    filename = author.replace(".", "").replace(" ", "_").lower() \
        + "_bibliography.png"
    fig.savefig(config.authors_fig_file.parent / filename, dpi=1000)
    plt.close(fig)


def run_table(author: str) -> None:
    df = get_author_bibliography_for_table(author)
    filename = author.replace(".", "").replace(" ", "_").lower() + ".md"
    to_markdown(df, config.author_biblio_output_dir / filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--author", required=True, help="Author name.")
    parser.add_argument("--table", action="store_true")
    args = parser.parse_args()
    run(args.author)
    if args.table:
        run_table(args.author)
