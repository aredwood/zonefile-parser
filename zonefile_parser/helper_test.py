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