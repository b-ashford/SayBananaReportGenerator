import matplotlib.pyplot as plt
from utils.user_dates import generate_date_array, get_from_date
import os

TEAL = "#76E1B5"
PURPLE = "#779BF5"
GREEN = "#A5C654"
GREEN2 = "#B6D360"
RED = "#EB503D"
WRONG_COLOUR = "coral"
CORRECT_COLOUR = TEAL


title_font = {
    "fontsize": 24,
    "fontweight": "bold",
    "color": "k",
    "fontname": "Helvetica",
}
axis_font = {
    "fontsize": 18,
    "fontweight": "normal",
    "color": "k",
    "fontname": "Helvetica",
}
legend_font = {
    "size": 14,
    "weight": "normal",
    "family": "sans-serif",
}
bar_font = {
    "fontsize": 16,
    "fontweight": "normal",
    "color": "k",
    "fontname": "Helvetica",
}
tick_font = {
    "fontsize": 14,
    "fontweight": "normal",
    "color": "k",
    "fontname": "Helvetica",
}


def set_tick_font(ax, fontdict):
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontsize(fontdict.get("fontsize", 10))
        label.set_fontweight(fontdict.get("fontweight", "normal"))
        label.set_color(fontdict.get("color", "black"))
        label.set_family(fontdict.get("family", "sans-serif"))


def build_stacks(active_dates: object, from_today: bool):
    words_correct, words_incorrect = [], []
    date_list = generate_date_array(
        get_from_date(active_dates.keys(), from_today=from_today)
    )
    for date in date_list:
        date_data = active_dates.get(date, {"words_correct": 0, "words_incorrect": 0})
        words_correct.append(date_data["words_correct"])
        words_incorrect.append(date_data["words_incorrect"])
    return date_list, words_correct, words_incorrect


def get_words_pc(words_correct, words_incorrect):
    words_correct_percentage, words_incorrect_percentage = [], []
    for word_correct, word_incorrect in zip(words_correct, words_incorrect):
        total_words = word_correct + word_incorrect
        if total_words > 0:
            correct_pc = round((word_correct / total_words), 2) * 100
            incorrect_pc = round((word_incorrect / total_words), 2) * 100
        else:
            correct_pc = 0
            incorrect_pc = 0

        words_correct_percentage.append(correct_pc)
        words_incorrect_percentage.append(incorrect_pc)
    return words_correct_percentage, words_incorrect_percentage


def format_date_list_for_plotting(date_list):
    formatted_date_list = []
    for date in date_list:
        day, month, year = date.split("-")
        formatted_date_list.append(f"{day}/{month}/{year[2:4]}")
    return formatted_date_list


def plot_percentage_of_words_accuracy_bar_chart(active_dates, from_today=True):
    """
    Plots a stacked bar chart of words correct and incorrect percentages over given dates.

    Args:
    date_list (list): List of date strings.
    words_correct_percentage (list): List of correct word percentages.
    words_in
    """
    date_list, words_correct, words_incorrect = build_stacks(
        active_dates, from_today=from_today
    )
    words_correct_percentage, words_incorrect_percentage = get_words_pc(
        words_correct, words_incorrect
    )

    fig, ax = plt.subplots(figsize=(15, 5))

    bars_correct = ax.bar(
        date_list, words_correct_percentage, label="Words Correct", color=CORRECT_COLOUR
    )
    bars_incorrect = ax.bar(
        date_list,
        words_incorrect_percentage,
        bottom=words_correct_percentage,
        label="Words Incorrect",
        color=WRONG_COLOUR,
    )

    # Add text labels on the bars for raw word counts
    for bar, label in zip(bars_correct, words_correct):
        height = bar.get_height()
        if label != 0:  # Only place text if the bar is not zero
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_y() + height / 2,
                str(label),
                ha="center",
                va="center",
                color="k",
                fontdict=bar_font,
            )

    for bar, label in zip(bars_incorrect, words_incorrect):
        height = bar.get_height()  
        if label != 0:  

            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_y() + height / 2,
                str(label),
                ha="center",
                va="center",
                color="k",
                fontdict=bar_font,
            )
    ax.set_ylim(0, 100)
    ax.set_xlabel("Last 14 Days from Most Recent Activity", fontdict=axis_font)
    ax.set_ylabel("Word Accuracy (%)", fontdict=axis_font)
    ax.set_title("Percentage of Words Accuracy", fontdict=title_font, y=1.05)
    ax.set_xticks(date_list)
    ax.set_xticklabels(format_date_list_for_plotting(date_list), rotation=90)
    set_tick_font(ax, tick_font)
    ax.legend(loc="upper right", bbox_to_anchor=(0.99, 1.3), prop=legend_font)
    plt.subplots_adjust(bottom=0.2)
    fig.autofmt_xdate()
    plt.tight_layout()
    return fig


