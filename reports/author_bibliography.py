import argparse
import pandas as pd
import matplotlib.pyplot as plt
from reading_stats.colors import Colors
from reading_stats.config import CONFIG
from reading_stats.settings import Settings


def load_data(author_name: str) -> pd.DataFrame:
    filename = author_name.replace(".", "").replace(" ", "_").lower() + ".md"

    df = pd.read_table(
        f"data/tables/{filename}",
        sep=r'\s*\|\s*',
        engine='python',
        skiprows=[1],
        skipinitialspace=True
        ).dropna(axis=1, how='all')
    return df


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    feats_to_drop = [
        "Title", "Series", "Order", "MyScore", "GoodreadsScore", "LastReadOn"]
    for feat_to_drop in feats_to_drop:
        if feat_to_drop in df.columns:
            df = df.drop(columns=[feat_to_drop])
    df["ReadStatus"] = df["ReadStatus"].fillna("NOT READ")
    df["ReadStatus"] = df["ReadStatus"].astype("category")
    df["Type"] = df["Type"].astype("category")

    totals = pd.DataFrame({})
    totals["TotalPagesPublished"] = df.groupby(
        "PublishedOn")["PageCount"].sum()
    totals["TotalPagesRead"] = df[
        df["ReadStatus"] == "FINISHED"].groupby(
            "PublishedOn")["PageCount"].sum()
    totals["TotalPagesRead"] = totals["TotalPagesRead"].fillna(0)
    totals["TotalPagesRead"] = totals["TotalPagesRead"].astype(int)
    for work_type in Settings.WORK_TYPE_SYMBOLS.keys():
        feat_name = work_type.replace(" ", "")
        totals[f"TotalPagesRead_{feat_name}"] = df[
            (df["ReadStatus"] == "FINISHED") &
            (df["Type"] == work_type)
        ].groupby("PublishedOn")["PageCount"].sum()
        totals[f"TotalPagesRead_{feat_name}"] = totals[
            f"TotalPagesRead_{feat_name}"].fillna(0)
        totals[f"TotalPagesRead_{feat_name}"] = totals[
            f"TotalPagesRead_{feat_name}"].astype(int)

    for year in range(totals.index.min(), totals.index.max() + 1):
        if year not in totals.index:
            totals.loc[year] = [0] * len(totals.columns)
    totals = totals.sort_index()

    return totals


def plot_data(data: pd.DataFrame) -> None:
    fig = plt.figure(figsize=(7, 5))
    gs = fig.add_gridspec(ncols=1, nrows=1, hspace=0, wspace=0)
    ax = fig.add_subplot(gs[0, 0])

    fig.patch.set_facecolor(Colors.LIGHTGRAY)
    ax.set_facecolor(Colors.LIGHTGRAY)
    ax.set_xlim(data.index.min() - 1, data.index.max() + 1)
    ax.set_ylim(0, data["TotalPagesPublished"].max() + 200)
    ax.set_xlabel("YEAR", fontsize=8,
                  fontname=Settings.FONTNAME, color=Colors.DARKGRAY)
    ax.set_ylabel("PAGES", rotation=0, fontsize=8,
                  fontname=Settings.FONTNAME, color=Colors.DARKGRAY)
    ax.yaxis.set_label_coords(0, 1.02)
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

    bottom = 0
    for work_type in Settings.WORK_TYPE_SYMBOLS.keys():
        feat_name = work_type.replace(" ", "")
        color = Settings.WORK_TYPE_COLOR_MAPPING[work_type]
        ax.bar(
            data.index, data[f"TotalPagesRead_{feat_name}"], 1,
            bottom=bottom, color=color, label=work_type)
        bottom += data[f"TotalPagesRead_{feat_name}"]
    ax.step(data.index, data["TotalPagesPublished"], where='mid',
            color=Colors.DARKGRAY, label="Pages Published", linewidth=1)

    plt.text(
        -0.05, 1.18, va="bottom", ha="left", fontsize=14,
        transform=ax.transAxes, color=Colors.DARKGRAY,
        s=f"{data.author_name} Bibliography History",
        fontname=Settings.FONTNAME, weight=800)
    plt.text(
        -0.05, 1.17, va="top", ha="left", fontsize=10,
        transform=ax.transAxes, color=Colors.DARKGRAY,
        s="This shows the total amount of pages published by year (black line)"
          " and the total pages I've read,\ncoloured by work type.",
        fontname=Settings.FONTNAME)
    plt.text(
        -0.04, -0.16, s="Source:", fontweight="bold", fontsize=8,
        transform=ax.transAxes, color=Colors.DARKGRAY,
        fontname=Settings.FONTNAME, va="bottom", ha="left")
    plt.text(
        0.04, -0.16, s=" https://github.com/ffiza/reading-stats",
        fontsize=8, transform=ax.transAxes, color=Colors.DARKGRAY,
        fontname=Settings.FONTNAME, va="bottom", ha="left")

    ax.legend(loc="upper right", fontsize=8, frameon=False, ncol=1,)

    fig.tight_layout()
    ax.set_position((0.05, 0.12, 0.9, 0.7))
    filename = data.author_name.replace(".", "").replace(" ", "_").lower() \
        + "_bibliography.png"
    fig.savefig(f"images/{filename}", dpi=1000)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--author", help="Author name.")
    args = parser.parse_args()

    df = load_data(args.author)
    totals = transform_data(df)
    totals.author_name = args.author
    plot_data(totals)
