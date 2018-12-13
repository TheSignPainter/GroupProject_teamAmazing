import re


def check_date(string): # Check whether a string is given form "YYYY-MM-DD".
    if re.match(r"^\d{4}-\d{2}-\d{2}$",string):
        return True
    else:
        return False
