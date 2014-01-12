#!/usr/bin/env python

import collections
import datetime
import argparse


Log = collections.namedtuple("Log", "date level session_id business_id request_id message")


def read_log_file(file):
    """Yield log entries from the given file, line by line.

    Raises IOError if the file can not be found.
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
    return datetime_obj.isoformat()


def time_str_to_datetime(timestring):
    """Return datetime object from the given timestring.

    Timestring should be in the following format: '%Y-%m-%d %H:%M:%S'

    """
    try:
        return datetime.datetime.strptime(timestring, '%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        print("Time string is malformed. Got exception: {0}".format(e))

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
    """Return a func that filters logs by level."""
    def inner(log_line):
        if log_line.level == str(loglevel).upper():
            return log_line
    return inner


def session_id_filter(sid):
    """Return a func that filters logs by session id."""
    def inner(log_line):
        if log_line.session_id == str(sid):
            return log_line
    return inner


def business_id_filter(bid):
    """Return func that filters logs by business id."""
    def inner(log_line):
        if log_line.business_id == str(bid):
            return log_line
    return inner


def request_id_filter(rid):
    """Return func that filters logs by request id."""
    def inner(log_line):
        if log_line.request_id == str(rid):
            return log_line
    return inner


def date_range_filter(start_date, end_date):
    """
    Return a func that filters logs between given
    start and end datetime obj.
    """
    if isinstance(start_date, str):
        start_date = time_str_to_datetime(start_date)
    if isinstance(end_date, str):
        end_date = time_str_to_datetime(end_date)

    def inner(log_line):
        if start_date <= log_line.date <= end_date:
            return log_line
    return inner


def display_search_results(results):
    for log in results:
        print log


def well_formed_timestamp(timestamp):
    """Validates if timestamp is well formed.

    Args:
        timestmp: str

    Raises:
        argparse.ArgumentError if datetime object can not be created from timestamp.
    """
    try:
        time_str_to_datetime(timestamp)
        return
    except ValueError:
        raise argparse.ArgumentError('Timestamp {timestamp} is not well formed'.format(
            timestmp=timestamp))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A simple log file parser.")
    parser.add_argument('-f', '--file', dest='logfile', action='store',
                        help='Log file to parse', required=True)

    subparsers = parser.add_subparsers(help='Log filters')

    log_level_parser = subparsers.add_parser('loglevel')
    log_level_parser.add_argument('loglevel', action='store', choices=('DEBUG', 'INFO', 'WARN', 'ERROR'))

    business_id_parser = subparsers.add_parser('business_id')
    business_id_parser.add_argument('bid', action='store', help='Show logs with business id')

    session_id_parser = subparsers.add_parser('session_id')
    session_id_parser.add_argument('sid', action='store', help='Show logs with session id')

    request_id_parser = subparsers.add_parser('request_id')
    request_id_parser.add_argument('rid', action='store', help='Show logs with request id.')

    date_parser = subparsers.add_parser('date')
    date_parser.add_argument('start', action='store', help='Start date.')
    date_parser.add_argument('end', action='store', help='End date.')

    arg_dict = vars(parser.parse_args())

    log_entries = [Log(log_time(l), log_level(l), session_id(l), business_id(l),
                       request_id(l), log_message(l)) for l in read_log_file(arg_dict.get('logfile'))]

    if arg_dict.get('loglevel'):
        display_search_results(search_results(log_level_filter(arg_dict.get('loglevel')), log_entries))

    if arg_dict.get('bid'):
        display_search_results(search_results(business_id_filter(arg_dict.get('bid')), log_entries))

    if arg_dict.get('sid'):
        display_search_results(search_results(session_id_filter(arg_dict.get('sid')), log_entries))

    if arg_dict.get('rid'):
        display_search_results(search_results(request_id_filter(arg_dict.get('rid')), log_entries))

    if arg_dict.get('start') and arg_dict.get('end'):
        display_search_results(search_results(date_range_filter(
            start_date=arg_dict.get('start'), end_date=arg_dict.get('end')), log_entries))
