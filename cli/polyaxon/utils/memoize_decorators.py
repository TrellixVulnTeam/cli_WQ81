#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def memoize(func):
    """
    Decorator: provide result cache for wrapped func. Results are cached
    for given parameter list.

    See also: http://en.wikipedia.org/wiki/Memoization

    Example:

        @memoize
        def foo(param1, param2):
            return do_calculation(param1, param2)

        a = foo(1, 2)
        b = foo(1, 2)

        The second call is a cache hit and does not lead to a 'do_calculation'
        call.

    HINT: - The current implementation does not allow to clear the cache.
            Therefore, the decorator should only be used in limited scope,
            e.g. to enhance a locally defined methods.
          - The decorator does not work with keyword arguments.
    """

    cache = {}

    def wrapper(*x):
        if x not in cache:
            cache[x] = func(*x)
        return cache[x]

    return wrapper


def memoize_method(func):
    """
    Provides memoization for methods on a specific instance.
    Results are cached for given parameter list.

    See also: http://en.wikipedia.org/wiki/Memoization

    N.B. The cache object gets added to the instance instead of the global scope.
    Therefore cached results are restricted to that instance.
    The cache dictionary gets a name containing the name of the decorated function to
    avoid clashes.

    Example:

        class MyClass:
            @memoize
            def foo(self, a, b):
                return self._do_calculation(a, b)

    HINT: - The decorator does not work with keyword arguments.
    """

    cache_name = "__CACHED_{}".format(func.__name__)

    def wrapper(self, *args):
        cache = getattr(self, cache_name, None)
        if cache is None:
            cache = {}
            setattr(self, cache_name, cache)
        if args not in cache:
            cache[args] = func(self, *args)
        return cache[args]

    return wrapper
