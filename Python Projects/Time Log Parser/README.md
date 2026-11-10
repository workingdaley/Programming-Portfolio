# Time Log Parser (Python)

A command-line program that parses time log files and calculates total elapsed time across one or more logged time periods.

## What It Does

Given a text file containing a `time log:` header and a series of logged time periods (e.g., `9:00am-5:00pm`), the program:

1. **Locates the time log header** by scanning the file character by character until it finds the literal marker `time log:`.
2. **Parses each line**, identifying date entries (skipped) versus time period entries (identified by the presence of both `:` and `-`).
3. **Converts 12-hour AM/PM times to 24-hour format** for accurate arithmetic.
4. **Calculates elapsed time per entry**, correctly handling cases where an end time is numerically earlier than the start time (e.g., crossing midnight) by adjusting for a full 24-hour cycle, and handling minute borrowing when subtracting minutes.
5. **Accumulates totals** across every time period in the file and normalizes any minute overflow (60+ minutes) into whole hours before printing the final result.

## Usage

```
python tl_parser_2712207.py <log_file>.txt
```

Outputs the total elapsed time in the format: `<name>: X hours Y minutes`

## Skills Demonstrated

- Recursive file parsing (line-by-line reading via recursion)
- String parsing and pattern identification
- Time arithmetic, including 12-hour to 24-hour conversion and day-rollover handling
- Input validation and error handling for malformed entries
