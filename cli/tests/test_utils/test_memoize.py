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

import pytest

from unittest import TestCase

from polyaxon.utils.memoize_decorators import memoize, memoize_method


@pytest.mark.utils_mark
class MemoizeTest(TestCase):
    """
    A test case for the memoize decorator
    """

    def setUp(self):
        self.execution_count = 0

    def test_function_is_executed_on_first_request(self):
        @memoize
        def wrapped_function(param):
            self.execution_count += 1
            return param

        result = wrapped_function(0)

        self.assertEqual(0, result)
        self.assertEqual(1, self.execution_count)

    def test_results_are_cached(self):
        @memoize
        def wrapped_function(param):
            self.execution_count += 1
            return param

        result = wrapped_function(0)
        self.assertEqual(0, result)
        result = wrapped_function(1)
        self.assertEqual(1, result)

        result = wrapped_function(0)
        self.assertEqual(0, result)
        result = wrapped_function(1)
        self.assertEqual(1, result)

        self.assertEqual(2, self.execution_count)

    def test_works_with_functions_without_arguments(self):
        @memoize
        def wrapped_function():
            self.execution_count += 1
            return 42

        wrapped_function()
        result = wrapped_function()

        self.assertEqual(42, result)
        self.assertEqual(1, self.execution_count)

    def test_works_with_functions_with_multiple_arguments(self):
        @memoize
        def wrapped_function(a, b):
            self.execution_count += 1
            return a**b

        wrapped_function(2, 3)
        result = wrapped_function(2, 3)

        self.assertEqual(result, 8)
        self.assertEqual(self.execution_count, 1)


@pytest.mark.utils_mark
class MemoizeMethodTest(TestCase):
    """
    A test case for the `memoize_method` decorator.
    """

    def setUp(self):
        super().setUp()

        class TestClass:
            def __init__(self):
                self.test0_execution_count = 0
                self.test1_execution_count = 0
                self.test2_execution_count = 0

            @memoize_method
            def test0(self):
                self.test0_execution_count += 1
                return 42

            @memoize_method
            def test1(self, a):
                self.test1_execution_count += 1
                return a

            @memoize_method
            def test2(self, a, b):
                self.test2_execution_count += 1
                return a**b

        self.obj1 = TestClass()
        self.obj2 = TestClass()

    def test_function_is_executed_on_first_request(self):
        result0 = self.obj1.test0()
        result1 = self.obj1.test1(1)
        result2 = self.obj1.test2(2, 3)
        self.assertEqual(42, result0)
        self.assertEqual(1, result1)
        self.assertEqual(8, result2)
        self.assertEqual(1, self.obj1.test0_execution_count)
        self.assertEqual(1, self.obj1.test1_execution_count)
        self.assertEqual(1, self.obj1.test2_execution_count)

    def test_results_are_cached(self):
        self.obj1.test0()
        self.obj1.test1(1)
        self.obj1.test2(2, 3)
        result0 = self.obj1.test0()
        result1 = self.obj1.test1(1)
        result2 = self.obj1.test2(2, 3)
        self.assertEqual(42, result0)
        self.assertEqual(1, result1)
        self.assertEqual(8, result2)
        self.assertEqual(1, self.obj1.test0_execution_count)
        self.assertEqual(1, self.obj1.test1_execution_count)
        self.assertEqual(1, self.obj1.test2_execution_count)

    def test_function_is_executed_for_new_parameter_combination(self):
        self.obj1.test2(2, 3)
        result = self.obj1.test2(3, 2)
        self.assertEqual(9, result)
        self.assertEqual(2, self.obj1.test2_execution_count)

    def test_result_is_not_cached_across_instances(self):
        self.obj1.test2(2, 3)
        self.assertEqual(0, self.obj2.test2_execution_count)
        self.obj2.test2(2, 3)
        self.assertEqual(1, self.obj2.test2_execution_count)
