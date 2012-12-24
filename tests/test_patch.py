# -*- coding: utf-8 -*-
# test_basic.py

from context import whatthepatch

from whatthepatch import patch

import unittest
from io import StringIO

class PatchTestSuite(unittest.TestCase):

    def test_default_diff(self):
        text = """0a1,6
> This is an important
> notice! It should
> therefore be located at
> the beginning of this
> document!
> 
8,14c14
< compress the size of the
< changes.
< 
< This paragraph contains
< text that is outdated.
< It will be deleted in the
< near future.
---
> compress anything.
17c17
< check this dokument. On
---
> check this document. On
24a25,28
> 
> This paragraph contains
> important new additions
> to this document."""

        expected = [
                (None, 1, 'This is an important'),
                (None, 2, 'notice! It should'),
                (None, 3, 'therefore be located at'),
                (None, 4, 'the beginning of this'),
                (None, 5, 'document!'),
                (None, 6, ''),

                (8, None, 'compress the size of the'),
                (9, None, 'changes.'),
                (10, None, ''),
                (11, None, 'This paragraph contains'),
                (12, None, 'text that is outdated.'),
                (13, None, 'It will be deleted in the'),
                (14, None, 'near future.'),
                (None, 14, 'compress anything.'),

                (17, None, 'check this dokument. On'),
                (None, 17, 'check this document. On'),

                (None, 25, ''),
                (None, 26, 'This paragraph contains'),
                (None, 27, 'important new additions'),
                (None, 28, 'to this document.')
                ]

        results = [x for x in patch.parse_default_diff(text)]
        assert results == expected

        results_main = [x for x in patch.parse_diff(text)]
        assert results_main == expected


    def test_unified_diff(self):
        text = """--- /path/to/original   ''timestamp''
+++ /path/to/new        ''timestamp''
@@ -1,3 +1,9 @@
"""

        text = """@@ -1,3 +1,9 @@
+This is an important
+notice! It should
+therefore be located at
+the beginning of this
+document!
+
 This part of the
 document has stayed the
 same from version to
@@ -5,16 +11,10 @@
 be shown if it doesn't
 change.  Otherwise, that
 would not be helping to
-compress the size of the
-changes.
-
-This paragraph contains
-text that is outdated.
-It will be deleted in the
-near future.
+compress anything.
 
 It is important to spell
-check this dokument. On
+check this document. On
 the other hand, a
 misspelled word isn't
 the end of the world.
@@ -22,3 +22,7 @@
 this paragraph needs to
 be changed. Things can
 be added after it.
+
+This paragraph contains
+important new additions
+to this document."""

        expected = [
                (None, 1, 'This is an important'),
                (None, 2, 'notice! It should'),
                (None, 3, 'therefore be located at'),
                (None, 4, 'the beginning of this'),
                (None, 5, 'document!'),
                (None, 6, ''),
                (1, 7, 'This part of the'),
                (2, 8, 'document has stayed the'),
                (3, 9, 'same from version to'),

                (5, 11, 'be shown if it doesn\'t'),
                (6, 12, 'change.  Otherwise, that'),
                (7, 13, 'would not be helping to'),
                (8, None, 'compress the size of the'),
                (9, None, 'changes.'),
                (10, None, ''),
                (11, None, 'This paragraph contains'),
                (12, None, 'text that is outdated.'),
                (13, None, 'It will be deleted in the'),
                (14, None, 'near future.'),
                (None, 14, 'compress anything.'),
                (15, 15, ''),
                (16, 16, 'It is important to spell'),
                (17, None, 'check this dokument. On'),
                (None, 17, 'check this document. On'),
                (18, 18, 'the other hand, a'),
                (19, 19, 'misspelled word isn\'t'),
                (20, 20, 'the end of the world.'),

                (22, 22, 'this paragraph needs to'),
                (23, 23, 'be changed. Things can'),
                (24, 24, 'be added after it.'),
                (None, 25, ''),
                (None, 26, 'This paragraph contains'),
                (None, 27, 'important new additions'),
                (None, 28, 'to this document.')
                ]

        results = [x for x in patch.parse_unified_diff(text)]
        assert results == expected

        results_main = [x for x in patch.parse_diff(text)]
        assert results_main == expected

    def test_context_diff(self):
        text = """*** /path/to/original   ''timestamp''
--- /path/to/new        ''timestamp''
***************"""
        text = """***************
*** 1,3 ****
--- 1,9 ----
+ This is an important
+ notice! It should
+ therefore be located at
+ the beginning of this
+ document!
+ 
  This part of the
  document has stayed the
  same from version to
***************
*** 5,20 ****
  be shown if it doesn't
  change.  Otherwise, that
  would not be helping to
! compress the size of the
! changes.
! 
! This paragraph contains
! text that is outdated.
! It will be deleted in the
! near future.
  
  It is important to spell
! check this dokument. On
  the other hand, a
  misspelled word isn't
  the end of the world.
--- 11,20 ----
  be shown if it doesn't
  change.  Otherwise, that
  would not be helping to
! compress anything.
  
  It is important to spell
! check this document. On
  the other hand, a
  misspelled word isn't
  the end of the world.
***************
*** 22,24 ****
--- 22,28 ----
  this paragraph needs to
  be changed. Things can
  be added after it.
+ 
+ This paragraph contains
+ important new additions
+ to this document."""

        expected = [
                (None, 1, 'This is an important'),
                (None, 2, 'notice! It should'),
                (None, 3, 'therefore be located at'),
                (None, 4, 'the beginning of this'),
                (None, 5, 'document!'),
                (None, 6, ''),
                (1, 7, 'This part of the'),
                (2, 8, 'document has stayed the'),
                (3, 9, 'same from version to'),

                # merge the two sections of the hunk so that deletions
                # are followed by the appropriate insertion
                # follow up: that was a horrible idea.
                (5, 11, 'be shown if it doesn\'t'),
                (6, 12, 'change.  Otherwise, that'),
                (7, 13, 'would not be helping to'),
                (8, None, 'compress the size of the'),
                (9, None, 'changes.'),
                (10, None, ''),
                (11, None, 'This paragraph contains'),
                (12, None, 'text that is outdated.'),
                (13, None, 'It will be deleted in the'),
                (14, None, 'near future.'),
                (None, 14, 'compress anything.'),
                (15, 15, ''),
                (16, 16, 'It is important to spell'),
                (17, None, 'check this dokument. On'),
                (None, 17, 'check this document. On'),
                (18, 18, 'the other hand, a'),
                (19, 19, 'misspelled word isn\'t'),
                (20, 20, 'the end of the world.'),

                (22, 22, 'this paragraph needs to'),
                (23, 23, 'be changed. Things can'),
                (24, 24, 'be added after it.'),
                (None, 25, ''),
                (None, 26, 'This paragraph contains'),
                (None, 27, 'important new additions'),
                (None, 28, 'to this document.')
                ]

        results = [x for x in patch.parse_context_diff(text)]
        assert results == expected

        results_main = [x for x in patch.parse_diff(text)]
        assert results_main == expected

    def test_ed_diff(self):
        text = """24a

This paragraph contains
important new additions
to this document.
.
17c
check this document. On
.
8,14c
compress anything.
.
0a
This is an important
notice! It should
therefore be located at
the beginning of this
document!

."""
        expected = [
                # ed, you so cray
                (None, 25, ''),
                (None, 26, 'This paragraph contains'),
                (None, 27, 'important new additions'),
                (None, 28, 'to this document.'),

                (17, None, None),
                (None, 17, 'check this document. On'),

                # ed, aka the lossy diff format.
                (8, None, None),
                (9, None, None),
                (10, None, None),
                (11, None, None),
                (12, None, None),
                (13, None, None),
                (14, None, None),

                # This is 14 in the other formats, because we are aware
                # of the previous changes (incoming blow), which add
                # the 6 lines (8+6=14)
                (None, 8, 'compress anything.'),

                # But, not in ed.

                (None, 1, 'This is an important'),
                (None, 2, 'notice! It should'),
                (None, 3, 'therefore be located at'),
                (None, 4, 'the beginning of this'),
                (None, 5, 'document!'),
                (None, 6, '')
                ]

        results = [x for x in patch.parse_ed_diff(text)]
        assert results == expected

        results_main = [x for x in patch.parse_diff(text)]
        assert results_main == expected

    def test_rcs_ed_diff(self):
        text="""a0 6
This is an important
notice! It should
therefore be located at
the beginning of this
document!

d8 7
a14 1
compress anything.
d17 1
a17 1
check this document. On
a24 4

This paragraph contains
important new additions
to this document."""

        expected = [
                (None, 1, 'This is an important'),
                (None, 2, 'notice! It should'),
                (None, 3, 'therefore be located at'),
                (None, 4, 'the beginning of this'),
                (None, 5, 'document!'),
                (None, 6, ''),

                (8, None, None),
                (9, None, None),
                (10, None, None),
                (11, None, None),
                (12, None, None),
                (13, None, None),
                (14, None, None),

                (None, 14, 'compress anything.'),

                (17, None, None),

                (None, 17, 'check this document. On'),

                (None, 25, ''),
                (None, 26, 'This paragraph contains'),
                (None, 27, 'important new additions'),
                (None, 28, 'to this document.')
                ]

        results = [x for x in patch.parse_rcs_ed_diff(text)]
        assert results == expected

        results_main = [x for x in patch.parse_diff(text)]
        assert results_main == expected


if __name__ == '__main__':
    unittest.main()
