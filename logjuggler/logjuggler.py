#!/usr/bin/env python

import collections
import datetime
import argparse


# namedtuple - storing data from a sinle log line
Log = collections.namedtuple("Log", "date level session_id business_id request_id message")


def read_log_file(file):
    """Returns a log line genarator.

    Args:
        file: str, location of the log file

    Raises:
        IOError if the file can not be found.

    """
    try:
        with open(file, 'r') as f:
            for line in f:
                yield line.strip("\n")
    except IOError:
        print("Log file {file_name} can not be found".format(file_name=file))


def log_message(logline):
    """Return log message (str) from the given logline (str)"""
    return logline[(logline.find("'") + 1): logline.rfind("'")]


def log_level(log_line):
    """Return log level (str) from the given log_line (str)"""
    return log_line.split(" ")[2]


def business_id(log_line):
    """Return business_id (str) from the given log_line (str)"""
    return log_line.split(' ')[4].split(':')[1]


def request_id(log_line):
    """Return request id (str) from the given log_line (str)"""
    return log_line.split(' ')[5].split(':')[1]


def session_id(log_line):
    """Return session id (str) from the given log_line (str)"""
    return log_line.split(' ')[3].split(':')[1]


def log_time(log_line):
    """Return a datetime object from the given log_line (str)"""
    timestamp = ' '.join(log_line.split(" ")[:2])
    return datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')


def time_to_iso(datetime_obj):
    """Return date in iso format (str).

    After parsing log file date is stored as a datetime obj.
    This function allows to change the date back to string
    if necessary (eg, for printing logs, etc)

    """
    return datetime_obj.isoformat(sep=' ')


def time_str_to_datetime(timestring):
    """Return datetime object from the given timestring.

    Args:
        timestamp: str in format: '%Y-%m-%d %H:%M:%S'

    Returns:
        datetime obj

    Raises:
        ValueError, if the string is not well formatted
    """
    try:
        return datetime.datetime.strptime(timestring, '%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        print("Datetime string is malformed. Got exception:\n{0}".format(e))


def search_results(query_filter, logs):
    """Return search results (list) for given query_filter (func) and logs."""
    results = []
    for log in logs:
        result = query_filter(log)
        if result:
            results.append(result)
    return map(convert_to_timestamp, results)


def convert_to_timestamp(tpl):
    """Replace datetime obj with timestamp (str)."""
    return tpl._replace(date=time_to_iso(tpl.date))


def log_level_filter(loglevel):
    """Return a func that filters logs by level.

    Args:
        loglevel: str

    """
    def inner(log_line):
        if log_line.level == str(loglevel).upper():
            return log_line
    return inner


def session_id_filter(sid):
    """Return a func that filters logs by session id.

    Args:
        sid: str

    """
    def inner(log_line):
        if log_line.session_id == str(sid):
            return log_line
    return inner


def business_id_filter(bid):
    """Return func that filters logs by business id.

    Args:
        bid: str
    """
    def inner(log_line):
        if log_line.business_id == str(bid):
            return log_line
    return inner


def request_id_filter(rid):
    """Return func that filters logs by request id.

    Args:
        rid: str

    """
    def inner(log_line):
        if log_line.request_id == str(rid):
            return log_line
    return inner


def date_range_filter(start_date, end_date):
    """Return a func that filter logs between given start and end date.

    Args:
        start_date: timestamp (str) or datetime obj
        end_date: timestamp (str) or datetime obj

    Returns:
        func

    """
    if isinstance(start_date, str):
        start_date = time_str_to_datetime(start_date)
    if isinstance(end_date, str):
        end_date = time_str_to_datetime(end_date)

    def inner(log_line):
        if start_date <= log_line.date <= end_date:
            return log_line
    return inner


def display_log(log):
    """Print a log line based on defined template.

    Args:
        log: namedtuple log obj

    """
    template = ("{date} {level} sid:{session_id} bid:{business_id} "
                "rid:{request_id} message:{message}")
    print template.format(date=log.date, level=log.level, session_id=log.session_id,
                          business_id=log.business_id, request_id=log.request_id,
                          message=log.message)


def display_search_results(results):
    """Print log lines from results.

    Args:
        results: list of filtered logs
    """
    for log in results:
        display_log(log)


# functions for profiling with decorator

def get_log_level(log_level, log_entries):
    return [res for res in search_results(log_level_filter(log_level), log_entries)]


def get_sid(sid, log_entries):
    return [res for res in search_results(session_id_filter(sid), log_entries)]


def get_bid(bid, log_entries):
    return [res for res in search_results(business_id_filter(bid), log_entries)]


def get_rid(rid, log_entries):
    return [res for res in search_results(request_id_filter(rid), log_entries)]


def get_dates(start_date, end_date, log_entries):
    return [res for res in (search_results(date_range_filter(
        start_date=arg_dict.get('start'), end_date=arg_dict.get('end')), log_entries))
    ]


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A simple log file parser.")
    parser.add_argument('-f', '--file', dest='logfile', action='store',
                        help='Log file to parse', required=True)

    subparsers = parser.add_subparsers(help='Log filters')

    log_level_parser = subparsers.add_parser('loglevel')
    log_level_parser.add_argument('loglevel', action='store',
                                  choices=('DEBUG', 'INFO', 'WARN', 'ERROR'),
                                  help="Show logs with given loglevel.")

    business_id_parser = subparsers.add_parser('bid')
    business_id_parser.add_argument('bid', action='store',
                                    help='Show logs with given business id')

    session_id_parser = subparsers.add_parser('sid')
    session_id_parser.add_argument('sid', action='store',
                                   help='Show logs with session id')

    request_id_parser = subparsers.add_parser('rid')
    request_id_parser.add_argument('rid', action='store',
                                   help='Show logs with request id.')

    date_parser = subparsers.add_parser('date')
    date_parser.add_argument('start', action='store', help='Start date.')
    date_parser.add_argument('end', action='store', help='End date.')

    arg_dict = vars(parser.parse_args())

    log_entries = (Log(log_time(l), log_level(l), session_id(l), business_id(l),
                       request_id(l), log_message(l)) for l in read_log_file(arg_dict.get('logfile')))

    if arg_dict.get('loglevel'):
        result = get_log_level(arg_dict.get('loglevel'), log_entries)
        display_search_results(result)

    if arg_dict.get('bid'):
        result = get_bid(arg_dict.get('bid'), log_entries)
        display_search_results(result)

    if arg_dict.get('sid'):
        result = get_sid(arg_dict.get('sid'), log_entries)
        display_search_results(result)

    if arg_dict.get('rid'):
        result = get_rid(arg_dict.get('rid'), log_entries)
        display_search_results(result)

    if arg_dict.get('start') and arg_dict.get('end'):
        result = get_dates(arg_dict.get('start'), arg_dict.get('end'), log_entries)
        display_search_results(result)
