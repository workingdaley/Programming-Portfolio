"""Djesse Jackson
Student id: 2712207
Linux id: dejackso
Project 3"""

# This program is a parser that looks through time log files and outputs the amount of time that passed between the start and end times recorded in the file

import sys

def main():

    # Ensuring that time log file is given in command line
    if len(sys.argv) < 2:
        print("Error - No log file given")
    else:
        # Opening time log file
        time_log = open(sys.argv[1], "r")
        name = time_log.name
        if "TimeLog" in name:
            name = name[7:-4]
        # Ensuring that "time log:" is in the file
        if findTimeLog(time_log) == True:
            # Setting line count and time to 0
            count = 0
            time = [0, 0]
            readline(time_log, count, time, name)
        time_log.close()

# A funciton to find the hard-coded "time log:"
def findTimeLog(time_log):
    nextChar = time_log.read(1)
    # if first character does not start with t, keep looking until you find t
    while nextChar.lower() != 't':
        nextChar = time_log.read(1)
        # if you reach the end of the file without finding the time log, this file is not usable
        if nextChar == "":
            print("No time log found, ending program")
            return False
    # If t is found, next 8 characters make up "time log:" so add next 8 characters to sequence
    sequence = nextChar
    sequence += time_log.read(8)
    # Check to ensure that sequence is time log
    if sequence.lower() == "time log:":
        return True
    else:
        findTimeLog(time_log)

# A function to read each line of the text file to find times
def readline(time_log, line_count, time, name):
    line_count += 1
    line = time_log.readline()
    split_line = line.split()
    for i, item in enumerate(split_line):
        # If item is date, skip (date has a colon and I don't want it to be confused for a time)
        if "/" in item:
            continue
        # If item is time in correct format, get time period
        elif ":" in item and "-" in item:
            hours, minutes = GetTimePeriod(item, line_count)
            if hours == -1:
                return -1
            time[0] += hours
            time[1] += minutes
            break
        # If item is individual time (applies to first time), format second time to format for time period function and continue
        elif ":" in item:
            split_line[i+2] = item + "-" + split_line[i+2]
    # Read next line as long as EOF has not been reached
    if line != "":
        readline(time_log, line_count, time, name)
    else:
        # Add 1 hour for every 60 minutes in overall time to hours and make minutes remainder, then print
        time[0] += time[1] // 60
        time[1] %= 60
        print(name + ": " + str(time[0]) + " hours " + str(time[1]) + " minutes")
    

def GetTimeValue(time):
    # Isolate am or pm from time then split time by ":"
    am_pm = time[-2:]
    time = time[:-2]
    split_time = time.split(":")
    hours = int(split_time[0])
    minutes = int(split_time[1])
    # Ensure hours are between 1 and 12 and minutes are between 0 and 59
    if hours < 1 or hours > 12:
        return -1, -1
    if minutes < 0 or minutes > 59:
        return -1, -1
    # Convert hours to 24 hour format for math purposes
    if am_pm.lower() == "am" and hours == 12:
        hours = 0
    elif am_pm.lower() == "pm" and hours < 12:
        hours += 12
    return hours, minutes

def GetTimePeriod(time_period, line_count):
    # Separate times by "-" and get start and end time values
    times = time_period.split("-")
    start_hour, start_minutes = GetTimeValue(times[0])
    end_hour, end_minutes = GetTimeValue(times[1])

    # If time value gave error value, print error code and end program
    if start_hour == -1 or end_hour == -1:
        print("Error in line " + str(line_count) +": Cannot parse line")
        return -1, -1
    # Ensure that end - start is positive, or add 24 hours or 60 minutes to final answer
    else:
        hours = end_hour - start_hour
        if hours < 0:
            hours += 24
        if end_minutes - start_minutes < 0:
            minutes = end_minutes - start_minutes + 60
            hours -= 1
        else:
            minutes = end_minutes - start_minutes
    return hours, minutes

if __name__ == "__main__":
    main()