import matplotlib.pyplot as plt
import matplotlib.figure
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
