import unittest

from scrapy.utils.misc import is_generator_with_return_value, is_generator_with_return_value_current, \
    is_generator_with_return_value_visitor


class UtilsMiscPy3TestCase(unittest.TestCase):

    def test_generators_with_return_statements(self):
        def f():
            yield 1
            return 2

        def g():
            yield 1
            return 'asdf'

        def h():
            yield 1
            return None

        def i():
            yield 1
            return

        def j():
            yield 1

        def k():
            yield 1
            yield from g()

        def m():
            yield 1

            def helper():
                return 0

            yield helper()

        def n():
            yield 1

            def helper():
                return 0

            yield helper()
            return 2

        assert is_generator_with_return_value(f)
        assert is_generator_with_return_value(g)
        assert not is_generator_with_return_value(h)
        assert not is_generator_with_return_value(i)
        assert not is_generator_with_return_value(j)
        assert not is_generator_with_return_value(k)  # not recursive
        assert not is_generator_with_return_value(m)
        assert is_generator_with_return_value(n)

        def perf_test():
            i = j = 1
            while True:
                temp = i
                i = j
                j = temp + i
                if j == i*2:
                    return 0
                if j == i*3:
                    break
                yield j
            yield i
            yield j

        number = 10000
        repetitions = 20

        import timeit, pandas as pd

        curr_t = timeit.Timer(lambda: is_generator_with_return_value_current(perf_test))
        new_t = timeit.Timer(lambda: is_generator_with_return_value(perf_test))
        new_visitor_t = timeit.Timer(lambda: is_generator_with_return_value_visitor(perf_test))

        curr_r = curr_t.repeat(repetitions, number=number)
        new_r = new_t.repeat(repetitions, number=number)
        new_visitor_r = new_visitor_t.repeat(repetitions, number=number)

        print(pd.DataFrame({'new: walk_callable': new_r,
                            'new: visitor': new_visitor_r,
                            'current': curr_r}).describe())
