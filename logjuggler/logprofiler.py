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




