import pytest
import zonefile_parser.helper as helper

class TestRemoveComments:
    def test_correctly_removes_comment(self):
        input = "value;comment"
        result = helper.remove_comments(input)
        assert result == "value"

    def test_doesnt_remove_comment_in_quote(self):
        input = 'value";comment"'
        result = helper.remove_comments(input)
        assert result == input

    def test_doesnt_change_string_without_comment(self):
        input = "something"
        result = helper.remove_comments(input)
        assert result == input

class TestIsInQuote:
    def test_returns_whether_index_in_quote(self):
        input = '"A"'
        result = helper.is_in_quote(input,1)
        assert result == True

    def test_string_not_in_quote_return_false(self):
        input = '"A"'
        result = helper.is_in_quote(input,0)
        assert result == False

class TestParseBind:
    def test_parses_two_digit_period(self):
        bind_string = "15M"
        result = helper.parse_bind(bind_string)
        assert result == (15*60)

    def test_parses_multiple_periods(self):
        bind_string = "1D15M"
        result = helper.parse_bind(bind_string)
        assert result == (60 * 60 * 24) + (60 * 15)


class TestCollapseLines:
    def test_doesnt_collapse_normal_lines(self):
        input = [
            "1",
            "2",
            "3"
        ]

        result = helper.collapse_lines(input)

        assert result == [
            "1",
            "2",
            "3"
        ]
    
    def test_collapse_brackets_into_line(self):
        input = [
            "1",
            "(2",
            "3",
            "4)"
        ]

        result = helper.collapse_lines(input)

        assert result == ["1","(234)"];

    def test_handles_single_line(self):
        input = ["(1)"]

        result = helper.collapse_lines(input)

        assert result == ["(1)"]

class TestRemoveWhitespace():
    def test_removes_whitespace_between_quote_strings(self):
        input_string = '("1" "2")'

        result = helper.remove_whitespace_between_quotes_between_brackets(input_string)

        assert result == "(12)"
    
    def test_whitespace_between_quotes_is_preserved(self):
        input_string = '(" 1 " "2")'

        result = helper.remove_whitespace_between_quotes_between_brackets(input_string)

        assert result == "( 1 2)"

class TestDefaultTTL():
    def test_parses_uppercase_ttl(self):
        input_string = """
$TTL 1D
"""

        ttl = helper.default_ttl(input_string)

        assert ttl == (60*60*24)
    def test_parses_lowercase_ttl(self):
        input_string = """
$ttl 1D
"""

        ttl = helper.default_ttl(input_string)

        assert ttl == (60*60*24)

    def test_parses_mixedcase_ttl(self):
        input_string = """
$TtL 1D
"""

        ttl = helper.default_ttl(input_string)

        assert ttl == (60*60*24)

class TestDefaultOrigin():
    def test_parses_uppercase_origin(self):
        input_string = """
$ORIGIN example.com
"""
        origin = helper.default_origin(input_string)

        assert origin == "example.com"

    def test_parses_lowercase_origin(self):
        input_string = """
$origin example.com
"""
        origin = helper.default_origin(input_string)

        assert origin == "example.com"

    def test_parses_mixedcase_origin(self):
        input_string = """
$OrIgIn example.com
"""
        origin = helper.default_origin(input_string)

        assert origin == "example.com"