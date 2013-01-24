# -*- coding: utf-8 -*-
# test_basic.py

from context import whatthepatch

from whatthepatch import apply

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
        self.assertEquals(type(self.lao), list)
        self.assertEquals(type(self.tzu), list)
        self.assertEquals(len(self.lao), 11)
        self.assertEquals(len(self.tzu), 13)

    def test_diff_default(self):
        with open('tests/casefiles/diff-default.diff') as f:
            diff_text = f.read()

        diff = [x for x in whatthepatch.parse_patch(diff_text)]
        diff = diff[0]

        new_text = apply.apply_diff(diff, self.lao)
        self.assertEquals(new_text, self.tzu)

    def test_diff_context(self):
        with open('tests/casefiles/diff-context.diff') as f:
            diff_text = f.read()

        diff = [x for x in whatthepatch.parse_patch(diff_text)]
        diff = diff[0]

        new_text = apply.apply_diff(diff, self.lao)
        self.assertEquals(new_text, self.tzu)

    def test_diff_unified(self):
        with open('tests/casefiles/diff-unified.diff') as f:
            diff_text = f.read()

        diff = [x for x in whatthepatch.parse_patch(diff_text)]
        diff = diff[0]

        new_text = apply.apply_diff(diff, self.lao)
        for e in self.tzu:
            print(e)
        print('~~~~')
        for e in new_text:
            print(e)

        self.assertEquals(new_text, self.tzu)

    def test_diff_unified_patchutil(self):
        with open('tests/casefiles/diff-unified.diff') as f:
            diff_text = f.read()

        diff = [x for x in whatthepatch.parse_patch(diff_text)]
        diff = diff[0]

        new_text = apply.apply_diff(diff, self.lao, use_patch=True)
        self.assertEquals(new_text, (self.tzu, None))

        self.assertRaises(AssertionError, apply.apply_diff, diff, [''] + self.lao, use_patch=True)

    def test_diff_rcs(self):
        with open('tests/casefiles/diff-rcs.diff') as f:
            diff_text = f.read()

        diff = [x for x in whatthepatch.parse_patch(diff_text)]
        diff = diff[0]

        new_text = apply.apply_diff(diff, self.lao)
        self.assertEquals(new_text, self.tzu)

    def test_diff_ed(self):
        self.maxDiff = None
        with open('tests/casefiles/diff-ed.diff') as f:
            diff_text = f.read()
        print(diff_text)
        print(diff_text.splitlines())

        diff = [x for x in whatthepatch.parse_patch(diff_text)]
        diff = diff[0]

        print(diff)
        new_text = apply.apply_diff(diff, self.lao)
        self.assertEquals(self.tzu,new_text)

        new_text = apply.apply_diff(diff, self.lao, use_patch=True)
        self.assertEquals(new_text, (self.tzu, None))

if __name__ == '__main__':
    unittest.main()
