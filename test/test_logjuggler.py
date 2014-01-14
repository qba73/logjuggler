"""

Tests for `logjuggler` module.

"""

import datetime
import pytest
from logjuggler import logjuggler


@pytest.fixture
def log_line():
    return "2012-09-13 16:04:22 DEBUG SID:34523 BID:1329 RID:65d33 'Starting new session'"


@pytest.fixture
def log_lines():
    return [
        logjuggler.Log(datetime.datetime(2012, 9, 13, 16, 4, 22),
            level='DEBUG', session_id='34523', business_id='1329',
            request_id='65d33', message='Starting new session'
        ),
        logjuggler.Log(datetime.datetime(2012, 9, 13, 16, 4, 30),
            level='DEBUG', session_id='34523', business_id='1329',
            request_id='54f22', message='Authenticating User'
        ),
        logjuggler.Log(datetime.datetime(2012, 9, 13, 16, 4, 33),
            level='ERROR', session_id='34523', business_id='1345',
            request_id='54ff3', message='Missing Authentication token'
        ),
        logjuggler.Log(datetime.datetime(2012, 9, 13, 16, 4, 22),
            level='DEBUG', session_id='42111', business_id='319',
            request_id='7a323', message='Deleting asset with ID 543234'
        ),
        logjuggler.Log(datetime.datetime(2012, 9, 14, 16, 4, 22),
            level='WARN', session_id='42111', business_id='319',
            request_id='7a323', message='Invalid asset ID'
        ),
    ]


class TestLogLineParsers(object):
    def test_extract_log_message(self, log_line):
        assert logjuggler.log_message(log_line) == 'Starting new session'

    def test_extract_log_level(self, log_line):
        assert logjuggler.log_level(log_line) == 'DEBUG'

    def test_extract_business_id(self, log_line):
        assert logjuggler.business_id(log_line) == '1329'

    def test_extract_request_id(self, log_line):
        assert logjuggler.request_id(log_line) == '65d33'

    def test_extract_session_id(self, log_line):
        assert logjuggler.session_id(log_line) == '34523'

    def test_timestamp_should_be_datetime_object(self, log_line):
        assert isinstance(logjuggler.log_time(log_line), datetime.datetime)

    def test_time_to_iso_should_return_timestamp_in_iso_format(self, log_line):
        assert logjuggler.time_to_iso(logjuggler.log_time(log_line)) ==\
                                                        '2012-09-13 16:04:22'


class TestDateRangeFilter(object):
    def test_log_dates_outside_range(self, log_lines):
        start_test_date = datetime.datetime(2011, 1, 12, 12, 1, 1)
        end_test_date = datetime.datetime(2011, 1, 12, 17, 1, 1)
        test_filter = logjuggler.date_range_filter(
            start_test_date, end_test_date)
        assert list(logjuggler.search_results(test_filter, log_lines)) == []

    def test_line_dates_inside_range(self, log_lines):
        start_test_date = datetime.datetime(2012, 9, 13, 16, 4, 22)
        end_test_date = datetime.datetime(2012, 9, 14, 16, 5, 32)
        test_filter = logjuggler.date_range_filter(
            start_test_date, end_test_date)
        assert len(list(logjuggler.search_results(test_filter, log_lines))) == 5

    def test_log_dates_inside_and_outside_range(self, log_lines):
        start_test_date = datetime.datetime(2012, 9, 12, 16, 4, 22)
        end_test_date = datetime.datetime(2012, 9, 13, 23, 59, 59)
        test_filter = logjuggler.date_range_filter(
            start_test_date, end_test_date)
        assert len(list(logjuggler.search_results(test_filter, log_lines))) == 4

    def test_date_string_should_be_converted_to_date_object(self, log_lines):
        start_date = '2012-09-12 16:04:22'
        end_date = '2012-09-13 23:59:59'
        test_filter = logjuggler.date_range_filter(
            start_date, end_date)
        assert len(list(logjuggler.search_results(test_filter, log_lines))) == 4


class TestLogLevelFilters(object):
    def test_debug_level(self, log_lines):
        test_filter = logjuggler.log_level_filter('DEBUG')
        assert len(list(logjuggler.search_results(test_filter, log_lines))) == 3

    def test_info_level(self, log_lines):
        test_filter = logjuggler.log_level_filter('INFO')
        assert len(list(logjuggler.search_results(test_filter, log_lines))) == 0

    def test_warn_level(self, log_lines):
        test_filter = logjuggler.log_level_filter('WARN')
        assert len(list(logjuggler.search_results(test_filter, log_lines))) == 1

    def test_not_existing_level(self, log_lines):
        test_filter = logjuggler.log_level_filter('xyz')
        assert len(list(logjuggler.search_results(test_filter, log_lines))) == 0

    def test_log_level_as_int(self, log_lines):
        test_filter = logjuggler.log_level_filter(234)
        assert len(list(logjuggler.search_results(test_filter, log_lines))) == 0


class TestSessionIdFilter(object):
    def test_existing_session_id(self, log_lines):
        test_session_id = 34523
        test_filter = logjuggler.session_id_filter(sid=test_session_id)
        search_result = logjuggler.search_results(test_filter, log_lines)
        assert len([log.session_id for log in search_result]) == 3

    def test_not_existing_session_id(self, log_lines):
        test_session_id = 'We234'
        test_filter = logjuggler.session_id_filter(sid=test_session_id)
        search_result = logjuggler.search_results(test_filter, log_lines)
        assert len([log.session_id for log in search_result]) == 0


class TestBusinessIdFilter(object):
    def test_existing_business_id(self, log_lines):
        test_business_id = 1329
        test_filter = logjuggler.business_id_filter(bid=test_business_id)
        search_result = logjuggler.search_results(test_filter, log_lines)
        assert len([log.business_id for log in search_result]) == 2

    def test_not_existing_business_id(self, log_lines):
        test_business_id = 'ZxC'
        test_filter = logjuggler.business_id_filter(bid=test_business_id)
        search_result = logjuggler.search_results(test_filter, log_lines)
        assert len([log.business_id for log in search_result]) == 0


class TestRequestIdFilter(object):
    def test_existing_request_id(self, log_lines):
        test_request_id = '54ff3'
        test_filter = logjuggler.request_id_filter(rid=test_request_id)
        search_result = logjuggler.search_results(test_filter, log_lines)
        assert len([log.request_id for log in search_result]) == 1

    def test_not_existin_grequest_id(self, log_lines):
        test_request_id = '54ff3ssss'
        test_filter = logjuggler.request_id_filter(rid=test_request_id)
        search_result = logjuggler.search_results(test_filter, log_lines)
        assert len([log.request_id for log in search_result]) == 0


class TestSearchResults(object):
    def test_log_time_should_be_type_of_str(self, log_lines):
        test_business_id = 1329
        test_filter = logjuggler.business_id_filter(bid=test_business_id)
        search_result = logjuggler.search_results(test_filter, log_lines)
        assert len([log.business_id for log in search_result]) == 2

        search_result = logjuggler.search_results(test_filter, log_lines)
        assert isinstance([item for item in search_result][0].date, str)

