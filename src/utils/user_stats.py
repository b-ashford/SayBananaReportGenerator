import sys
from utils.table_builder import make_word_table
import copy
from utils.plotting import plot_percentage_of_words_accuracy_bar_chart, save_png
from utils.user_dates import (
    format_date,
    sort_dates,
    get_day_name,
    generate_date_array,
    get_from_date,
)
from datetime import datetime
from utils.pdf_maker import init_pdf, set_title, draw_ruler, set_image, set_text


CORRECT = "1"
INCORRECT = "0"
SKIPPED = "2"

daily_stat_template = {
    "words_correct": 0,
    "words_incorrect": 0,
    "words_skipped": 0,
    "words_total": 0,
    "words_accuracy_pc": 0.0,
    "by_word": {},
}
word_daily_stat_template = {
    "correct": 0,
    "incorrect": 0,
    "skipped": 0,
    "word_accuracy_pc": 0.0,
}


class UserStats:
    def __init__(self, up_contents):
        self.up_contents = [element for element in up_contents if element.strip()]
        self.uid = self.get_uid()
        self.daily_data = self.get_daily_data()
        self.daily_stats = self.init_daily_stats()
        self.get_daily_stats()

    def get_uid(self):
        """
        Gets the child's uid (format: username_email) from the user_production
        logs. Every line of the log contains the uid. If more than one is detected
        then something has gone wrong when the user_productions was made.
        """
        uid = set()
        for line in self.up_contents:
            if line:
                uid.add(line.split(",")[0].strip())
        if len(uid) != 1:
            print("ERROR: Multiple UIDs found:", uid, file=sys.stderr)
            sys.exit(1)
        return list(uid)[0]

    def get_daily_data(self):
        """
        Create an object of the user_productions content based on date and then time.
        Format: obj[date][time] = (word, grade)
        """
        daily_data = {}
        for line in self.up_contents:
            _, word, grade, date_time = line.split(",")
            date, time = date_time.split(" ")
            date = format_date(date)
            if date not in daily_data:
                daily_data[date] = {}
            daily_data[date][time] = (word, grade)
        return daily_data

    def init_daily_stats(self):
        daily_stats = {}
        for day in self.daily_data.keys():
            if day not in daily_stats.keys():
                daily_stats[day] = copy.deepcopy(daily_stat_template)

        return daily_stats

    def get_daily_stats(self):
        for day in self.get_ordered_dates():
            self.get_daily_word_stats(day)

    def get_daily_word_stats(self, day):
        total, total_correct, total_incorrect, total_skipped = 0, 0, 0, 0

        for _, (word, grade) in self.daily_data[day].items():
            if word not in self.daily_stats[day]["by_word"].keys():
                self.daily_stats[day]["by_word"][word] = copy.deepcopy(
                    word_daily_stat_template
                )
            if grade == CORRECT:
                total_correct += 1
                total += 1
                self.daily_stats[day]["by_word"][word]["correct"] += 1
            elif grade == INCORRECT:
                total_incorrect += 1
                total += 1
                self.daily_stats[day]["by_word"][word]["incorrect"] += 1
            elif grade == SKIPPED:
                total_skipped += 1
                self.daily_stats[day]["by_word"][word]["skipped"] += 1

        self.daily_stats[day]["words_correct"] = total_correct
        self.daily_stats[day]["words_incorrect"] = total_incorrect
        self.daily_stats[day]["words_skipped"] = total_skipped
        self.daily_stats[day]["words_total"] = total
        self.daily_stats[day]["words_accuracy_pc"] = (
            round(total_correct / total, 2) * 100
        )
        # Get the by word pc
        for word_stats in self.daily_stats[day]["by_word"].values():
            correct = word_stats["correct"]
            incorrect = word_stats["incorrect"]
            word_stats["word_accuracy_pc"] = (
                round(correct / (correct + incorrect), 2) * 100
            )

    def get_daily_stat_str(self):
        output = f"{str(self.uid)} STATS:\n"
        for date, date_info in self.daily_stats.items():
            output += date + "\n"
            for k, v in date_info.items():
                output += f"\t{k} = {v}\n"
        return output

    def __str__(self):
        output = f"{str(self.uid)} DATA:\n"
        for date, date_info in self.daily_data.items():
            output += f"{date}\n"
            for time, time_info in date_info.items():
                output += f"    {time} {time_info}\n"
        return output

    def get_ordered_dates(self, reversed=False):
        dates = self.daily_data.keys()
        ordered_dates = sort_dates(dates)
        if reversed:
            return ordered_dates[::-1]
        return ordered_dates

    def get_all_words_list(self):
        words = set()
        for _, info in self.daily_data.items():
            for _, (word, _) in info.items():
                words.add(word)
        return sorted(words)

    def daily_words_attempt_history(self):
        output = [("date", "word", "correct", "incorrect", "skipped")]
        for date, info in self.daily_stats.items():
            for word, stats in info["by_word"].items():
                output.append(
                    (date, word, stats["correct"], stats["incorrect"], stats["skipped"])
                )
        return output

    def daily_word_attempt_history(self, target_word):
        history = self.daily_words_attempt_history()
        word_history = []
        for date, word, correct, incorrect, skipped in history:
            if word == target_word:
                word_history.append((date, word, correct, incorrect, skipped))
        return word_history

    def daily_word_attempts_str(self):
        history = self.daily_words_attempt_history()
        output = ""
        for date in self.get_ordered_dates(reversed=True):
            output += f"{get_day_name(date)} {date}:\n"
            for word, grades in self.daily_stats[date]["by_word"].items():
                output += f"\t{word},{grades['correct']}, {grades['incorrect']}, {grades['skipped']}, {grades['word_accuracy_pc']}\n"

        return output

    def create_table(self, save_path, from_today=True, num_days=14):
        date_list = self.get_ordered_dates(reversed=False)
        from_date = get_from_date(date_list=date_list, from_today=from_today)
        dates_columns = generate_date_array(from_date=from_date, num_days=num_days)
        formatted_dates = [
            datetime.strptime(date, "%d-%m-%Y").strftime("%d/%m/%y")
            for date in dates_columns
        ]
        data = {}
        for date, f_date in zip(dates_columns, formatted_dates):
            if date in date_list:
                data[f_date] = {}
                for word, grades in self.daily_stats[date]["by_word"].items():
                    data[f_date][word] = (
                        grades["correct"],
                        grades["incorrect"],
                        grades["skipped"],
                        grades["word_accuracy_pc"],
                    )
            else:  # fill in dates user wasnt active with empty obj
                data[f_date] = {}
        fig = make_word_table(data)
        save_png(fig, save_path)
        return save_path

    def get_percentage_of_word_accuracy_img(self, from_today=True):
        fig = plot_percentage_of_words_accuracy_bar_chart(
            self.daily_stats, from_today=from_today
        )
        figure1_path = "images/figure1.png"
        png = save_png(fig, figure1_path)
        return png

    def create_pdf_report(self, filename):
        pdf = init_pdf(filename=filename)
        set_title(pdf, height=730)
        set_image(pdf=pdf, x=50, y=725, max_height=40, image="images/say66_logo.png")

        figure = self.get_percentage_of_word_accuracy_img(from_today=False)
        table = self.create_table(from_today=False, save_path="images/table.png")
        set_image(pdf=pdf, x=40, y=420, image=figure, max_width=520)
        set_image(pdf=pdf, x=40, y=200, image=table, max_width=570)
        text = f"Player User ID:   {self.uid}"
        set_text(pdf=pdf, text=text, x=50, y=650)
        text = f"Date Generated:  {get_from_date(from_today=True)}"
        set_text(pdf=pdf, text=text, x=50, y=675)

        # draw_ruler(pdf)
        pdf.save()
        return filename
