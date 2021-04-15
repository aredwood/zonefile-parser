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
    SRV_PRIORITY = 4
    SRV_WEIGHT= 5
    SRV_PORT = 6
    SRV_HOST = 7
# TODO unit test
def parse_record(parts:list) -> Record:
    record = Record()

    record.set_name(parts[RecordEnum.NAME])
    record.set_ttl(parts[RecordEnum.TTL])
    record.set_rclass(parts[RecordEnum.RCLASS].upper())
    record.set_rtype(parts[RecordEnum.RTYPE].upper())

    # rdata is unique for MX, OA and SRV, everything else is the same.
    if record.rtype not in ["MX","SOA","SRV"]:
        record.set_rdata({
            "value":parts[RecordEnum.RDATA]
        })
    elif record.rtype == "MX":
        # the record is a SOA, MX or SRV
        record.set_rdata({
            "priority": parts[RecordEnum.MX_PRIORITY],
            "host":parts[RecordEnum.MX_HOST]
        })
    elif record.rtype == "SOA":
        record.set_rdata({
                "mname": parts[RecordEnum.SOA_MNAME],
                "rname": parts[RecordEnum.SOA_RNAME],
                "serial": parts[RecordEnum.SOA_SERIAL],
                "refresh": parts[RecordEnum.SOA_REFRESH],
                "retry": parts[RecordEnum.SOA_RETRY],
                "expire": parts[RecordEnum.SOA_EXPIRE],
                "minimum": parts[RecordEnum.SOA_MINIMUM]
        })
    elif record.rtype == "SRV":
        record.set_rdata({
            "priority": parts[RecordEnum.SRV_PRIORITY],
            "weight": parts[RecordEnum.SRV_WEIGHT],
            "port": parts[RecordEnum.SRV_PORT],
            "host": parts[RecordEnum.SRV_HOST]
        })

    return record





