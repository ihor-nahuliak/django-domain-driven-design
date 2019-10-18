import unittest

from app.core.types.bunch import bunch


class TestCase(unittest.TestCase):

    def test_it_creates_from_dict(self):
        d = bunch({'a': 1, 'b': 2})

        self.assertEqual("bunch({'a': 1, 'b': 2})", repr(d))

    def test_it_creates_from_kwargs(self):
        d = bunch(a=1, b=2)

        self.assertEqual("bunch({'a': 1, 'b': 2})", repr(d))

    def test_it_reads_existing_keys_as_params(self):
        d = bunch(a=1, b=2)

        self.assertEqual(1, d.a)
        self.assertEqual(2, d.b)

    def test_it_raises_an_attribute_error_reading_unknown_key(self):
        d = bunch(a=1, b=2)

        with self.assertRaises(AttributeError) as err_ctx:
            _ = d.c  # noqa: F841

        self.assertEqual("'bunch' object has no attribute 'c'",
                         err_ctx.exception.args[0])

    def test_it_updates_existing_keys_as_params(self):
        d = bunch(a=1, b=2)
        d.a = 'test1'
        d.b = 'test2'

        self.assertEqual('test1', d.a)
        self.assertEqual('test2', d.b)

    def test_attr_assigning_setups_keys_that_do_not_exist(self):
        d = bunch(a=1, b=2)
        d.c = 3

        self.assertTrue(hasattr(d, 'c'))
        self.assertEqual(3, d.c)
        self.assertIn('c', d)
        self.assertEqual(3, d['c'])
        self.assertEqual("bunch({'a': 1, 'b': 2, 'c': 3})", repr(d))

    def test_key_assigning_setups_attrs_that_do_not_exist(self):
        d = bunch(a=1, b=2)
        d['c'] = 3

        self.assertTrue(hasattr(d, 'c'))
        self.assertEqual(3, d.c)
        self.assertIn('c', d)
        self.assertEqual(3, d['c'])
        self.assertEqual("bunch({'a': 1, 'b': 2, 'c': 3})", repr(d))

    def test_it_raises_an_error_setting_invalid_key(self):
        d = bunch()
        with self.assertRaises(ValueError) as err_ctx:
            d['x.y'] = 'z'

        self.assertEqual("Invalid key: 'x.y'. Only letters, "
                         "natural numbers, underline char allowed. "
                         "The first char can not be a number. "
                         "Python keywords like: 'if', 'from', etc. "
                         "are not allowed, use 'if_', 'from_' instead.",
                         err_ctx.exception.args[0])

    def test_it_raises_an_error_setting_key_that_starts_with_a_number(self):
        d = bunch()
        with self.assertRaises(ValueError) as err_ctx:
            d['1a'] = 1

        self.assertEqual("Invalid key: '1a'. Only letters, "
                         "natural numbers, underline char allowed. "
                         "The first char can not be a number. "
                         "Python keywords like: 'if', 'from', etc. "
                         "are not allowed, use 'if_', 'from_' instead.",
                         err_ctx.exception.args[0])

    def test_it_raises_an_error_setting_key_that_is_a_keyword(self):
        d = bunch()
        with self.assertRaises(ValueError) as err_ctx:
            d['if'] = 1

        self.assertEqual("Invalid key: 'if'. Only letters, "
                         "natural numbers, underline char allowed. "
                         "The first char can not be a number. "
                         "Python keywords like: 'if', 'from', etc. "
                         "are not allowed, use 'if_', 'from_' instead.",
                         err_ctx.exception.args[0])

    def test_it_raises_an_error_creating_with_an_invalid_key(self):
        with self.assertRaises(ValueError) as err_ctx:
            bunch({'x.y': 'z'})

        self.assertEqual("Invalid key: 'x.y'. Only letters, "
                         "natural numbers, underline char allowed. "
                         "The first char can not be a number. "
                         "Python keywords like: 'if', 'from', etc. "
                         "are not allowed, use 'if_', 'from_' instead.",
                         err_ctx.exception.args[0])

    def test_it_raises_an_error_creating_with_a_key_starts_with_a_number(self):
        with self.assertRaises(ValueError) as err_ctx:
            bunch({'1a': 1})

        self.assertEqual("Invalid key: '1a'. Only letters, "
                         "natural numbers, underline char allowed. "
                         "The first char can not be a number. "
                         "Python keywords like: 'if', 'from', etc. "
                         "are not allowed, use 'if_', 'from_' instead.",
                         err_ctx.exception.args[0])

    def test_it_raises_an_error_creating_with_a_key_that_is_a_keyword(self):
        with self.assertRaises(ValueError) as err_ctx:
            bunch({'if': 1})

        self.assertEqual("Invalid key: 'if'. Only letters, "
                         "natural numbers, underline char allowed. "
                         "The first char can not be a number. "
                         "Python keywords like: 'if', 'from', etc. "
                         "are not allowed, use 'if_', 'from_' instead.",
                         err_ctx.exception.args[0])

    def test_access_to_the__class__attr(self):
        d = bunch({'a': 1})

        self.assertEqual('bunch', d.__class__.__name__)

    def test_access_to_the__dict__attr(self):
        d = bunch({'a': 1})

        self.assertDictEqual({'a': 1}, d.__dict__)

    def test_issubclass(self):
        self.assertTrue(issubclass(bunch, dict))

    def test_is_instance(self):
        d = bunch({'a': 1})

        self.assertTrue(isinstance(d, dict))

    def test_iteration_simple(self):
        d = bunch({'a': 1, 'b': 2, 'c': 3})
        lst = list(sorted(d))

        self.assertListEqual(['a', 'b', 'c'], lst)

    def test_iteration_by_items(self):
        d = bunch({'a': 1, 'b': 2, 'c': 3})
        lst = list(sorted((k, v) for k, v in d.items()))

        self.assertListEqual([('a', 1), ('b', 2), ('c', 3)], lst)

    def test_iteration_by_keys(self):
        d = bunch({'a': 1, 'b': 2, 'c': 3})
        lst = list(sorted(d.keys()))

        self.assertListEqual(['a', 'b', 'c'], lst)

    def test_iteration_by_values(self):
        d = bunch({'a': 1, 'b': 2, 'c': 3})
        lst = list(sorted(d.values()))

        self.assertListEqual([1, 2, 3], lst)

    def test_it_creates_from_dict_with_allowed_keys(self):
        d = bunch({
            '_protected': 1,
            '_TestCase__private': 'yay!',
            '__private': 2,
            '__magic__': 3,
            'number123': 4,
            'False_': 5,
            'None_': 6,
            'True_': 7,
            'and_': 8,
            'as_': 9,
            'assert_': 10,
            'break_': 11,
            'class_': 12,
            'continue_': 13,
            'def_': 14,
            'del_': 15,
            'elif_': 16,
            'else_': 17,
            'except_': 18,
            'finally_': 19,
            'for_': 20,
            'from_': 21,
            'global_': 22,
            'if_': 23,
            'import_': 24,
            'in_': 25,
            'is_': 26,
            'lambda_': 27,
            'nonlocal_': 28,
            'not_': 29,
            'or_': 30,
            'pass_': 31,
            'raise_': 32,
            'return_': 33,
            'try_': 34,
            'while_': 35,
            'with_': 36,
            'yield_': 37,
            'id': 38,
            'async_': 39,
            'property': 40,
            'staticmethod': 41,
            'classmethod': 42,
            'all': 43,
            'any': 44,
            'map': 45,
            'filter': 46,
            'int': 47,
            'str': 48,
        })

        self.assertEqual(1, d._protected)
        self.assertEqual(2, d['__private'])  # TODO: should we allow private?
        self.assertEqual('yay!', d.__private)
        self.assertEqual(3, d.__magic__)
        self.assertEqual(4, d.number123)
        self.assertEqual(5, d.False_)
        self.assertEqual(6, d.None_)
        self.assertEqual(7, d.True_)
        self.assertEqual(8, d.and_)
        self.assertEqual(9, d.as_)
        self.assertEqual(10, d.assert_)
        self.assertEqual(11, d.break_)
        self.assertEqual(12, d.class_)
        self.assertEqual(13, d.continue_)
        self.assertEqual(14, d.def_)
        self.assertEqual(15, d.del_)
        self.assertEqual(16, d.elif_)
        self.assertEqual(17, d.else_)
        self.assertEqual(18, d.except_)
        self.assertEqual(19, d.finally_)
        self.assertEqual(20, d.for_)
        self.assertEqual(21, d.from_)
        self.assertEqual(22, d.global_)
        self.assertEqual(23, d.if_)
        self.assertEqual(24, d.import_)
        self.assertEqual(25, d.in_)
        self.assertEqual(26, d.is_)
        self.assertEqual(27, d.lambda_)
        self.assertEqual(28, d.nonlocal_)
        self.assertEqual(29, d.not_)
        self.assertEqual(30, d.or_)
        self.assertEqual(31, d.pass_)
        self.assertEqual(32, d.raise_)
        self.assertEqual(33, d.return_)
        self.assertEqual(34, d.try_)
        self.assertEqual(35, d.while_)
        self.assertEqual(36, d.with_)
        self.assertEqual(37, d.yield_)
        self.assertEqual(38, d.id)
        self.assertEqual(39, d.async_)
        self.assertEqual(40, d.property)
        self.assertEqual(41, d.staticmethod)
        self.assertEqual(42, d.classmethod)
        self.assertEqual(43, d.all)
        self.assertEqual(44, d.any)
        self.assertEqual(45, d.map)
        self.assertEqual(46, d.filter)
        self.assertEqual(47, d.int)
        self.assertEqual(48, d.str)

    def test_it_creates_from_allowed_kwargs(self):
        d = bunch(
            _protected=1,
            _TestCase__private='yay!',
            __private=2,
            __magic__=3,
            number123=4,
            False_=5,
            None_=6,
            True_=7,
            and_=8,
            as_=9,
            assert_=10,
            break_=11,
            class_=12,
            continue_=13,
            def_=14,
            del_=15,
            elif_=16,
            else_=17,
            except_=18,
            finally_=19,
            for_=20,
            from_=21,
            global_=22,
            if_=23,
            import_=24,
            in_=25,
            is_=26,
            lambda_=27,
            nonlocal_=28,
            not_=29,
            or_=30,
            pass_=31,
            raise_=32,
            return_=33,
            try_=34,
            while_=35,
            with_=36,
            yield_=37,
            id=38,
            async_=39,
            property=40,
            staticmethod=41,
            classmethod=42,
            all=43,
            any=44,
            map=45,
            filter=46,
            int=47,
            str=48,
        )

        self.assertEqual(1, d._protected)
        self.assertEqual(2, d['__private'])  # TODO: should we allow private?
        self.assertEqual('yay!', d.__private)
        self.assertEqual(3, d.__magic__)
        self.assertEqual(4, d.number123)
        self.assertEqual(5, d.False_)
        self.assertEqual(6, d.None_)
        self.assertEqual(7, d.True_)
        self.assertEqual(8, d.and_)
        self.assertEqual(9, d.as_)
        self.assertEqual(10, d.assert_)
        self.assertEqual(11, d.break_)
        self.assertEqual(12, d.class_)
        self.assertEqual(13, d.continue_)
        self.assertEqual(14, d.def_)
        self.assertEqual(15, d.del_)
        self.assertEqual(16, d.elif_)
        self.assertEqual(17, d.else_)
        self.assertEqual(18, d.except_)
        self.assertEqual(19, d.finally_)
        self.assertEqual(20, d.for_)
        self.assertEqual(21, d.from_)
        self.assertEqual(22, d.global_)
        self.assertEqual(23, d.if_)
        self.assertEqual(24, d.import_)
        self.assertEqual(25, d.in_)
        self.assertEqual(26, d.is_)
        self.assertEqual(27, d.lambda_)
        self.assertEqual(28, d.nonlocal_)
        self.assertEqual(29, d.not_)
        self.assertEqual(30, d.or_)
        self.assertEqual(31, d.pass_)
        self.assertEqual(32, d.raise_)
        self.assertEqual(33, d.return_)
        self.assertEqual(34, d.try_)
        self.assertEqual(35, d.while_)
        self.assertEqual(36, d.with_)
        self.assertEqual(37, d.yield_)
        self.assertEqual(38, d.id)
        self.assertEqual(39, d.async_)
        self.assertEqual(40, d.property)
        self.assertEqual(41, d.staticmethod)
        self.assertEqual(42, d.classmethod)
        self.assertEqual(43, d.all)
        self.assertEqual(44, d.any)
        self.assertEqual(45, d.map)
        self.assertEqual(46, d.filter)
        self.assertEqual(47, d.int)
        self.assertEqual(48, d.str)


if __name__ == '__main__':
    unittest.main()
