import unittest

from src import whatthepatch as wtp


class TestRenameOnlyPaths(unittest.TestCase):
    def _check_rename_paths(self, old_path, new_path):
        text = (
            "diff --git a/{old} b/{new}\n"
            "similarity index 100%\n"
            "rename from {old}\n"
            "rename to {new}\n"
        ).format(old=old_path, new=new_path)
        diffs = list(wtp.parse_patch(text))
        self.assertEqual(len(diffs), 1)
        diff = diffs[0]
        self.assertIsNone(diff.changes)
        self.assertEqual(
            (diff.header.old_path, diff.header.new_path), (old_path, new_path)
        )

    @unittest.expectedFailure
    def test_rename_only_removes_git_prefixes(self):
        self._check_rename_paths("before.txt", "after.txt")

    @unittest.expectedFailure
    def test_rename_only_preserves_real_a_and_b_directories(self):
        self._check_rename_paths("a/before.txt", "b/after.txt")

    def test_unified_paths_without_git_header_keep_a_and_b_directories(self):
        text = "--- a/a/before.txt\n+++ b/b/after.txt\n@@ -1 +1 @@\n-before\n+after\n"
        diffs = list(wtp.parse_patch(text))
        self.assertEqual(len(diffs), 1)
        self.assertEqual(
            (diffs[0].header.old_path, diffs[0].header.new_path),
            ("a/before.txt", "b/after.txt"),
        )
