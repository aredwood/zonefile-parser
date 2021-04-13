
# TODO unit test
def remove_comments(line:str):
    for index,character in enumerate(line):
        if character == ";" and not is_in_quote(line,index):
            line = line[:index]
            break
    return line

# TODO unit test
def is_in_quote(text:str,index:int):
    return text[:index].count("\"") % 2 == 1

# TODO unit test
def remove_trailing_spaces(line:str):
    return line

def collapse_brackets(text:str):
    return text

def parse_bind(bind:str):
    periods = {
        "s": 1,
        "m": 60,
        "h": 3600,
        "d": 86400,
        "w": 604800
    }

    period = bind[-1]

    amount = int(bind.replace(period,""))

    ttl_seconds = amount * periods[period.lower()]

    return ttl_seconds

# TODO unit test
def default_ttl(text:str):
    lines = text.splitlines()
    for line in lines:
        if "$TTL" in line:
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
        if "$ORIGIN" in line:
            origin = line.split(" ")[1]
            return origin
    return None

# TODO unit test
# TODO refactor
def find_soa_lines(text:str):

    lines = text.splitlines()

    soa_start_line = 0

    soa_end_line = 0

    find_bracket = False

    for line_number in range(0,len(lines)-1):
        line = lines[line_number]
        if "SOA" in line.upper():
            soa_start_line = line_number
            if "(" in line:
                find_bracket = True
            else:
                soa_end_line = soa_start_line
                break


        if ")" in line and find_bracket is True:
            soa_end_line = line_number
            break


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
