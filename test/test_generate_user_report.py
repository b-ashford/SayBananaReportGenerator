
from SBReportGenerator import generate_user_report



files = ["test/user_productions_example.txt"]
outputs = ["output/test1.pdf", "output/test2.pdf"]
for file, output in zip(files, outputs):
    generate_user_report(file, output)
