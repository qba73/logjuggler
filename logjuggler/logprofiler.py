#!/usr/bin/env python

"""

Example of a profiler decorator that collect basic
stats about decorated function.

Usage:
    >>>
    >>> from logprofiler import profile
    >>>
    >>> @profile
    ... def sample_foo():
        ... return [item for item in xrange(10)]
        ...
    >>> sample_foo()

        === Function profiler report ===

        Function:   sample_foo
        NumSamples: 1
        Min:        2.47955322266e-05
        Max         2.47955322266e-05
        Average:    2.47955322266e-05

        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    >>> sample_foo()

        === Function profiler report ===

        Function:   sample_foo
        NumSamples: 2
        Min:        1.78813934326e-05
        Max         2.47955322266e-05
        Average:    2.13384628296e-05

        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>>
    >>> sample_foo()

        === Function profiler report ===

        Function:   sample_foo
        NumSamples: 3
        Min:        1.78813934326e-05
        Max         2.47955322266e-05
        Average:    2.121925354e-05

        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>>
    >>> sample_foo()

        === Function profiler report ===

        Function:   sample_foo
        NumSamples: 4
        Min:        1.78813934326e-05
        Max         2.47955322266e-05
        Average:    2.03847885132e-05

        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>>


Usage:
    >>> import logjuggler as lj
    >>> from logprofiler import profile
    >>>
    >>> log_entries = [lj.Log(lj.log_time(l), lj.log_level(l), lj.session_id(l), lj.business_id(l), lj.request_id(l), lj.log_message(l)) for l in lj.read_log_file('../data/app.log')]
    >>> log_entries
    [Log(date=datetime.datetime(2012, 9, 13, 16, 4, 22), level='DEBUG', session_id='34523', business_id='1329', request_id='65d33', message='Starting new session'), Log(date=datetime.datetime(2012, 9, 13, 16, 4, 30), level='DEBUG', session_id='34523', business_id='1329', request_id='54f22', message='Authenticating User'), Log(date=datetime.datetime(2012, 9, 13, 16, 5, 30), level='DEBUG', session_id='42111', business_id='319', request_id='65a23', message='Starting new session'), Log(date=datetime.datetime(2012, 9, 13, 16, 4, 50), level='ERROR', session_id='34523', business_id='1329', request_id='54ff3', message='Missing Authentication token'), Log(date=datetime.datetime(2012, 9, 13, 16, 5, 31), level='DEBUG', session_id='42111', business_id='319', request_id='86472', message='Authenticating User'), Log(date=datetime.datetime(2012, 9, 13, 16, 5, 31), level='DEBUG', session_id='42111', business_id='319', request_id='7a323', message='Deleting asset with ID 543234'), Log(date=datetime.datetime(2012, 9, 13, 16, 5, 32), level='WARN', session_id='42111', business_id='319', request_id='7a323', message='Invalid asset ID')]
    >>>
    >>>
    >>> @profile
    ... def log_level(log_level, log_entries):
    ...     lj.get_log_level(log_level, log_entries)
    >>>
    >>> log_level('DEBUG', log_entries)

    === Function profiler report ===

    Function: log_level
    NumSamples:   1
    Min:      0.000174045562744
    Max       0.000174045562744
    Average:  0.000174045562744

    >>> log_level('DEBUG', log_entries)

    === Function profiler report ===

    Function: log_level
    NumSamples:   2
    Min:      0.000169038772583
    Max       0.000174045562744
    Average:  0.000171542167664

    >>> log_level('DEBUG', log_entries)

    === Function profiler report ===

    Function: log_level
    NumSamples:   3
    Min:      0.000169038772583
    Max       0.000227928161621
    Average:  0.000190337498983

    >>> log_level('DEBUG', log_entries)

    === Function profiler report ===

    Function: log_level
    NumSamples:   4
    Min:      0.000169038772583
    Max       0.000227928161621
    Average:  0.000186502933502

    >>> log_level('DEBUG', log_entries)

    === Function profiler report ===

    Function: log_level
    NumSamples:   5
    Min:      0.000169038772583
    Max       0.000227928161621
    Average:  0.000184011459351

    >>> log_level('DEBUG', log_entries)

    === Function profiler report ===

    Function: log_level
    NumSamples:   6
    Min:      0.000169038772583
    Max       0.000227928161621
    Average:  0.000181992848714

    >>> log_level('DEBUG', log_entries)

    === Function profiler report ===

    Function: log_level
    NumSamples:   7
    Min:      0.000169038772583
    Max       0.000235080718994
    Average:  0.000189576830183

    >>> log_level('DEBUG', log_entries)

    === Function profiler report ===

    Function: log_level
    NumSamples:   8
    Min:      0.000169038772583
    Max       0.000235080718994
    Average:  0.000187516212463

    >>> log_level('DEBUG', log_entries)

    === Function profiler report ===

    Function: log_level
    NumSamples:   9
    Min:      0.000168085098267
    Max       0.000235080718994
    Average:  0.000185357199775

    >>> log_level('DEBUG', log_entries)

    === Function profiler report ===

    Function: log_level
    NumSamples:   10
    Min:      0.000168085098267
    Max       0.000235080718994
    Average:  0.000184416770935

    >>> log_level('WARN', log_entries)

    === Function profiler report ===

    Function: log_level
    NumSamples:   11
    Min:      0.000102043151855
    Max       0.000235080718994
    Average:  0.00017692826011


"""

import time


class profile(object):

    """Profiler decorator."""

    def __init__(self, func):
        self.func = func
        self.counter = 0
        self.executions = []
        self.stats = {'func': self.func.__name__}

    def __call__(self, *args, **kwargs):
        start = time.time()

        result = self.func(*args, **kwargs)

        elapsed_time = time.time() - start
        self.counter += 1
        self.add_exec_sample(elapsed_time)
        self.update_stats()
        self.print_report()
        return result

    def add_exec_sample(self, elapsed):
        self.executions.append(elapsed)

    def update_stats(self):
        self.stats['counter'] = self.counter
        self.stats['avg_time'] = sum(self.executions) / self.counter
        self.stats['min_time'] = min(self.executions)
        self.stats['max_time'] = max(self.executions)

    def print_report(self):
        template = ("\n=== Function profiler report ===\n\n"
                    "Function:\t{func}\nNumSamples:\t{counter}\n"
                    "Min:\t\t{tmin}\nMax\t\t{tmax}\nAverage:\t{tavg}\n")
        print template.format(func=self.stats.get('func'),
                              counter=self.stats.get('counter'),
                              tmin=self.stats.get('min_time'),
                              tmax=self.stats.get('max_time'),
                              tavg=self.stats.get('avg_time'))


@profile
def test_function():
    return [a for a in xrange(10)]



if __name__=="__main__":
    test_function()





