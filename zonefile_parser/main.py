import os
from zonefile_parser.helper import remove_comments
from zonefile_parser.helper import remove_trailing_spaces
from zonefile_parser.helper import default_ttl
from zonefile_parser.helper import default_origin
from zonefile_parser.helper import find_soa_lines
from zonefile_parser.helper import parted_soa
from zonefile_parser.parser import parse_record

import shlex


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
def parse(text:str):

    text = clean(text)
    lines = text.splitlines()

    ttl = default_ttl(text)

    origin = default_origin(text)

    # find the SOA, process it, and add it back as a single line
    soa_lines = find_soa_lines(text)

    raw_soa = "\n".join([lines[index] for index in soa_lines])

    soa_parts = parted_soa(raw_soa)

    default_rclass = "IN"

    for index in reversed(soa_lines):
        lines.pop(index)

    lines.insert(soa_lines[0]," ".join(soa_parts))

    # remove all the $TTL & $ORIGIN lines, we have the values,
    # they are no longer needed.
    record_lines = list(
        filter(
            lambda x : "$TTL" not in x and "$ORIGIN" not in x,
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

        if record_line[0] == "@" and origin is not None:
            record_line = record_line.replace("@",origin)
            last_name = origin

        if record_line[0] == " ":
            record_line = last_name + record_line
        else:
            name = record_line[:record_line.index(" ")]
            last_name = name

        normalized_records.append(record_line)

    normalized_records = list(
        map(
            lambda x : shlex.split(x),
            normalized_records
        )
    )

    # add a TTL to records where one doesn't exist
    def add_ttl(record:list):
        if not record[1].isdigit():
            record.insert(1,ttl)

        return record

    # add an rclass (defaults to IN) when one isn't present
    def add_rclass(record:list):
        if not (record[2] in ('IN','CS','CH','HS')):
            record.insert(2,default_rclass)

        return record


    normalized_records = list(
        map(
            lambda x : add_ttl(x),
            normalized_records
        )
    )

    normalized_records = list(
        map(
            lambda x : add_rclass(x),
            normalized_records
        )
    )

    normalized_records = list(
        map(
            lambda x : parse_record(x),
            normalized_records
        )
    )

    return normalized_records
