import unittest


from zonefile_parser.helper import remove_comments

from zonefile_parser.helper import default_ttl

class Util(unittest.TestCase):
    def test_remove_comments(self):
        test_string = "test; comment"
        result = remove_comments(test_string)
        self.assertEqual(result,"test")


class test_default_ttl(unittest.TestCase):
    def test_gets_ttl(self):
        text = """
$TTL 300
$ORIGIN emailtesting.site.
        """

        result = default_ttl(text)
        self.assertEqual(result,300)

    def test_gets_ttl_bind(self):
        text = """
$TTL 10d
$ORIGIN emailtesting.site.
        """

        result = default_ttl(text)
        self.assertEqual(result,864000)

if __name__ == '__main__':
    unittest.main()
