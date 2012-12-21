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
> to this document.
"""
        expected = [
                (patch.DIFF.insert, None, 1, 'This is an important'),
                (patch.DIFF.insert, None, 2, 'notice! It should'),
                (patch.DIFF.insert, None, 3, 'therefore be located at'),
                (patch.DIFF.insert, None, 4, 'the beginning of this'),
                (patch.DIFF.insert, None, 5, 'document!'),
                (patch.DIFF.insert, None, 6, ''),

                (patch.DIFF.delete, 8, None, 'compress the size of the'),
                (patch.DIFF.delete, 9, None, 'changes.'),
                (patch.DIFF.delete, 10, None, ''),
                (patch.DIFF.delete, 11, None, 'This paragraph contains'),
                (patch.DIFF.delete, 12, None, 'text that is outdated.'),
                (patch.DIFF.delete, 13, None, 'It will be deleted in the'),
                (patch.DIFF.delete, 14, None, 'near future.'),
                (patch.DIFF.insert, None, 14, 'compress anything.'),

                (patch.DIFF.delete, 17, None, 'check this dokument. On'),
                (patch.DIFF.insert, None, 17, 'check this document. On'),

                (patch.DIFF.insert, None, 25, ''),
                (patch.DIFF.insert, None, 26, 'This paragraph contains'),
                (patch.DIFF.insert, None, 27, 'important new additions'),
                (patch.DIFF.insert, None, 28, 'to this document.')
                ]

        results = [x for x in patch.parse_default_diff(text)]

        assert results == expected


    def test_unified_diff(self):
        text = """--- /path/to/original   ''timestamp''
+++ /path/to/new        ''timestamp''
@@ -1,3 +1,9 @@
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
+to this document.
"""
        expected = [
                (patch.DIFF.insert, None, 1, 'This is an important'),
                (patch.DIFF.insert, None, 2, 'notice! It should'),
                (patch.DIFF.insert, None, 3, 'therefore be located at'),
                (patch.DIFF.insert, None, 4, 'the beginning of this'),
                (patch.DIFF.insert, None, 5, 'document!'),
                (patch.DIFF.insert, None, 6, ''),
                (patch.DIFF.equal, 1, 7, 'This part of the'),
                (patch.DIFF.equal, 2, 8, 'document has stayed the'),
                (patch.DIFF.equal, 3, 9, 'same from version to'),

                (patch.DIFF.equal, 5, 11, 'be shown if it doesn\'t'),
                (patch.DIFF.equal, 6, 12, 'change.  Otherwise, that'),
                (patch.DIFF.equal, 7, 13, 'would not be helping to'),
                (patch.DIFF.delete, 8, None, 'compress the size of the'),
                (patch.DIFF.delete, 9, None, 'changes.'),
                (patch.DIFF.delete, 10, None, ''),
                (patch.DIFF.delete, 11, None, 'This paragraph contains'),
                (patch.DIFF.delete, 12, None, 'text that is outdated.'),
                (patch.DIFF.delete, 13, None, 'It will be deleted in the'),
                (patch.DIFF.delete, 14, None, 'near future.'),
                (patch.DIFF.insert, None, 14, 'compress anything.'),
                (patch.DIFF.equal, 15, 15, ''),
                (patch.DIFF.equal, 16, 16, 'It is important to spell'),
                (patch.DIFF.delete, 17, None, 'check this dokument. On'),
                (patch.DIFF.insert, None, 17, 'check this document. On'),
                (patch.DIFF.equal, 18, 18, 'the other hand, a'),
                (patch.DIFF.equal, 19, 19, 'misspelled word isn\'t'),
                (patch.DIFF.equal, 20, 20, 'the end of the world.'),

                (patch.DIFF.equal, 22, 22, 'this paragraph needs to'),
                (patch.DIFF.equal, 23, 23, 'be changed. Things can'),
                (patch.DIFF.equal, 24, 24, 'be added after it.'),
                (patch.DIFF.insert, None, 25, ''),
                (patch.DIFF.insert, None, 26, 'This paragraph contains'),
                (patch.DIFF.insert, None, 27, 'important new additions'),
                (patch.DIFF.insert, None, 28, 'to this document.')
                ]

        results = [x for x in patch.parse_unified_diff(text)]

        assert results == expected

    def test_context_diff(self):
        text = """*** /path/to/original   ''timestamp''
