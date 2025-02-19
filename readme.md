# SayBanana App User Report Generator

Generates PDF reports from user statistics of the SayBanana children's speech therapy app.

## Usage

To create a user report, input the path to "user_productions.txt" and specify the output PDF file name.

```python
from SayBanana_stats import generate_user_report

file_path = "test/user_productions.txt"
output_path = "output/test.pdf"
generate_user_report(file_path, output_path)
```
## File Format

The "user_productions.txt" should follow this format:
```
username_email@email.com,Word,Score,Timestamp
```

For example
```
username_email@email.com,Fishing,0,22-03-2024 10:51:07
username_email@email.com,Fishing,1,22-03-2024 10:51:31
...
```

## Example Report
<p align="center">
  <img src="assets/example_report.png" alt="Example Image" width="700" style="border: 2px solid black;">
</p>


