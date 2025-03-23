# SayBanana App User Report Generator

Generates PDF reports from user statistics of the SayBanana children's speech therapy app.

## Installation
   ```bash
   git clone git@github.com:b-ashford/SayBananaReportGenerator.git
   cd SayBananaReportGenerator
   pip install --upgrade pip
   pip install .
   ```

## Usage

To create a user report, input the path to a `user_productions.txt` file and specify the output PDF file name.

```python
import os
from SBReportGenerator import generate_user_report, user_productions_example_file

output_pdf_path = os.path.expanduser("~/Desktop/example_report.pdf")
input_user_productions_path = user_productions_example_file
generate_user_report(input_user_productions_path, output_pdf_path)

```
## User Productions File Format

The `user_productions.txt` should follow this format:
```
username_email@email.com,Word,Score,Timestamp
```

For example
```
username_email@email.com,Fishing,0,22-03-2024 10:51:07
username_email@email.com,Fishing,1,22-03-2024 10:51:31
...
```

## Output Example Report
<p align="center">
  <img src="assets/example_report.png" alt="Example Image" width="700" style="border: 2px solid black;">
</p>


