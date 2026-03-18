import matplotlib.pyplot as plt
import matplotlib.figure
import pandas as pd

from reading_stats.utils.colors import Colors
from reading_stats.utils.styles import Styles


def apply_base_style(fig: matplotlib.figure.Figure, ax: plt.Axes) -> None:
    fig.patch.set_facecolor(Colors.LIGHTGRAY)
    ax.set_facecolor(Colors.LIGHTGRAY)

    ax.tick_params(axis="y", which="both", length=0, labelsize=9)
    ax.tick_params(axis="x", length=0, labelsize=9)
    ax.grid(
        visible=True, color=Colors.DARKGRAY, alpha=0.3,
        linestyle=(0, (5, 4)), linewidth=0.5,
    )
    for label in ax.get_yticklabels() + ax.get_xticklabels():
        label.set_fontname(Styles.FONTNAME)
    for spine in ["right", "top"]:
        ax.spines[spine].set_visible(False)


def add_titles(ax: plt.Axes, title: str, subtitle: str,) -> None:
    plt.text(
        -0.05, 1.18, va="bottom", ha="left", fontsize=14,
        transform=ax.transAxes, color=Colors.DARKGRAY,
        s=title, fontname=Styles.FONTNAME, weight=800,
    )
    plt.text(
        -0.05, 1.17, va="top", ha="left", fontsize=10,
        transform=ax.transAxes, color=Colors.DARKGRAY,
        s=subtitle, fontname=Styles.FONTNAME,
    )


def add_source(ax: plt.Axes, source: str,
               source_label_xanchor: float = -0.04,
               source_text_xanchor: float = 0.05) -> None:
    plt.text(
        source_label_xanchor, -0.16, s="Source:", fontweight="bold",
        fontsize=8,
        transform=ax.transAxes, color=Colors.DARKGRAY,
        fontname=Styles.FONTNAME, va="bottom", ha="left",
    )
    plt.text(
        source_text_xanchor, -0.16, s=source, fontsize=8,
        transform=ax.transAxes, color=Colors.DARKGRAY,
        fontname=Styles.FONTNAME, va="bottom", ha="left",
    )


def highlight_points(
        ax: plt.Axes,
        df: pd.DataFrame,
        labels: list[str],
        label_col: str,
        x_col: str,
        y_col: str,
        annotation_x: float,
        ) -> None:
    for label in labels:
        subset = df[df[label_col] == label]
        if subset.empty:
            continue
        ax.scatter(
            subset[x_col], subset[y_col],
            s=10, label=label, zorder=20, linewidth=0.5,
            facecolor="none", edgecolor=Colors.DARKGRAY,
        )
        ax.annotate(
            label,
            (subset[x_col].values[0], subset[y_col].values[0]),
            textcoords="data",
            xytext=(annotation_x, subset[y_col].values[0]),
            ha="left", va="center",
            arrowprops=dict(arrowstyle="-", lw=0.5),
            fontsize=8, fontname=Styles.FONTNAME,
            color=Colors.DARKGRAY, zorder=25,
        )