--- /path/to/new        ''timestamp''
***************
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
+ to this document.
"""
        expected = [
                (patch.DIFF.insert, None, 1, 'This is an important'),
                (patch.DIFF.insert, None, 2, 'notice! It should'),
                (patch.DIFF.insert, None, 3, 'therefore be located at'),
                (patch.DIFF.insert, None, 4, 'the beginning of this'),
                (patch.DIFF.insert, None, 5, 'document!'),
                (patch.DIFF.insert, None, 6, ''),
                (patch.DIFF.equal, 1, 7, 'This part of the'),
                (patch.DIFF.equal, 2, 8, 'document has stayed the'),
                (patch.DIFF.equal, 3, 9, 'same from version to'),

                (patch.DIFF.equal, 5, 11, 'be shown if it doesn\'t'),
                (patch.DIFF.equal, 6, 12, 'change.  Otherwise, that'),
                (patch.DIFF.equal, 7, 13, 'would not be helping to'),
                (patch.DIFF.delete, 8, None, 'compress the size of the'),
                (patch.DIFF.delete, 9, None, 'changes.'),
                (patch.DIFF.delete, 10, None, ''),
                (patch.DIFF.delete, 11, None, 'This paragraph contains'),
                (patch.DIFF.delete, 12, None, 'text that is outdated.'),
                (patch.DIFF.delete, 13, None, 'It will be deleted in the'),
                (patch.DIFF.delete, 14, None, 'near future.'),
                (patch.DIFF.insert, None, 14, 'compress anything.'),
                (patch.DIFF.equal, 15, 15, ''),
                (patch.DIFF.equal, 16, 16, 'It is important to spell'),
                (patch.DIFF.delete, 17, None, 'check this dokument. On'),
                (patch.DIFF.insert, None, 17, 'check this document. On'),
                (patch.DIFF.equal, 18, 18, 'the other hand, a'),
                (patch.DIFF.equal, 19, 19, 'misspelled word isn\'t'),
                (patch.DIFF.equal, 20, 20, 'the end of the world.'),

                (patch.DIFF.equal, 22, 22, 'this paragraph needs to'),
                (patch.DIFF.equal, 23, 23, 'be changed. Things can'),
                (patch.DIFF.equal, 24, 24, 'be added after it.'),
                (patch.DIFF.insert, None, 25, ''),
                (patch.DIFF.insert, None, 26, 'This paragraph contains'),
                (patch.DIFF.insert, None, 27, 'important new additions'),
                (patch.DIFF.insert, None, 28, 'to this document.')
                ]

        results = [x for x in patch.parse_context_diff(text)]

        assert results == expected

    def test_ed_diff(self):
        text = """ 24a

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

 .
"""
        expected = [
                # ed you so cray
                (patch.DIFF.insert, None, 25, ''),
                (patch.DIFF.insert, None, 26, 'This paragraph contains'),
                (patch.DIFF.insert, None, 27, 'important new additions'),
                (patch.DIFF.insert, None, 28, 'to this document.'),

                (patch.DIFF.delete, 17, None, 'check this dokument. On'),
                (patch.DIFF.insert, None, 17, 'check this document. On'),

                (patch.DIFF.delete, 8, None, 'compress the size of the'),
                (patch.DIFF.delete, 9, None, 'changes.'),
                (patch.DIFF.delete, 10, None, ''),
                (patch.DIFF.delete, 11, None, 'This paragraph contains'),
                (patch.DIFF.delete, 12, None, 'text that is outdated.'),
                (patch.DIFF.delete, 13, None, 'It will be deleted in the'),
                (patch.DIFF.delete, 14, None, 'near future.'),
                (patch.DIFF.insert, None, 14, 'compress anything.'),

                (patch.DIFF.insert, None, 1, 'This is an important'),
                (patch.DIFF.insert, None, 2, 'notice! It should'),
                (patch.DIFF.insert, None, 3, 'therefore be located at'),
                (patch.DIFF.insert, None, 4, 'the beginning of this'),
                (patch.DIFF.insert, None, 5, 'document!'),
                (patch.DIFF.insert, None, 6, '')
                ]

        results = [x for x in patch.parse_ed_diff(text)]

        assert results == expected

if __name__ == '__main__':
    unittest.main()
