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

    def test_svn_unified_patch(self):
        with open('tests/casefiles/svn-unified.patch') as f:
            text = f.read()

        expected = [
                patch.diffobj(
                    header=patch.header(
                        index_path='bugtrace/trunk/src/bugtrace/csc.py',
                        old_path='bugtrace/trunk/src/bugtrace/csc.py',
                        old_version=12783,
                        new_path='bugtrace/trunk/src/bugtrace/csc.py',
                        new_version=12784,
                        ),
                    changes=[
                        (None, 1, '# This is a basic script I wrote to run Bugxplore over the dataset'),
                        (None, 2, ''),
                        (None, 3, ''),
                        (1, 4, 'import os'),
                        (2, 5, 'import sys'),
                        (3, 6, 'import pickle'),
                        (5, 8, 'import copy'),
                        (6, 9, ''),
                        (7, 10, 'from datetime import date'),
                        (8, None, 'from Main import main'),
                        (9, None, 'from Main import _make_dir'),
                        (None, 11, 'from Bugxplore import main'),
                        (None, 12, 'from Bugxplore import _make_dir'),
                        (10, 13, ''),
                        (11, 14, 'storageDir = \'/tmp/csc/bugs/\''),
                        (12, 15, 'argv = []'),
                        ]
                   ),
                patch.diffobj(
                    header=patch.header(
                        index_path='bugtrace/trunk/src/bugtrace/Diffxplore.py',
                        old_path='bugtrace/trunk/src/bugtrace/Diffxplore.py',
                        old_version=12783,
                        new_path='bugtrace/trunk/src/bugtrace/Diffxplore.py',
                        new_version=12784,
                        ),
                    changes=[
                        (46, 46, ''),
                        (47, 47, '    # Configure option parser'),
                        (48, 48, "    optparser = OptionParser(usage='%prog [options] DIFF_FILE', version='0.1')"),
                        (49, None, "    optparser.set_defaults(output_dir='/tmp/sctdiffs',project_name='default_project')"),
                        (None, 49, "    optparser.set_defaults(output_dir='/tmp/diffs')"),
                        (50, 50, "    optparser.add_option('-o', '--output-dir', dest='output_dir', help='Output directory')"),
                        (51, 51, "    optparser.add_option('-p', '--project_name', dest='project_name', help='Project name')"),
                        (52, 52, "    optparser.add_option('-d', '--delete_cvs_folder', dest='cvs_delete', help='Deletable CVS checkout folder')"),
                        (53, None, "    optparser.add_option('-a', '--append', action='store_true', dest='app', default=False, help='Append to existing MethTerms2 document')"),
                        (None, 53, ''),
                        (54, 54, '    # Invoke option parser'),
                        (55, 55, '    (options,args) = optparser.parse_args(argv)'),
                        (56, 56, ''),
                        ]
                    ),
                patch.diffobj(
                    header=patch.header(
                        index_path='bugtrace/trunk/src/bugtrace/Bugxplore.py',
                        old_path='bugtrace/trunk/src/bugtrace/Bugxplore.py',
                        old_version=12783,
                        new_path='bugtrace/trunk/src/bugtrace/Bugxplore.py',
                        new_version=12784,
                        ),
                    changes=[
                        (83, 83, ''),
                        (84, 84, '    # Configure option parser'),
                        (85, 85, "    optparser = OptionParser(usage='%prog [options] BUG_IDS', version='0.1')"),
                        (86, None, "    optparser.set_defaults(output_dir='/tmp/bugs',project_name='default_project')"),
                        (None, 86, "    optparser.set_defaults(output_dir='/tmp/bugs')"),
                        (87, 87, "    optparser.add_option('-u', '--bugzilla-url', dest='bugzilla_url', help='URL of Bugzilla installation root')"),
                        (88, 88, "    optparser.add_option('-o', '--output-dir', dest='output_dir', help='Output directory')"),
                        (89, 89, "    optparser.add_option('-p', '--project_name', dest='project_name', help='Project name')"),
                        (90, 90, "    optparser.add_option('-d', '--delete_cvs_folder', dest='cvs_delete', help='Deletable CVS checkout folder')"),
                        (91, None, "    optparser.add_option('-a', '--append', action='store_true', dest='app', default=False, help='Append to existing MethTerms2 document')"),
                        (None, 91, ''),
                        (92, 92, '    # Invoke option parser'),
                        (93, 93, '    (options,args) = optparser.parse_args(argv)'),
                        (94, 94, '    '),
                        ]
                    )
                    ]

        results = [x for x in patch.parse_patch(text)]

        assert results == expected

        with open('tests/casefiles/svn-context.patch') as f:
            text = f.read()
        results = [x for x in patch.parse_patch(text)]

        assert results == expected

    def test_svn_default_patch(self):
        expected = [
                patch.diffobj(
                    header=patch.header(
                        index_path = 'bugtrace/trunk/src/bugtrace/csc.py',
                        old_path='bugtrace/trunk/src/bugtrace/csc.py',
                        old_version=None,
                        new_path='bugtrace/trunk/src/bugtrace/csc.py',
                        new_version=None,
                        ),
                    changes=[
                        (None, 1, '# This is a basic script I wrote to run Bugxplore over the dataset'),
                        (None, 2, ''),
                        (None, 3, ''),
                        (8, None, 'from Main import main'),
                        (9, None, 'from Main import _make_dir'),
                        (None, 11, 'from Bugxplore import main'),
                        (None, 12, 'from Bugxplore import _make_dir'),
                        ]
                   ),
                patch.diffobj(
                    header=patch.header(
                        index_path = 'bugtrace/trunk/src/bugtrace/Diffxplore.py',
                        old_path='bugtrace/trunk/src/bugtrace/Diffxplore.py',
                        old_version=None,
                        new_path='bugtrace/trunk/src/bugtrace/Diffxplore.py',
                        new_version=None,
                        ),
                    changes=[
                        (49, None, "    optparser.set_defaults(output_dir='/tmp/sctdiffs',project_name='default_project')"),
                        (None, 49, "    optparser.set_defaults(output_dir='/tmp/diffs')"),
                        (53, None, "    optparser.add_option('-a', '--append', action='store_true', dest='app', default=False, help='Append to existing MethTerms2 document')"),
                        (None, 53, ''),
                        ]
                    ),
                patch.diffobj(
                    header=patch.header(
                        index_path = 'bugtrace/trunk/src/bugtrace/Bugxplore.py',
                        old_path='bugtrace/trunk/src/bugtrace/Bugxplore.py',
                        old_version=None,
                        new_path='bugtrace/trunk/src/bugtrace/Bugxplore.py',
                        new_version=None,
                        ),
                    changes=[
                        (86, None, "    optparser.set_defaults(output_dir='/tmp/bugs',project_name='default_project')"),
                        (None, 86, "    optparser.set_defaults(output_dir='/tmp/bugs')"),
                        (91, None, "    optparser.add_option('-a', '--append', action='store_true', dest='app', default=False, help='Append to existing MethTerms2 document')"),
                        (None, 91, ''),
                        ]
                    )
                    ]
        with open('tests/casefiles/svn-default.patch') as f:
            text = f.read()
        results = [x for x in patch.parse_patch(text)]
        assert results == expected

    def test_git_patch(self):
        with open('tests/casefiles/git.patch') as f:
            text = f.read()

        expected = [
                patch.diffobj(
                    header=patch.header(
                        index_path=None,
                        old_path='novel/src/java/edu/ua/eng/software/novel/NovelFrame.java',
                        old_version='aae63fe',
                        new_path='novel/src/java/edu/ua/eng/software/novel/NovelFrame.java',
                        new_version='5abbc99'
                        ),
                    changes=[
                        (135, 135, '    public void actionPerformed(ActionEvent e) {'),
                        (136, 136, ''),
                        (137, 137, '        if (e.getActionCommand().equals("OPEN")) {'),
                        (138, None, '            prefsDialog(prefs.getImportPane());'),
                        (None, 138, '            prefs.selectImportPane();'),
                        (None, 139, '            prefsDialog();'),
                        (139, 140, '        } else if (e.getActionCommand().equals("SET")) {'),
                        (140, None, '            prefsDialog(prefs.getRepoPane());'),
                        (None, 141, '            prefs.selectRepoPane();'),
                        (None, 142, '            prefsDialog();'),
                        (141, 143, '        } else if (e.getActionCommand().equals("PREFS"))'),
                        (142, 144, '            prefsDialog();'),
                        (143, 145, '        else if (e.getActionCommand().equals("EXIT"))'),
                        (158, 160, '     * Create dialog to handle user preferences'),
                        (159, 161, '     */'),
                        (160, 162, '    public void prefsDialog() {'),
                        (161, None, ''),
                        (162, 163, '        prefs.setVisible(true);'),
                        (163, 164, '    }'),
                        (164, 165, ''),
                        (165, None, '    public void prefsDialog(Component c) {'),
                        (166, None, '        prefs.setSelectedComponent(c);'),
                        (167, None, '        prefsDialog();'),
                        (168, None, '    }'),
                        (169, None, ''),
                        (170, 166, '    /**'),
                        (171, 167, '     * Open software tutorials, most likely to be hosted online'),
                        (172, 168, '     * ')]),
                    patch.diffobj(
                        header=patch.header(
                            index_path=None,
                            old_path='novel/src/java/edu/ua/eng/software/novel/NovelPrefPane.java',
                            old_version='a63b57e',
                            new_path='novel/src/java/edu/ua/eng/software/novel/NovelPrefPane.java',
                            new_version='919f413'
                            ),
                        changes=[
                            (18, 18, ''),
                            (19, 19, '    public abstract void apply();'),
                            (20, 20, ''),
                            (None, 21, '    public abstract void applyPrefs();'),
                            (None, 22, ''),
                            (21, 23, '    public abstract boolean isChanged();'),
                            (22, 24, ''),
                            (23, 25, '    protected Preferences prefs;')]
                        )
                    ]

        results = [x for x in patch.parse_patch(text)]

        assert results == expected


    def test_git_header(self):
        text = """
diff --git a/bugtrace/patch.py b/bugtrace/patch.py
index 8910dfd..456e34f 100644
--- a/bugtrace/patch.py
+++ b/bugtrace/patch.py
@@ -8,20 +8,30 @@
"""
        expected = patch.header(
                index_path = None,
                old_path = 'bugtrace/patch.py',
                old_version = '8910dfd',
                new_path = 'bugtrace/patch.py',
                new_version = '456e34f')

        results = patch.parse_git_header(text)
        assert results == expected

        results_main = patch.parse_scm_header(text)
        assert results_main == expected

    def test_svn_header(self):
        text = """
Index: bugtrace/trunk/src/bugtrace/csc.py
===================================================================
--- bugtrace/trunk/src/bugtrace/csc.py  (revision 12783)
+++ bugtrace/trunk/src/bugtrace/csc.py  (revision 12784)
@@ -1,3 +1,6 @@
"""
        expected = patch.header(
                index_path = 'bugtrace/trunk/src/bugtrace/csc.py',
                old_path = 'bugtrace/trunk/src/bugtrace/csc.py',
                old_version = 12783,
                new_path = 'bugtrace/trunk/src/bugtrace/csc.py',
                new_version = 12784)
        results = patch.parse_svn_header(text)
        assert results == expected

        results_main = patch.parse_scm_header(text)
        assert results_main == expected

    def test_cvs_header(self):
        text = """Index: org.eclipse.core.resources/src/org/eclipse/core/internal/localstore/SafeChunkyInputStream.java
===================================================================
RCS file: /cvsroot/eclipse/org.eclipse.core.resources/src/org/eclipse/core/internal/localstore/SafeChunkyInputStream.java,v
retrieving revision 1.6.4.1
retrieving revision 1.8
diff -u -r1.6.4.1 -r1.8
--- org.eclipse.core.resources/src/org/eclipse/core/internal/localstore/SafeChunkyInputStream.java	23 Jul 2001 17:51:45 -0000	1.6.4.1
+++ org.eclipse.core.resources/src/org/eclipse/core/internal/localstore/SafeChunkyInputStream.java	17 May 2002 20:27:56 -0000	1.8
@@ -1 +1 @@
"""
        expected = patch.header(
                index_path = 'org.eclipse.core.resources/src/org/eclipse/core/internal/localstore/SafeChunkyInputStream.java',
                old_path = 'org.eclipse.core.resources/src/org/eclipse/core/internal/localstore/SafeChunkyInputStream.java',
                old_version = '1.6.4.1',
                new_path = 'org.eclipse.core.resources/src/org/eclipse/core/internal/localstore/SafeChunkyInputStream.java',
                new_version = '1.8')
        results = patch.parse_cvs_header(text)
        print(expected)
        print('~~~~~~')
        print(results)
        assert results == expected

        results_main = patch.parse_scm_header(text)
        assert results_main == expected

    def test_unified_header(self):
        text = """--- /tmp/o  2012-12-22 06:43:35.000000000 -0600
+++ /tmp/n  2012-12-23 20:40:50.000000000 -0600
@@ -1,3 +1,9 @@"""

        expected = patch.header(
                index_path = None,
                old_path = '/tmp/o',
                old_version = '2012-12-22 06:43:35.000000000 -0600',
                new_path = '/tmp/n',
                new_version = '2012-12-23 20:40:50.000000000 -0600')

        results = patch.parse_unified_header(text)
        assert results == expected

        results_main = patch.parse_diff_header(text)
        assert results_main == expected


    def test_unified_diff(self):
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

    def test_context_header(self):
        text = """*** /tmp/o   2012-12-22 06:43:35.000000000 -0600
--- /tmp/n  2012-12-23 20:40:50.000000000 -0600
***************"""

        expected = patch.header(
                index_path = None,
                old_path = '/tmp/o',
                old_version = '2012-12-22 06:43:35.000000000 -0600',
                new_path = '/tmp/n',
                new_version = '2012-12-23 20:40:50.000000000 -0600')

        results = patch.parse_context_header(text)
        assert results == expected

        results_main = patch.parse_diff_header(text)
        assert results_main == expected


    def test_context_diff(self):
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
