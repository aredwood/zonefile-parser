import zonefile_parser

class Main:

    def test_correctly_parses_srv(self):
        text = """
$TTL 10d
$ORIGIN example.com.
_sip._tcp.example.com. 86400 IN SRV 0 5 5060 sipserver.example.com.
"""

        result = zonefile_parser.main.parse(text)

        record = result[0]

        assert (record.name == "_sip._tcp.example.com.")
        assert (record.ttl == "86400")
        assert (record.rclass == "IN")
        assert (record.rtype == "SRV")
        assert (record.rdata == {
            "priority":"0",
            "weight":"5",
            "port":"5060",
            "host":"sipserver.example.com."
        })

    def test_handles_lowercase_rclass(self):
        text = """
$TTL 10d
$ORIGIN example.com.
@ 86400 IN CAA 0 issue "ca.example.com"
""" 
        result = zonefile_parser.main.parse(text)

        record = result[0]

        assert record.rclass == "IN"
    def test_handles_mixedcase_rclass(self):
        text = """
$TTL 10d
$ORIGIN example.com.
@ 86400 iN CAA 0 issue "ca.example.com"
""" 
        result = zonefile_parser.main.parse(text)

        record = result[0]

        assert record.rclass == "IN"

    def test_correctly_parses_caa(self):
        text = """
$TTL 10d
$ORIGIN example.com.
@ 86400 IN CAA 0 issue "ca.example.com"
"""

        result = zonefile_parser.main.parse(text)

        record = result[0]

        assert (record.name == "@")
        assert (record.ttl == "86400")
        assert (record.rclass == "IN")
        assert (record.rtype == "CAA")
        assert (record.rdata == {
            "flag":"0",
            "tag":"issue",
            "value":"ca.example.com"
        })