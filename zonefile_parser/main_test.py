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

    def test_multiple_origin_directives(self):
        text = """
$TTL 300
$ORIGIN first.com.
@ 300 IN A 1.2.3.4
sub 300 IN A 1.2.3.5
$ORIGIN second.com.
@ 300 IN A 5.6.7.8
host 300 IN A 5.6.7.9
"""
        result = zonefile_parser.main.parse(text)

        # records under first.com.
        assert result[0].name == "first.com."
        assert result[0].rdata == {"value": "1.2.3.4"}
        assert result[1].name == "sub.first.com."
        assert result[1].rdata == {"value": "1.2.3.5"}

        # records under second.com. (origin changed mid-file)
        assert result[2].name == "second.com."
        assert result[2].rdata == {"value": "5.6.7.8"}
        assert result[3].name == "host.second.com."
        assert result[3].rdata == {"value": "5.6.7.9"}

    def test_multiple_origins_more_than_two(self):
        # three consecutive $ORIGIN changes — each group of records
        # should only be affected by the origin active at that point
        text = """
$TTL 300
$ORIGIN a.com.
@ 300 IN A 1.1.1.1
$ORIGIN b.com.
@ 300 IN A 2.2.2.2
$ORIGIN c.com.
@ 300 IN A 3.3.3.3
"""
        result = zonefile_parser.main.parse(text)

        assert result[0].name == "a.com."
        assert result[1].name == "b.com."
        assert result[2].name == "c.com."

    def test_multiple_origins_at_symbol_updates_with_origin(self):
        # @ should resolve to whatever origin is active at that line,
        # not the first origin in the file
        text = """
$TTL 300
$ORIGIN first.com.
@ 300 IN A 1.2.3.4
$ORIGIN second.com.
@ 300 IN A 5.6.7.8
"""
        result = zonefile_parser.main.parse(text)

        assert result[0].name == "first.com."
        assert result[1].name == "second.com."

    def test_multiple_origins_relative_names_use_active_origin(self):
        # relative names should be expanded using whichever origin
        # was most recently declared, not the first one
        text = """
$TTL 300
$ORIGIN first.com.
www 300 IN A 1.2.3.4
$ORIGIN second.com.
www 300 IN A 5.6.7.8
"""
        result = zonefile_parser.main.parse(text)

        assert result[0].name == "www.first.com."
        assert result[1].name == "www.second.com."

    def test_multiple_origins_tab_delimited(self):
        # $ORIGIN directives using tab delimiters should be handled
        # correctly when there are multiple of them
        text = "$TTL 300\n$ORIGIN\tfirst.com.\n@ 300 IN A 1.2.3.4\n$ORIGIN\tsecond.com.\n@ 300 IN A 5.6.7.8\n"
        result = zonefile_parser.main.parse(text)

        assert result[0].name == "first.com."
        assert result[1].name == "second.com."

    def test_multiple_origins_case_insensitive(self):
        # $origin and $ORIGIN should both update the active origin
        text = """
$TTL 300
$origin first.com.
@ 300 IN A 1.2.3.4
$ORIGIN second.com.
@ 300 IN A 5.6.7.8
"""
        result = zonefile_parser.main.parse(text)

        assert result[0].name == "first.com."
        assert result[1].name == "second.com."

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

    def test_issue_45_cname_rdata_not_corrupted(self):
        text = """
$TTL 3600
$ORIGIN snorkell.live.
xeno-rat-snorkell-ai-1 3600 IN CNAME xeno-rat-snorkell-ai-1.netlify.app.
"""
        result = zonefile_parser.main.parse(text)

        record = result[0]

        assert record.name == "xeno-rat-snorkell-ai-1.snorkell.live."
        assert record.rtype == "CNAME"
        assert record.rdata == {"value": "xeno-rat-snorkell-ai-1.netlify.app."}

    def test_cname_target_name_appears_multiple_times(self):
        # name appears twice in the CNAME target — neither occurrence should get origin appended
        text = """
$TTL 3600
$ORIGIN example.com.
foo 3600 IN CNAME foo.foo.other.com.
"""
        result = zonefile_parser.main.parse(text)

        record = result[0]

        assert record.name == "foo.example.com."
        assert record.rtype == "CNAME"
        assert record.rdata == {"value": "foo.foo.other.com."}

    def test_origin_not_appended_to_txt_rdata_when_name_matches(self):
        # same-name substring in TXT rdata should not get origin injected
        text = """
$TTL 3600
$ORIGIN example.com.
mail 3600 IN TXT "v=spf1 include:mail.otherdomain.com ~all"
"""
        result = zonefile_parser.main.parse(text)

        record = result[0]

        assert record.name == "mail.example.com."
        assert record.rtype == "TXT"
        assert record.rdata == {"value": "v=spf1 include:mail.otherdomain.com ~all"}

    def test_issue_49_escaped_semicolon_in_txt(self):
        # TXT record with a trailing escaped semicolon (\;) should not raise ValueError
        text = """
$TTL 3600
$ORIGIN example.com.
_dmarc 3600 IN TXT v=DMARC1\\;
"""
        result = zonefile_parser.main.parse(text)

        record = result[0]

        assert record.name == "_dmarc.example.com."
        assert record.rtype == "TXT"
        assert record.rdata == {"value": "v=DMARC1;"}

    def test_issue_49_dmarc_record_with_comment(self):
        # DMARC TXT record with an escaped semicolon followed by a real comment
        # the real comment (unescaped ;) should be stripped, \; should survive as ;
        text = """
$TTL 3600
$ORIGIN example.com.
_dmarc 3600 IN TXT v=DMARC1\\; ; this is a comment
"""
        result = zonefile_parser.main.parse(text)

        record = result[0]

        assert record.name == "_dmarc.example.com."
        assert record.rtype == "TXT"
        assert record.rdata == {"value": "v=DMARC1;"}

    def test_multiple_cnames_with_name_in_target(self):
        # multiple records in the same zone, each with name appearing in their CNAME target
        text = """
$TTL 3600
$ORIGIN example.com.
api 3600 IN CNAME api.backend.net.
www 3600 IN CNAME www.cdn.net.
"""
        result = zonefile_parser.main.parse(text)

        assert result[0].name == "api.example.com."
        assert result[0].rdata == {"value": "api.backend.net."}

        assert result[1].name == "www.example.com."
        assert result[1].rdata == {"value": "www.cdn.net."}

    def test_issue_44_print_records_does_not_raise(self):
        text = """
$TTL 3600
$ORIGIN example.com.
@ 3600 IN A 192.0.2.1
"""
        records = zonefile_parser.main.parse(text)
        # __repr__ must return a str; printing a list calls repr() on each element
        assert isinstance(repr(records[0]), str)
        # str(record) and print(records) must not raise
        assert isinstance(str(records[0]), str)
        _ = str(records)  # exercises list __repr__, which calls record.__repr__()