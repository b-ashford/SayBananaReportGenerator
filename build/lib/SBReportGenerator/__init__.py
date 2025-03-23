from importlib.resources import files
from .report_core import generate_user_report


user_productions_example_file = str(
    files("SBReportGenerator").joinpath("data", "user_productions_example.txt")
)

__all__ = ["generate_user_report", "user_productions_example_file"]