def save_png(fig, save_path):
    """
    Saves a matplotlib figure as a PNG file.

    Args:
        fig (matplotlib.figure.Figure): The figure to save.
        save_path (str, optional): File path where the image will be saved. Defaults to "temp_image.png".

    Returns:
        str: The file path of the saved PNG image.
    """

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    fig.savefig(save_path, format="png")
    plt.close(fig)

    return save_path


if __name__ == "__main__":
    dates = {
        "01-11-2023": {"words_correct": 2, "words_incorrect": 8},
        "05-11-2023": {"words_correct": 3, "words_incorrect": 7},
        "10-11-2023": {"words_correct": 4, "words_incorrect": 6},
        "15-11-2023": {"words_correct": 5, "words_incorrect": 5},
        "20-11-2023": {"words_correct": 3, "words_incorrect": 2},
        "25-11-2023": {"words_correct": 7, "words_incorrect": 3},
        "30-11-2023": {"words_correct": 8, "words_incorrect": 3},
        "05-12-2023": {"words_correct": 0, "words_incorrect": 1},
        "11-11-2023": {"words_correct": 1, "words_incorrect": 0},
        "2-11-2023": {"words_correct": 9, "words_incorrect": 5},
        "07-12-2023": {"words_correct": 8, "words_incorrect": 0},
    }
    extended_dates = {
        "01-11-2023": {"words_correct": 1, "words_incorrect": 1},
        "05-11-2023": {"words_correct": 9, "words_incorrect": 4},
        "10-11-2023": {"words_correct": 9, "words_incorrect": 3},
        "14-11-2023": {"words_correct": 4, "words_incorrect": 6},
        "16-11-2023": {"words_correct": 7, "words_incorrect": 7},
        "17-11-2023": {"words_correct": 7, "words_incorrect": 1},
        "22-11-2023": {"words_correct": 9, "words_incorrect": 4},
        "23-11-2023": {"words_correct": 3, "words_incorrect": 8},
        "28-11-2023": {"words_correct": 2, "words_incorrect": 8},
        "30-11-2023": {"words_correct": 5, "words_incorrect": 0},
        "01-12-2023": {"words_correct": 2, "words_incorrect": 7},
        "06-12-2023": {"words_correct": 8, "words_incorrect": 8},
        "09-12-2023": {"words_correct": 5, "words_incorrect": 4},
        "11-12-2023": {"words_correct": 9, "words_incorrect": 4},
        "14-12-2023": {"words_correct": 8, "words_incorrect": 0},
        "18-12-2023": {"words_correct": 0, "words_incorrect": 1},
        "22-12-2023": {"words_correct": 5, "words_incorrect": 3},
        "27-12-2023": {"words_correct": 5, "words_incorrect": 5},
        "28-12-2023": {"words_correct": 6, "words_incorrect": 1},
        "31-12-2023": {"words_correct": 9, "words_incorrect": 8},
    }

    dense_dates = {
        "01-12-2023": {"words_correct": 0, "words_incorrect": 7},
        "02-12-2023": {"words_correct": 4, "words_incorrect": 4},
        "03-12-2023": {"words_correct": 4, "words_incorrect": 8},
        "04-12-2023": {"words_correct": 9, "words_incorrect": 4},
        "05-12-2023": {"words_correct": 9, "words_incorrect": 3},
        "06-12-2023": {"words_correct": 10, "words_incorrect": 0},
        "17-11-2023": {"words_correct": 1, "words_incorrect": 5},
        "18-11-2023": {"words_correct": 0, "words_incorrect": 9},
        "19-11-2023": {"words_correct": 10, "words_incorrect": 0},
        "20-11-2023": {"words_correct": 7, "words_incorrect": 2},
        "21-11-2023": {"words_correct": 8, "words_incorrect": 5},
        "22-11-2023": {"words_correct": 1, "words_incorrect": 8},
        "23-11-2023": {"words_correct": 4, "words_incorrect": 8},
        "24-11-2023": {"words_correct": 8, "words_incorrect": 4},
        "25-11-2023": {"words_correct": 10, "words_incorrect": 0},
    }

    plot_percentage_of_words_accuracy_bar_chart(dense_dates, from_today=True)
