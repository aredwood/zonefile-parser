import zonefile_parser

class TestMain:

    def test_parse_file(self):
        result = zonefile_parser.main.parse_file("./test-data/zonefiles/00-parse-file/main.zone")

        record = result[0]

        assert (record.ttl == "86400")

    def test_parse_file_with_include(self):
        result = zonefile_parser.main.parse_file("./test-data/zonefiles/01-test-includes/main.zone")

        record = result[3]

        assert record.rdata == {
            "value": "value.com"
        }

    def test_check_closing_space_for_soa(self):
        result = zonefile_parser.main.parse_file("./test-data/zonefiles/03-issue-50-regression/main.zone")

        record = result[0]

        assert record.name == '@'
        assert record.rclass == 'IN'
        assert record.rdata['expire'] == '1w'
        assert record.rdata['minimum'] == '1m'
        assert record.rdata['mname'] == 'localhost.'
        assert record.rdata['refresh'] == '1h'
        assert record.rdata['retry'] == '5m'
        assert record.rdata['rname'] == 'root.localhost.'
        assert record.rdata['serial'] == '2025031001'
        assert record.rtype == 'SOA'
        assert record.ttl == 60



    def test_parse_file_with_include_different_path(self):
        result = zonefile_parser.main.parse_file("./test-data/zonefiles/01-test-includes/main.zone")

        record = result[13]

        # include inherits the imported zone origin
        assert record.name == "www.zone1.example.com"

        assert record.rdata == {"value": "192.168.2.10"}

    def test_parse_file_includes_no_origin(self):
        result = zonefile_parser.main.parse_file("./test-data/zonefiles/02-test-includes-noorigin/main.zone")

        record = result[3]

        assert record.name == "blank.example.com"
        assert record.rdata == {"value":"192.168.1.50"}


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

    def test_parentheses_single_line(self):
        text = """
dkim._domainkey         TXT	( "v=DKIM1; t=s; p=MIIBIjANBg/kqhkiG9w0BAQEFAAOCAQ8AMKKFZIIBCgKCAQEA2KXqtqfmWDgP6X7d2gKPCAl" ) 
"""

        result = zonefile_parser.main.parse(text)

        record = result[0]

        assert record.name == "dkim._domainkey"
        assert record.rtype == "TXT"
        assert record.rdata == {
            "value":"v=DKIM1; t=s; p=MIIBIjANBg/kqhkiG9w0BAQEFAAOCAQ8AMKKFZIIBCgKCAQEA2KXqtqfmWDgP6X7d2gKPCAl"
        }

    def test_parentheses_multi_line(self):
        text = """
dkim._domainkey         TXT	( "test=multi; v=DKIM1; t=s; p=MIIBIjANBg/kqhGGEEkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2KXqtqfmWDgP6X7d2gKPCAl"
                        		"tlgbSstMhKj3+UA+VbGZomqyY1er7QqkIriQSuTQT2hkV7DHHFMhYx4MFUvDHbLtTTREtkkzKqRr2Z1TwuYmgS5kzo453lm0uiQIxQXXHLlUMST0VerzO/Jp+0Ix76g68DxSU2nWudW6rE"
                        		"7g3vADE20JDJqriUKjGBqKY0RR/CqdLCLsyBrvuF/Nefg8hB/oz/0a3Ae1AYVmqtEf2d9Z/seGQPVj+E/wqobRyYdEKo4BBdUfRb3Jaw6rpqQ5aVOTuOZF5zaozf0BtgKeo"
                        		"l4PzCcPLQUTWp42Vh+9aeCL/j34XJyFjN7+40L3itdequjc6v/Ose51wnSMtR4sWwIDAQAB" )
"""

        result = zonefile_parser.main.parse(text)

        record = result[0]

        assert record.rdata == {
            "value":"test=multi; v=DKIM1; t=s; p=MIIBIjANBg/kqhGGEEkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2KXqtqfmWDgP6X7d2gKPCAltlgbSstMhKj3+UA+VbGZomqyY1er7QqkIriQSuTQT2hkV7DHHFMhYx4MFUvDHbLtTTREtkkzKqRr2Z1TwuYmgS5kzo453lm0uiQIxQXXHLlUMST0VerzO/Jp+0Ix76g68DxSU2nWudW6rE7g3vADE20JDJqriUKjGBqKY0RR/CqdLCLsyBrvuF/Nefg8hB/oz/0a3Ae1AYVmqtEf2d9Z/seGQPVj+E/wqobRyYdEKo4BBdUfRb3Jaw6rpqQ5aVOTuOZF5zaozf0BtgKeol4PzCcPLQUTWp42Vh+9aeCL/j34XJyFjN7+40L3itdequjc6v/Ose51wnSMtR4sWwIDAQAB"
        }
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
        
        # should infer name from origin declaration
        assert (record.name == "example.com.")
        assert (record.ttl == "86400")
        assert (record.rclass == "IN")
        assert (record.rtype == "CAA")
        assert (record.rdata == {
            "flag":"0",
            "tag":"issue",
            "value":"ca.example.com"
        })

    def test_issue_24(self):
        text = """
$origin example.com
@	300	IN	SOA	1 1 2 3600 600 604800 1800
sub.sub	63	IN	CNAME	value.com
sub     64  IN  CNAME   value.com
@       65  IN  CNAME   value.com
        65  IN  CNAME   value.com
"""
        result = zonefile_parser.main.parse(text)

        assert (result[0].rtype == "SOA")

        assert (result[1].name == "sub.sub.example.com")
        assert (result[2].name == "sub.example.com")
        assert (result[3].name == "example.com")
        assert (result[4].name == "example.com")

    # issue 47
    def test_adaptive_delimiter(self):
        text = str("""
$TTL	10d
$ORIGIN	example.com.
@	86400	IN	CAA	0	issue	"ca.example.com"
""")
        record = zonefile_parser.main.parse(text)[0]
        assert (record.name == "example.com.")
        assert (record.ttl == "86400")
        assert (record.rclass == "IN")
        assert (record.rtype == "CAA")
        assert (record.rdata == {
            "flag":"0",
            "tag":"issue",
            "value":"ca.example.com"
        })