# -*- coding: utf-8 -*-

import whatthepatch as wtp
from whatthepatch import exceptions

from nose.tools import assert_raises
import unittest


class ApplyTestSuite(unittest.TestCase):
    """Basic test cases."""

    def setUp(self):
        with open('tests/casefiles/lao') as f:
            self.lao = f.read().splitlines()

        with open('tests/casefiles/tzu') as f:
            self.tzu = f.read().splitlines()

    def test_truth(self):
        self.assertEqual(type(self.lao), list)
        self.assertEqual(type(self.tzu), list)
        self.assertEqual(len(self.lao), 11)
        self.assertEqual(len(self.tzu), 13)

    def test_diff_default(self):
        with open('tests/casefiles/diff-default.diff') as f:
            diff_text = f.read()

        diff = next(wtp.parse_patch(diff_text))

        new_text = wtp.apply.apply_diff(diff, self.lao)
        self.assertEqual(new_text, self.tzu)

    def test_diff_context(self):
        with open('tests/casefiles/diff-context.diff') as f:
            diff_text = f.read()

        diff = next(wtp.parse_patch(diff_text))

        new_text = wtp.apply.apply_diff(diff, self.lao)
        self.assertEqual(new_text, self.tzu)

    def test_diff_unified(self):
        with open('tests/casefiles/diff-unified.diff') as f:
            diff_text = f.read()

        diff = next(wtp.parse_patch(diff_text))

        new_text = wtp.apply.apply_diff(diff, self.lao)

        self.assertEqual(new_text, self.tzu)

    def test_diff_unified_bad(self):
        with open('tests/casefiles/diff-unified-bad.diff') as f:
            diff_text = f.read()

        diff = next(wtp.parse_patch(diff_text))

        with assert_raises(exceptions.ApplyException) as ec:
            wtp.apply.apply_diff(diff, self.lao)

        e = ec.exception
        e_str = str(e)
        assert 'line 4' in e_str
        assert 'The Named is the mother of all tings.' in e_str
        assert 'The Named is the mother of all things.' in e_str
        assert e.hunk == 1

    def test_diff_unified_bad2(self):
        with open('tests/casefiles/diff-unified-bad2.diff') as f:
            diff_text = f.read()

        diff = next(wtp.parse_patch(diff_text))

        with assert_raises(exceptions.ApplyException) as ec:
            wtp.apply.apply_diff(diff, self.lao)

        e = ec.exception
        e_str = str(e)
        assert 'line 9' in e_str
        assert 'The two are te same,' in e_str
        assert 'The two are the same,' in e_str
        assert e.hunk == 2

    def test_diff_unified_bad_backward(self):
        with open('tests/casefiles/diff-unified-bad2.diff') as f:
            diff_text = f.read()

        diff = next(wtp.parse_patch(diff_text))

        with assert_raises(exceptions.ApplyException) as ec:
            wtp.apply.apply_diff(diff, self.tzu)

        e = ec.exception
        e_str = str(e)
        assert 'line 1' in e_str
        assert 'The Way that can be told of is not the eternal Way;' in e_str
        assert 'The Nameless is the origin of Heaven and Earth;' in e_str
        assert e.hunk == 1

    def test_diff_unified_bad_empty_source(self):
        with open('tests/casefiles/diff-unified-bad2.diff') as f:
            diff_text = f.read()

        diff = next(wtp.parse_patch(diff_text))

        with assert_raises(exceptions.ApplyException) as ec:
            wtp.apply.apply_diff(diff, '')

        e = ec.exception
        e_str = str(e)
        assert 'line 1' in e_str
        assert 'The Way that can be told of is not the eternal Way;' in e_str
        assert 'does not exist in source'
        assert e.hunk == 1

    def test_diff_unified_patchutil(self):
        with open('tests/casefiles/diff-unified.diff') as f:
            diff_text = f.read()

        diff = next(wtp.parse_patch(diff_text))

        new_text = wtp.apply.apply_diff(diff, self.lao, use_patch=True)
        self.assertEqual(new_text, (self.tzu, None))

        self.assertRaises(
            exceptions.ApplyException,
            wtp.apply.apply_diff,
            diff,
            [''] + self.lao,
            use_patch=True,
        )

    def test_diff_rcs(self):
        with open('tests/casefiles/diff-rcs.diff') as f:
            diff_text = f.read()

        diff = next(wtp.parse_patch(diff_text))

        new_text = wtp.apply.apply_diff(diff, self.lao)
        self.assertEqual(new_text, self.tzu)

    def test_diff_ed(self):
        self.maxDiff = None
        with open('tests/casefiles/diff-ed.diff') as f:
            diff_text = f.read()

        diff = next(wtp.parse_patch(diff_text))

        new_text = wtp.apply.apply_diff(diff, self.lao)
        self.assertEqual(self.tzu, new_text)

        new_text = wtp.apply.apply_diff(diff, self.lao, use_patch=True)
        self.assertEqual(new_text, (self.tzu, None))


if __name__ == '__main__':
    unittest.main()
