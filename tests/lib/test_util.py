import unittest


from zonefile_parser.helper import remove_comments

from zonefile_parser.helper import default_ttl

from zonefile_parser.helper import parse_bind

import zonefile_parser

from zonefile_parser.record import Record

class Util(unittest.TestCase):
    def test_remove_comments(self):
        test_string = "test; comment"
        result = remove_comments(test_string)
        self.assertEqual(result,"test")


class test_default_ttl(unittest.TestCase):
    def test_gets_ttl(self):
        text = """
$TTL 300
$ORIGIN example.site.
        """

        result = default_ttl(text)
        self.assertEqual(result,300)
    def test_bind_parsing(self):
        # parses 10 days
        self.assertEqual(parse_bind("10d"),864000)
        # parses 10 days with a capital "d"
        self.assertEqual(parse_bind("10D"),864000)


    def test_gets_ttl_bind(self):
        text = """
$TTL 10d
$ORIGIN example.site.
        """

        result = default_ttl(text)
        self.assertEqual(result,864000)

    def test_correctly_parses_srv(self):
        text = """
$TTL 10d
$ORIGIN example.com.
_sip._tcp.example.com. 86400 IN SRV 0 5 5060 sipserver.example.com.
"""

        result = zonefile_parser.main.parse(text)

        record = result[0]

        self.assertEqual(record.name,"_sip._tcp.example.com.")
        self.assertEqual(record.ttl,"86400")
        self.assertEqual(record.rclass,"IN")
        self.assertEqual(record.rtype,"SRV")
        self.assertEqual(record.rdata,{
            "priority":"0",
            "weight":"5",
            "port":"5060",
            "host":"sipserver.example.com."
        })
        
if __name__ == '__main__':
    unittest.main()
