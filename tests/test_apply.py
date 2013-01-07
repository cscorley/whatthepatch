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
            self.lao = f.read().split('\n')

        with open('tests/casefiles/tzu') as f:
            self.tzu = f.read().split('\n')

    def test_truth(self):
        assert type(self.lao) == list
        assert type(self.tzu) == list
        assert len(self.lao) == 12
        assert len(self.tzu) == 14

    def test_diff_default(self):
        with open('tests/casefiles/diff-default.diff') as f:
            diff_text = f.read()

        diff = [x for x in whatthepatch.parse_patch(diff_text)]
        diff = diff[0]

        new_text = apply.apply_diff(diff, self.lao)
        assert new_text == self.tzu

    def test_diff_context(self):
        with open('tests/casefiles/diff-context.diff') as f:
            diff_text = f.read()

        diff = [x for x in whatthepatch.parse_patch(diff_text)]
        diff = diff[0]

        new_text = apply.apply_diff(diff, self.lao)
        assert new_text == self.tzu

    def test_diff_unified(self):
        with open('tests/casefiles/diff-unified.diff') as f:
            diff_text = f.read()

        diff = [x for x in whatthepatch.parse_patch(diff_text)]
        diff = diff[0]

        new_text = apply.apply_diff(diff, self.lao)
        assert new_text == self.tzu

    def test_diff_unified_patchutil(self):
        with open('tests/casefiles/diff-unified.diff') as f:
            diff_text = f.read()

        diff = [x for x in whatthepatch.parse_patch(diff_text)]
        diff = diff[0]

        with self.assertRaises(Exception):
            new_text = apply.apply_diff(diff, [''] + padded_lao, use_patch=True)

        new_text = apply.apply_diff(diff, self.lao, use_patch=True)
        assert new_text == self.tzu

    def test_diff_rcs(self):
        with open('tests/casefiles/diff-rcs.diff') as f:
            diff_text = f.read()

        diff = [x for x in whatthepatch.parse_patch(diff_text)]
        diff = diff[0]

        new_text = apply.apply_diff(diff, self.lao)
        assert new_text == self.tzu

    def test_diff_ed(self):
        with open('tests/casefiles/diff-ed.diff') as f:
            diff_text = f.read()

        diff = [x for x in whatthepatch.parse_patch(diff_text)]
        diff = diff[0]

        new_text = apply.apply_diff(diff, self.lao)
        assert new_text != self.tzu

        new_text = apply.apply_diff(diff, self.lao, use_patch=True)
        assert new_text == self.tzu

if __name__ == '__main__':
    unittest.main()
