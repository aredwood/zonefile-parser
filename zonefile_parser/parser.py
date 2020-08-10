from zonefile_parser.record import Record
from enum import IntEnum

class RecordEnum(IntEnum):
    NAME = 0
    TTL = 1
    RCLASS = 2
    RTYPE = 3
    RDATA = 4
    MX_PRIORITY = 4
    MX_HOST = 5
    SOA_MNAME = 4
    SOA_RNAME = 5
    SOA_SERIAL = 6
    SOA_REFRESH = 7
    SOA_RETRY = 8
    SOA_EXPIRE = 9
    SOA_MINIMUM = 10
# TODO unit test
def parse_record(parts:list) -> Record:
    record = Record()

    record.set_name(parts[RecordEnum.NAME])
    record.set_ttl(parts[RecordEnum.TTL])
    record.set_rclass(parts[RecordEnum.RCLASS])
    record.set_rtype(parts[RecordEnum.RTYPE])

    # rdata is unique for MX and SOA, everything else is the same.
    if parts[RecordEnum.RTYPE] not in ["MX","SOA"]:
        record.set_rdata({
            "value":parts[RecordEnum.RDATA]
        })
    elif parts[RecordEnum.RTYPE] == "MX":
        # the record is a SOA or MX
        record.set_rdata({
            "priority": parts[RecordEnum.MX_PRIORITY],
            "host":parts[RecordEnum.MX_HOST]
        })
    elif parts[RecordEnum.RTYPE] == "SOA":
        record.set_rdata({
                "mname": parts[RecordEnum.SOA_MNAME],
                "rname": parts[RecordEnum.SOA_RNAME],
                "serial": parts[RecordEnum.SOA_SERIAL],
                "refresh": parts[RecordEnum.SOA_REFRESH],
                "retry": parts[RecordEnum.SOA_RETRY],
                "expire": parts[RecordEnum.SOA_EXPIRE],
                "minimum": parts[RecordEnum.SOA_MINIMUM]
        })
    return record





