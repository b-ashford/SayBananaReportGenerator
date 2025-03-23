import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from utils.plotting import (
    axis_font,
    title_font,
    set_tick_font,
    save_png,
    tick_font,
    WRONG_COLOUR,
    CORRECT_COLOUR,
)

LIGHTGREY = "#F0F0F0"


# Function to format annotations
def format_annotation(val):
    if isinstance(val, tuple):
        return f"{val[0]}✔ {val[1]}✘"
    return str(val)


def make_word_table(data):
    # Define annotation function
    def format_annotation(val):
        if isinstance(val, tuple):
            return f"{val[0]}✔ {val[1]}✘"
        return str(val)

    # DataFrame creation and data manipulation
    df_raw = pd.DataFrame(data)

    # Extracting the first and fourth elements for values and intensity
    df_values = df_raw.apply(
        lambda col: col.apply(lambda x: x[0] if isinstance(x, tuple) else x)
    )
    df_intensity = df_raw.apply(
        lambda col: col.apply(lambda x: x[3] if isinstance(x, tuple) else x)
    )
    annot = df_raw.apply(lambda col: col.apply(format_annotation))

    # Color map creation
    cmap = mcolors.LinearSegmentedColormap.from_list("", [WRONG_COLOUR, CORRECT_COLOUR])

    # Create a figure and a set of subplots
    # fig, ax = plt.subplots(figsize=(12, len(df_intensity) * 0.5))
    fig, ax = plt.subplots(figsize=(15, 5))

    # Heatmap plotting with grid lines
    sns_heatmap = sns.heatmap(
        df_intensity,
        annot=annot,
        annot_kws={"fontsize": 11},
        fmt="s",
        cmap=cmap,
        vmin=0,
        vmax=100,
        linewidths=0.5,
        linecolor=LIGHTGREY,
        ax=ax,  # Use the axes object created above
    )
    cbar = sns_heatmap.collections[0].colorbar
    cbar.set_label("Correct Percentage (0-100)%", size=12)

    plt.xticks(rotation=45)
    set_tick_font(ax, tick_font)

    plt.title("Accuracy by Word", fontdict=title_font, y=1.05)
    plt.xlabel("Last 14 Days from Most Recent Activity", fontdict=axis_font)
    plt.ylabel("Words", fontdict=axis_font)
    plt.subplots_adjust(bottom=0.2)
    plt.yticks(rotation=0)  # This will make the y-axis labels horizontal
    plt.tight_layout()

    return fig


if __name__ == "__main__":

    data = {
        "09-03-2024": {
            "Pin": (4, 0, 0, 100.0),
            "Pop": (4, 0, 0, 100.0),
            "Cat": (2, 0, 0, 100.0),
            "Peep": (8, 0, 0, 100.0),
            "Pig": (0, 6, 0, 0.0),
            "Pen": (2, 0, 0, 100.0),
            "Pear": (4, 2, 0, 67.0),
        },
        "10-03-2024": {
            "Pen": (2, 0, 0, 100.0),
            "Cat": (4, 0, 0, 100.0),
            "Peep": (4, 0, 0, 100.0),
            "Pig": (4, 4, 0, 50.0),
            "Case": (4, 4, 0, 50.0),
            "Baby": (2, 0, 0, 100.0),
            "Back": (2, 0, 0, 100.0),
            "Pin": (0, 4, 0, 0.0),
        },
        "12-03-2024": {
            "Pen": (2, 0, 0, 100.0),
            "Cat": (4, 0, 0, 100.0),
            "Peep": (4, 0, 0, 100.0),
            "Pig": (4, 0, 0, 100.0),
            "Case": (4, 4, 0, 50.0),
            "Baby": (2, 0, 0, 100.0),
            "Back": (2, 0, 0, 100.0),
            "Pin": (0, 4, 0, 0.0),
        },
        "08-03-2024": {
            "Pen": (2, 0, 0, 100.0),
            "Cat": (4, 0, 0, 100.0),
            "Peep": (4, 0, 0, 100.0),
            "Pig": (4, 4, 0, 50.0),
            "Case": (4, 4, 0, 50.0),
            "Baby": (2, 0, 0, 100.0),
            "Back": (2, 0, 0, 100.0),
            "Pin": (0, 4, 0, 0.0),
        },
        "09-03-2024": {
            "Pen": (2, 0, 0, 100.0),
            "Cat": (4, 0, 0, 100.0),
            "Pig": (4, 4, 0, 50.0),
            "Case": (4, 4, 0, 50.0),
            "Baby": (2, 0, 0, 100.0),
            "Back": (2, 0, 0, 100.0),
            "Pin": (0, 4, 0, 0.0),
        },
        "10-03-2024": {
            "Pen": (2, 0, 0, 100.0),
            "Cat": (4, 0, 0, 100.0),
            "Peep": (4, 0, 0, 100.0),
            "Pig": (4, 4, 0, 50.0),
            "Case": (4, 4, 0, 50.0),
            "Baby": (2, 0, 0, 100.0),
            "Back": (2, 0, 0, 100.0),
            "Pin": (0, 4, 0, 0.0),
        },
        "12-03-2024": {},
    }
    fig = make_word_table(data)
    save_png(fig, "test/table.png")
