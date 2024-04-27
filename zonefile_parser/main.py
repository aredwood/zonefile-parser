from zonefile_parser.helper import remove_comments
from zonefile_parser.helper import remove_trailing_spaces
from zonefile_parser.helper import default_ttl
from zonefile_parser.helper import default_origin
from zonefile_parser.helper import find_soa_lines
from zonefile_parser.helper import parted_soa
from zonefile_parser.parser import parse_record
from zonefile_parser.helper import collapse_lines
from zonefile_parser.helper import trim_brackets
from zonefile_parser.helper import remove_whitespace_between_quotes_between_brackets
import shlex
import os


def clean(text:str):
    lines = text.splitlines()

    clean_lines = []
    for line in lines:
        line = remove_comments(line)
        line = remove_trailing_spaces(line)

        if len(line) == 0:
            continue
        clean_lines.append(line)

    return "\n".join(clean_lines)

# TODO unit test
# TODO break apart
# TODO error handling

# TODO this whole thing needs to be refactored at some point
# handling of spaces / tabs is inconsistent
# doing this while watching Shameless US S07E10 is affecting code quality
def parse_file(file_path:str):
    """this effectively passes the result to
    the below 'parse' function, but it
    also pre-populates all $INCLUDES
    """

    lines = [];

    with open(file_path,"r") as stream:
        content = stream.readlines()

        # get the origin for the original zone file
        # this may be used where an include is specified without an origin
        # TODO this is bad.
        found_origin = default_origin("\n".join(content))

        for line in content:
            is_include = line.casefold().startswith("$INCLUDE".casefold())

            # this line represents an include,
            # read the file
            if is_include:
                # $INCLUDE <file-name> [<domain-name>] [<comment>]
                line = line.replace("\t", " ")

                line = remove_comments(line)
                line = remove_trailing_spaces(line)

                parts = shlex.split(line)

                include_file = parts[1]
                if len(parts) is 2:
                    # there is no origin, use the default
                    include_origin = found_origin
                else:
                    include_origin = parts[2]

                resolved_path = os.path.join(
                    os.path.dirname(file_path)
                ,include_file)

                # read the include file
                with open(resolved_path,'r') as include_stream:
                    for include_line in include_stream.readlines():
                        include_line = include_line.replace("\t", " ")

                        sanitized_include_line = remove_comments(
                            remove_trailing_spaces(include_line)
                        )

                        include_line_parts = shlex.split(sanitized_include_line)

                        # as per RFC1035, if the domain in the zone is relative
                        # (does NOT end in .)
                        # we add the domain name if provided in the $INCLUDE directive
                        # if it exists

                        if not include_line_parts[0].endswith("."):
                            include_line_parts[0] = include_line_parts[0] + "." + include_origin
                        lines.append(" ".join(include_line_parts))

                pass;

            # this line isn't an include,
            # just push it back into the line
            else:
                lines.append(line)

        # all the lines have been expanded,
        # push them back together
        # and return the result of parse
        return parse(
            "\n".join(lines)
        )




def parse(text:str):

    text = clean(text)

    raw_lines = text.splitlines()

    # function to collapse records that are spread with brackets
    lines = collapse_lines(raw_lines)

    ttl = default_ttl(text)

    origin = default_origin(text)

    default_rclass = "IN"

    # find the SOA, process it, and add it back as a single line
    soa_lines = find_soa_lines(lines)

    if soa_lines is not None:
        raw_soa = "\n".join([lines[index] for index in soa_lines])

        soa_parts = parted_soa(raw_soa)

        for index in reversed(soa_lines):
            lines.pop(index)

        lines.insert(soa_lines[0]," ".join(soa_parts))

    # remove all the $TTL & $ORIGIN lines, we have the values,
    # they are no longer needed.
    record_lines = list(
        filter(
            lambda x : "$TTL".casefold() not in x.casefold() and "$ORIGIN".casefold() not in x.casefold(),
            lines
        )
    )

    # each line now represents a single record
    # we need to fill in the name of each record

    # go through the zone file and add a name to every record
    normalized_records = []
    last_name = None
    for record_line in record_lines:

        # replace all tabs with spaces
        record_line = record_line.replace("\t"," ")

        name = record_line[:record_line.index(" ")]

        # if the line starts with "@", replace it with the origin
        if record_line[0] == "@" and origin is not None:
            record_line = record_line.replace("@",origin)
            last_name = origin
        # if the line behinds with a space,
        # it inherits the name of the previously processed record
        elif record_line[0] == " ":
            record_line = last_name + record_line
        # if you specify a name, add the origin to the end of the name
        # provided that the name doesnt already have the origin
        #
        # $ORIGIN example.com
        # test              test.example.com
        # test.example.com  test.example.com
        elif origin is not None and not name.endswith(origin):
            record_line = record_line.replace(name,name + "." + origin)
        else:
            last_name = name

        # clean up any records that have brackets
        record_line = remove_whitespace_between_quotes_between_brackets(record_line)
        record_line = trim_brackets(record_line)

        normalized_records.append(record_line)
    normalized_records = list(
        map(
            shlex.split,
            normalized_records
        )
    )

    # collapse lines again due to shlex handling
    normalized_records = list(map(
        lambda  x : collapse_lines(x," "),
        normalized_records
    ))

    # add a TTL to records where one doesn't exist
    def add_ttl(record:list):
        if not record[1].isdigit():
            record.insert(1,ttl)

        return record

    # add an rclass (defaults to IN) when one isn't present
    def add_rclass(record:list):
        if not (str(record[2]).upper() in ('IN','CS','CH','HS')):
            record.insert(2,default_rclass)

        return record

    normalized_records = list(
        map(
            add_ttl,
            normalized_records
        )
    )

    normalized_records = list(
        map(
            add_rclass,
            normalized_records
        )
    )

    normalized_records = list(
        map(
            parse_record,
            normalized_records
        )
    )

    return normalized_records
