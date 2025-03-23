from utils.user_stats import UserStats
import sys

def load_user_productions_content(user_productions):
    if isinstance(user_productions, str):
        content = []
        with open(user_productions, "r") as file:
            content = [line.rstrip() for line in file]
    elif isinstance(user_productions, list):
        content = user_productions
    else:
        raise ValueError("user_productions must be either a string (file path) or a list of strings.")
    return content

def generate_user_report(user_productions, output_pdf):
    """
    Generates a user report based on daily statistics from the SayBanana app.

    Parameters:
    - user_productions (str | list): Path to a .txt file with daily user stats, or directly the list of stats.
    - output_pdf (str): File path where the generated PDF report will be saved.
    """
    content = load_user_productions_content(user_productions)
    if content:
        user_stats = UserStats(content)
        user_stats.create_pdf_report(output_pdf)
        print(f"...generating {output_pdf}")
    else:
        print("Empty user_productions.txt")

if __name__ == "__main__":

    generate_user_report("test/user_productions.txt", "output/test1.pdf")


