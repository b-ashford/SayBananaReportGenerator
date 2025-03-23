from datetime import datetime, timedelta

TODAY_STR = datetime.today().strftime("%d-%m-%y")
TODAY_DATETIME = datetime.today().date()


def generate_date_array(from_date, num_days=14):
    """
    Generates a list of dates from a given start date, spanning a specified number of days.

    Parameters:
    from_date (str): The start date from which to generate the date array in 'DD-MM-YYYY' format.
    num_days (int): Number of days to generate dates for, including the start date.

    Returns:
    list: A list of date strings in 'DD-MM-YYYY' format.
    """
    # Parse the string to a datetime object
    date_format = "%d-%m-%Y"
    date = datetime.strptime(from_date, date_format)

    date_list = []
    for _ in range(num_days):
        date_list.append(date.strftime("%d-%m-%Y"))
        date = date - timedelta(days=1)
    date_list.reverse()
    return date_list


def format_date(date_str):
    """
    Parses a date string in various formats and converts it to 'dd-mm-yyyy', adding leading zeros where necessary.

    Parameters:
    date_str (str): The date string to be formatted.

    Returns:
    str: The formatted date string in 'dd-mm-yyyy' format, or an error message if parsing fails.
    """
    # Define possible date formats
    date_formats = ["%d-%m-%Y", "%d/%m/%Y", "%d-%m-%y", "%d/%m/%y"]

    for fmt in date_formats:
        try:
            # Try to parse the date with the current format
            parsed_date = datetime.strptime(date_str, fmt)
            # Return the date in 'dd-mm-yyyy' format
            return parsed_date.strftime("%d-%m-%Y")
        except ValueError:
            # If parsing fails, try the next format
            continue

    return "Invalid date format"


def format_dates(dates):
    formatted_dates = []
    for date in dates:
        formatted_dates.append(format_date(date))
    return formatted_dates


def get_from_date(date_list=None, from_today=False):
    if from_today or date_list is None:
        return datetime.today().strftime("%d-%m-%Y")

    # else use the most recent date in the list
    parsed_dates = [datetime.strptime(date, "%d-%m-%Y") for date in date_list]
    most_recent_date = max(parsed_dates)
    return most_recent_date.strftime("%d-%m-%Y")


def sort_dates(dates):
    dates = [datetime.strptime(date, "%d-%m-%Y") for date in dates]
    dates.sort()
    sorted_dates = [datetime.strftime(date, "%d-%m-%Y") for date in dates]
    return sorted_dates


def get_day_name(date):
    # Assuming the input date format is 'dd-mm-yyyy'
    date_obj = datetime.strptime(date, "%d-%m-%Y")
    day_name = date_obj.strftime("%A")
    return day_name


def get_most_recent_date(date_list):
    formatted_dates = format_dates(date_list)
    dates = [datetime.strptime(date_str, "%d-%m-%Y") for date_str in formatted_dates]
    if dates:
        most_recent_date = max(dates)
        return most_recent_date.strftime("%d-%m-%Y")
    else:
        return None


def is_today(date):
    if isinstance(date, str):
        date = datetime.strptime(date, "%d-%m-%Y").date()
    elif isinstance(date, datetime):
        date = date.date()
    return TODAY_DATETIME == date
