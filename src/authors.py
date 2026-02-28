import sqlite3
import numpy as np
import pandas as pd
from typing import List
import matplotlib.pyplot as plt

from colors import Colors
from settings import Settings


def export_top_authors(amount_to_export: int = 50) -> None:
    df = pd.read_csv("data/processed/read_history.csv")
    df = df[df["ReadStatus"].isin(["FINISHED", "NOT FINISHED"])]
    df["WeightedScore"] = df["ReadScore"] * df["PageCount"]

    avg_scores = (
        df.groupby(["AuthorID", "AuthorName"])
        .agg(WeightedReadScore=("WeightedScore", "sum"),
             TotalPages=("PageCount", "sum")))

    avg_scores["WeightedReadScore"] = (
        avg_scores["WeightedReadScore"] / avg_scores["TotalPages"])

    avg_scores = (avg_scores.reset_index().sort_values("WeightedReadScore",
                                                       ascending=False))

    avg_scores.to_csv("data/results/top_authors.csv", index=False)


def plot_most_read_authors(df: pd.DataFrame, n_authors: int = 20) -> None:
    df = df.sort_values("TotalPages", ascending=False).reset_index(
        drop=True).head(n_authors).sort_values("TotalPages", ascending=True)
    max_pages = df["TotalPages"].max()

    fig = plt.figure(figsize=(7, 7))
    gs = fig.add_gridspec(ncols=1, nrows=1, hspace=0, wspace=0)
    ax = fig.add_subplot(gs[0, 0])

    fig.patch.set_facecolor("#e9e9e9")
    ax.set_facecolor("#e9e9e9")

    ax.set_xlim(0, (int(max_pages / 1_000) + 3) * 1_000)
    ax.set_xticks([])
    ax.tick_params(axis='y', length=0, labelsize=10)

    for spine in ["right", "left", "bottom", "top"]:
        ax.spines[spine].set_visible(False)

    plt.text(
        -0.3, 1.01, va="bottom", ha="left", fontsize=14,
        transform=ax.transAxes, color=Colors.DARKGRAY,
        s="Top read authors: Which are the authors I've read the most?",
        fontname=Settings.FONTNAME, weight=800)
    plt.text(
        -0.3, 0.98, va="bottom", ha="left", fontsize=10,
        transform=ax.transAxes, color=Colors.DARKGRAY,
        s="This shows the amount of pages I've read for each author.",
        fontname=Settings.FONTNAME)
    plt.text(
        -0.3, -0.01, s="Source:", fontweight="bold", fontsize=8,
        transform=ax.transAxes, color=Colors.DARKGRAY,
        fontname=Settings.FONTNAME, va="bottom", ha="left")
    plt.text(
        -0.22, -0.01, s=" https://github.com/ffiza/reading-stats",
        fontsize=8, transform=ax.transAxes, color=Colors.DARKGRAY,
        fontname=Settings.FONTNAME, va="bottom", ha="left")
    ax.barh(df["AuthorName"], df["TotalPages"], label="Total Pages",
            color="#88769e")
    for label in ax.get_yticklabels():
        label.set_fontname(Settings.FONTNAME)

    for i in range(n_authors):
        add_text = " pages read" if i == n_authors - 1 else ""
        pages_txt: str = str(df.loc[i]["TotalPages"]) + add_text
        total_pages = df.loc[i]["TotalPages"]
        ax.text(x=total_pages + 200, y=n_authors - i - 1, s=pages_txt,
                style='italic', fontname=Settings.FONTNAME,
                ha="left", va="center", color=Colors.DARKGRAY, size=10)

    fig.tight_layout()
    fig.savefig("images/most_read_authors.png", dpi=1000)


def plot_top_rated_authors(df: pd.DataFrame,
                           n_authors: int = 20,
                           min_page_count: int = 500) -> None:
    df = df[df["TotalPages"] >= min_page_count]
    df = df.sort_values("WeightedReadScore", ascending=False).reset_index(
        drop=True).head(n_authors).sort_values("WeightedReadScore",
                                               ascending=True)

    fig = plt.figure(figsize=(7, 7))
    gs = fig.add_gridspec(ncols=1, nrows=1, hspace=0, wspace=0)
    ax = fig.add_subplot(gs[0, 0])

    fig.patch.set_facecolor("#e9e9e9")
    ax.set_facecolor("#e9e9e9")

    ax.set_xlim(0, 5)
    ax.set_xticks([])
    ax.tick_params(axis='y', length=0, labelsize=10)

    for spine in ["right", "left", "bottom", "top"]:
        ax.spines[spine].set_visible(False)

    plt.text(
        -0.3, 1.01, va="bottom", ha="left", fontsize=14,
        transform=ax.transAxes, color=Colors.DARKGRAY,
        s="Highest rated authors: Which are the authors I like the most?",
        fontname=Settings.FONTNAME, weight=800)
    plt.text(
        -0.3, 0.98, va="bottom", ha="left", fontsize=10,
        transform=ax.transAxes, color=Colors.DARKGRAY,
        s="This shows the page-weighted average score of authors with at least"
          f" {min_page_count} pages read.",
        fontname=Settings.FONTNAME)
    plt.text(
        -0.3, -0.01, s="Source:", fontweight="bold", fontsize=8,
        transform=ax.transAxes, color=Colors.DARKGRAY,
        fontname=Settings.FONTNAME, va="bottom", ha="left")
    plt.text(
        -0.22, -0.01, s=" https://github.com/ffiza/reading-stats",
        fontsize=8, transform=ax.transAxes, color=Colors.DARKGRAY,
        fontname=Settings.FONTNAME, va="bottom", ha="left")
    ax.barh(df["AuthorName"], df["WeightedReadScore"], color="#88769e")
    for label in ax.get_yticklabels():
        label.set_fontname(Settings.FONTNAME)

    for i in range(n_authors):
        add_text = " rating score" if i == n_authors - 1 else ""
        score_txt: str = f"{df.loc[i]['WeightedReadScore']:.2f}" + add_text
        score = df.loc[i]["WeightedReadScore"]
        ax.text(x=score + 0.05, y=n_authors - i - 1, s=score_txt,
                style='italic', fontname=Settings.FONTNAME,
                ha="left", va="center", color=Colors.DARKGRAY, size=10)

    fig.tight_layout()
    fig.savefig("images/highest_rated_authors.png", dpi=1000)


if __name__ == "__main__":
    export_top_authors()
    df = pd.read_csv("data/results/top_authors.csv")
    plot_most_read_authors(df)
    plot_top_rated_authors(df, min_page_count=1000)
