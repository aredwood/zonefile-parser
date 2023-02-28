import zonefile_parser

class TestMain:

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

    def test_issue_26(self):
        text = """
$TTL 86400
$ORIGIN XX.EXAMPLE.
@ IN SOA NS1.XX.EXAMPLE. HOSTMATER.XX.EXAMPLE. (
1997102000 ; serial
1800 ; refresh (30 mins)
900 ; retry (15 mins)
604800 ; expire (7 days)
1200 ) ; minimum (20 mins)
"""
        result = zonefile_parser.main.parse(text)
        record = result[0]

        assert (record.rtype == "SOA")

