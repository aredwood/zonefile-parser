import re
from typing import List
def remove_comments(line:str):
    for index,character in enumerate(line):
        if character == ";" and not is_in_quote(line,index):
            line = line[:index]
            break
    return line

def is_in_quote(text:str,index:int):
    return text[:index].count("\"") % 2 == 1

# TODO remove
def remove_trailing_spaces(line:str):
    return line

# TODO remove
def collapse_brackets(text:str):
    return text

def is_integer(n):
    try:
        int(n)
        return True
    except ValueError:
        return False

def parse_bind(bind:str):
    periods = {
        "s": 1,
        "m": 60,
        "h": 3600,
        "d": 86400,
        "w": 604800
    }

    seconds = 0

    parts = []
    buffer = ""

    for char in bind:
        if is_integer(char):
            buffer += char
        else:
            parts.append(buffer + char)
            buffer = ""

    for part in parts:
        period = part[-1]

        amount = int(part.replace(period,""))

        seconds += amount * periods[period.lower()]

    return seconds

# TODO unit test
def default_ttl(text:str):
    lines = text.splitlines()
    for line in lines:
        if "$TTL".casefold() in line.casefold():
            ttl_str = line.split(" ")[1]
            try:
                ttl = int(ttl_str)
                return int(ttl)
            except ValueError:
                # the value could be BIND format, attempt to parse
                # https://www.zytrax.com/books//dns/apa/time.html
                ttl = parse_bind(ttl_str)
                return ttl

    return None

# TODO write test case
def default_origin(text:str):
    lines = text.splitlines()
    for line in lines:
        if "$ORIGIN".casefold() in line.casefold():
            origin = line.split(" ")[1]
            return origin
    return None



# ensure that the string:
# 1. ends and starts with round brackets
# 2. there is no whitespace between the brackets and the content
# e.g. " ( 'test string') " should be "('test string')"
def trim_brackets(input_string:str):
    # regex that matches either round bracket, 
    # preceded or followed by whitespace

    # pattern = re.compile(r"(\(\s)|(\s\()|(\)\s)|(\s\))")
    pattern = re.compile(r"(\(\s)|(\)\s)|(\s\))")

    # print(re.match(pattern,input_string).groups())

    # while re.search(pattern, input_string) is not None:
    while re.search(pattern, input_string) is not None:
        
        matched_groups = (g for g in re.search(pattern, input_string).groups() if g is not None)

        for group in matched_groups:

            input_string = input_string.replace(
                group,
                group.strip()
            )

    return input_string

# worth renaming tbh
def remove_whitespace_between_quotes_between_brackets(input_string:str):
    whitespace_pattern = re.compile(r'"(.*?)"')

    bracket_pattern = re.compile(r"\((.*?)\)")

    # get bracket portion of record
    bracket_match = re.search(bracket_pattern,input_string)

    if bracket_match is None:
        return input_string
    
    bracket_contents = bracket_match.group(0)

    bracket_contents_cleaned = "(" + "".join(
        re.findall(whitespace_pattern, bracket_contents)
    ) + ")"

    result = re.sub(
        bracket_pattern,
        bracket_contents_cleaned,
        input_string
    )

    print(result)

    return result



def collapse_lines(lines:List[str],delimiter = ""):
    buffer = []
    collapsed_lines = []
    

    for line in lines:
        # if the single line has both a closing and 
        # opening bracket, then it can be added straight away
        # because it cannot be further collapsed
        if "(" in line and ")" in line:

            collapsed_lines.append(trim_brackets(line))

        # start of a multi-line record, store in buffer
        elif "(" in line:
            buffer.append(line)

        # add the line to the buffer, the buffer forms a single record
        # close the buffer
        elif ")" in line:
            buffer.append(line)

            # remove whitespace between quotes, between brackets
            collapsed_lines.append(delimiter.join(buffer))
            buffer = ""


        # if the buffer has content in it, add current line
        elif len(buffer) > 0:
            buffer.append(line)

        # record is not part of a multiline record, no alteration needed.
        else:
            collapsed_lines.append(line)
    return collapsed_lines
    

# TODO unit test
# TODO refactor
def find_soa_lines(text:str):

    lines = text.splitlines()

    soa_start_line = 0

    soa_end_line = 0

    find_bracket = False

    soa_found = False
    for line_number in range(0,len(lines)-1):
        line = lines[line_number]
        if "SOA" in line.upper():
            soa_found = True
            soa_start_line = line_number
            if "(" in line:
                find_bracket = True
            else:
                soa_end_line = soa_start_line
                break


        if ")" in line and find_bracket is True:
            soa_end_line = line_number
            break

    if not soa_found:
        return None
    else:
        return range(soa_start_line,soa_end_line + 1)

# TODO unit test
def parted_soa(text:str):

    # flatten
    text = text.replace("\n","")

    # part out the soa
    parts = text.split()

    # remove multiple spaces, and replace them with a single space
    parts = list(
        filter(
            lambda x : ")" not in x and "(" not in x,
            parts
        )
    )

    return parts
