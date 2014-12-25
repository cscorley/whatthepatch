# -*- coding: utf-8 -*-

import whatthepatch as wtp


import unittest
from io import StringIO

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

    def test_diff_unified_patchutil(self):
        with open('tests/casefiles/diff-unified.diff') as f:
            diff_text = f.read()

        diff = next(wtp.parse_patch(diff_text))

        new_text = wtp.apply.apply_diff(diff, self.lao, use_patch=True)
        self.assertEqual(new_text, (self.tzu, None))

        self.assertRaises(AssertionError, wtp.apply.apply_diff, diff, [''] + self.lao, use_patch=True)

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
        self.assertEqual(self.tzu,new_text)

        new_text = wtp.apply.apply_diff(diff, self.lao, use_patch=True)
        self.assertEqual(new_text, (self.tzu, None))

if __name__ == '__main__':
    unittest.main()
