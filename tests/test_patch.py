# -*- coding: utf-8 -*-

import os
import time
import unittest

from src import whatthepatch as wtp
from src.whatthepatch.patch import Change, diffobj
from src.whatthepatch.patch import header as headerobj

module_path = os.path.dirname(__file__)


def datapath(fname):
    return os.path.join(module_path, "casefiles", fname)


def indent(amount, changes):
    indent_str = " " * amount
    return [(l, r, indent_str + t if t else t) for (l, r, t) in changes]


CSC_CHANGES = [
    (
        None,
        1,
        "# This is a basic script I wrote to run Bugxplore over the dataset",
    ),
    (None, 2, ""),
    (None, 3, ""),
    (1, 4, "import os"),
    (2, 5, "import sys"),
    (3, 6, "import pickle"),
    (5, 8, "import copy"),
    (6, 9, ""),
    (7, 10, "from datetime import date"),
    (8, None, "from Main import main"),
    (9, None, "from Main import _make_dir"),
    (None, 11, "from Bugxplore import main"),
    (None, 12, "from Bugxplore import _make_dir"),
    (10, 13, ""),
    (11, 14, "storageDir = '/tmp/csc/bugs/'"),
    (12, 15, "argv = []"),
]

DIFFXPLORE_CHANGES = indent(
    4,
    [
        (46, 46, ""),
        (47, 47, "# Configure option parser"),
        (
            48,
            48,
            "optparser = OptionParser(usage='%prog [options] DIFF_FILE', "
            "version='0.1')",
        ),
        (
            49,
            None,
            "optparser.set_defaults(output_dir='/tmp/sctdiffs',"
            "project_name='default_project')",
        ),
        (None, 49, "optparser.set_defaults(output_dir='/tmp/diffs')"),
        (
            50,
            50,
            "optparser.add_option('-o', '--output-dir', dest='output_dir', "
            "help='Output directory')",
        ),
        (
            51,
            51,
            "optparser.add_option('-p', '--project_name', "
            "dest='project_name', help='Project name')",
        ),
        (
            52,
            52,
            "optparser.add_option('-d', '--delete_cvs_folder', "
            "dest='cvs_delete', help='Deletable CVS checkout folder')",
        ),
        (
            53,
            None,
            "optparser.add_option('-a', '--append', action='store_true', "
            "dest='app', default=False, "
            "help='Append to existing MethTerms2 document')",
        ),
        (None, 53, ""),
        (54, 54, "# Invoke option parser"),
        (55, 55, "(options,args) = optparser.parse_args(argv)"),
        (56, 56, ""),
    ],
)

BUGXPLORE_CHANGES = indent(
    4,
    [
        (83, 83, ""),
        (84, 84, "# Configure option parser"),
        (
            85,
            85,
            "optparser = OptionParser(usage='%prog [options] BUG_IDS', "
            "version='0.1')",
        ),
        (
            86,
            None,
            "optparser.set_defaults(output_dir='/tmp/bugs',"
            "project_name='default_project')",
        ),
        (None, 86, "optparser.set_defaults(output_dir='/tmp/bugs')"),
        (
            87,
            87,
            "optparser.add_option('-u', '--bugzilla-url', "
            "dest='bugzilla_url', help='URL of Bugzilla installation root')",
        ),
        (
            88,
            88,
            "optparser.add_option('-o', '--output-dir', dest='output_dir', "
            "help='Output directory')",
        ),
        (
            89,
            89,
            "optparser.add_option('-p', '--project_name', "
            "dest='project_name', help='Project name')",
        ),
        (
            90,
            90,
            "optparser.add_option('-d', '--delete_cvs_folder', "
            "dest='cvs_delete', help='Deletable CVS checkout folder')",
        ),
        (
            91,
            None,
            "optparser.add_option('-a', '--append', action='store_true', "
            "dest='app', default=False, "
            "help='Append to existing MethTerms2 document')",
        ),
        (None, 91, ""),
        (92, 92, "# Invoke option parser"),
        (93, 93, "(options,args) = optparser.parse_args(argv)"),
    ],
) + [(94, 94, "    ")]


class PatchTestSuite(unittest.TestCase):
    def assert_diffs_equal(self, a, b):
        def _process_change(c):
            return (c.old, c.new, c.line)

        def _process_diffobj(d):
            changes = d.changes or []
            return d._replace(changes=[_process_change(c) for c in changes])

        def _process(d_or_c):
            if isinstance(d_or_c, list):
                return [_process(o) for o in d_or_c]
            if isinstance(d_or_c, diffobj):
                return _process_diffobj(d_or_c)
            if isinstance(d_or_c, Change):
                return _process_change(d_or_c)
            return d_or_c

        return self.assertEqual(_process(a), b)

    def test_default_diff(self):
        with open(datapath("diff-default.diff")) as f:
            text = f.read()

        expected = [
            (1, None, "The Way that can be told of is not the eternal Way;"),
            (2, None, "The name that can be named is not the eternal name."),
            (4, None, "The Named is the mother of all things."),
            (None, 2, "The named is the mother of all things."),
            (None, 3, ""),
            (None, 11, "They both may be called deep and profound."),
            (None, 12, "Deeper and more profound,"),
            (None, 13, "The door of all subtleties!"),
        ]

        results = list(wtp.patch.parse_default_diff(text))
        self.assert_diffs_equal(results, expected)

        expected_main = [diffobj(header=None, changes=expected, text=text)]
        results_main = list(wtp.patch.parse_patch(text))
        self.assert_diffs_equal(results_main, expected_main)

    def test_svn_unified_patch(self):
        with open("tests/casefiles/svn-unified.patch") as f:
            text = f.read()

        lines = text.splitlines()

        expected = [
            diffobj(
                header=headerobj(
                    index_path="bugtrace/trunk/src/bugtrace/csc.py",
                    old_path="bugtrace/trunk/src/bugtrace/csc.py",
                    old_version=12783,
                    new_path="bugtrace/trunk/src/bugtrace/csc.py",
                    new_version=12784,
                ),
                changes=CSC_CHANGES,
                text="\n".join(lines[:22]) + "\n",
            ),
            diffobj(
                header=headerobj(
                    index_path="bugtrace/trunk/src/bugtrace/Diffxplore.py",
                    old_path="bugtrace/trunk/src/bugtrace/Diffxplore.py",
                    old_version=12783,
                    new_path="bugtrace/trunk/src/bugtrace/Diffxplore.py",
                    new_version=12784,
                ),
                changes=DIFFXPLORE_CHANGES,
                text="\n".join(lines[22:40]) + "\n",
            ),
            diffobj(
                header=headerobj(
                    index_path="bugtrace/trunk/src/bugtrace/Bugxplore.py",
                    old_path="bugtrace/trunk/src/bugtrace/Bugxplore.py",
                    old_version=12783,
                    new_path="bugtrace/trunk/src/bugtrace/Bugxplore.py",
                    new_version=12784,
                ),
                changes=BUGXPLORE_CHANGES,
                text="\n".join(lines[40:]) + "\n",
            ),
        ]

        results = list(wtp.parse_patch(text))

        self.assert_diffs_equal(results, expected)

    def test_svn_context_patch(self):
        with open("tests/casefiles/svn-context.patch") as f:
            text = f.read()

        lines = text.splitlines()

        expected = [
            diffobj(
                header=headerobj(
                    index_path="bugtrace/trunk/src/bugtrace/csc.py",
                    old_path="bugtrace/trunk/src/bugtrace/csc.py",
                    old_version=12783,
                    new_path="bugtrace/trunk/src/bugtrace/csc.py",
                    new_version=12784,
                ),
                changes=CSC_CHANGES,
                text="\n".join(lines[:32]) + "\n",
            ),
            diffobj(
                header=headerobj(
                    index_path="bugtrace/trunk/src/bugtrace/Diffxplore.py",
                    old_path="bugtrace/trunk/src/bugtrace/Diffxplore.py",
                    old_version=12783,
                    new_path="bugtrace/trunk/src/bugtrace/Diffxplore.py",
                    new_version=12784,
                ),
                changes=DIFFXPLORE_CHANGES,
                text="\n".join(lines[32:61]) + "\n",
            ),
            diffobj(
                header=headerobj(
                    index_path="bugtrace/trunk/src/bugtrace/Bugxplore.py",
                    old_path="bugtrace/trunk/src/bugtrace/Bugxplore.py",
                    old_version=12783,
                    new_path="bugtrace/trunk/src/bugtrace/Bugxplore.py",
                    new_version=12784,
                ),
                changes=BUGXPLORE_CHANGES,
                text="\n".join(lines[61:]) + "\n",
            ),
        ]

        results = list(wtp.parse_patch(text))

        self.assert_diffs_equal(results, expected)

    def test_svn_git_patch(self):
        with open("tests/casefiles/svn-git.patch") as f:
            text = f.read()

        lines = text.splitlines()

        csc_diff = diffobj(
            header=headerobj(
                index_path="bugtrace/trunk/src/bugtrace/csc.py",
                old_path="projects/bugs/bugtrace/trunk/src/bugtrace/csc.py",
                old_version=12783,
                new_path="projects/bugs/bugtrace/trunk/src/bugtrace/csc.py",
                new_version=12784,
            ),
            changes=CSC_CHANGES,
            text="\n".join(lines[:23]) + "\n",
        )

        diffxplore_path = "bugtrace/trunk/src/bugtrace/Diffxplore.py"
        diffxplore_diff = diffobj(
            header=headerobj(
                index_path=diffxplore_path,
                old_path="projects/bugs/" + diffxplore_path,
                old_version=12783,
                new_path="projects/bugs/" + diffxplore_path,
                new_version=12784,
            ),
            changes=DIFFXPLORE_CHANGES,
            text="\n".join(lines[23:42]) + "\n",
        )

        bugexplore_path = "bugtrace/trunk/src/bugtrace/Bugxplore.py"
        bugxplore_diff = diffobj(
            header=headerobj(
                index_path=bugexplore_path,
                old_path="projects/bugs/" + bugexplore_path,
                old_version=12783,
                new_path="projects/bugs/" + bugexplore_path,
                new_version=12784,
            ),
            changes=BUGXPLORE_CHANGES,
            text="\n".join(lines[42:]) + "\n",
        )

        expected = [csc_diff, diffxplore_diff, bugxplore_diff]

        results = list(wtp.parse_patch(text))

        self.assert_diffs_equal(results, expected)

    def test_svn_rcs_patch(self):
        with open("tests/casefiles/svn-rcs.patch") as f:
            text = f.read()

        lines = text.splitlines()

        csc_changes = [
            (
                None,
                1,
                "# This is a basic script I wrote to run " "Bugxplore over the dataset",
            ),
            (None, 2, ""),
            (None, 3, ""),
            (8, None, None),
            (9, None, None),
            (None, 11, "from Bugxplore import main"),
            (None, 12, "from Bugxplore import _make_dir"),
        ]

        diffxplore_changes = [
            (49, None, None),
            (None, 49, "    optparser.set_defaults(output_dir='/tmp/diffs')"),
            (53, None, None),
            (None, 53, ""),
        ]

        bugxplore_changes = [
            (86, None, None),
            (None, 86, "    optparser.set_defaults(output_dir='/tmp/bugs')"),
            (91, None, None),
            (None, 91, ""),
        ]

        expected = [
            diffobj(
                header=headerobj(
                    index_path="bugtrace/trunk/src/bugtrace/csc.py",
                    old_path="bugtrace/trunk/src/bugtrace/csc.py",
                    old_version=None,
                    new_path="bugtrace/trunk/src/bugtrace/csc.py",
                    new_version=None,
                ),
                changes=csc_changes,
                text="\n".join(lines[:10]) + "\n",
            ),
            diffobj(
                header=headerobj(
                    index_path="bugtrace/trunk/src/bugtrace/Diffxplore.py",
                    old_path="bugtrace/trunk/src/bugtrace/Diffxplore.py",
                    old_version=None,
                    new_path="bugtrace/trunk/src/bugtrace/Diffxplore.py",
                    new_version=None,
                ),
                changes=diffxplore_changes,
                text="\n".join(lines[10:18]) + "\n",
            ),
            diffobj(
                header=headerobj(
                    index_path="bugtrace/trunk/src/bugtrace/Bugxplore.py",
                    old_path="bugtrace/trunk/src/bugtrace/Bugxplore.py",
                    old_version=None,
                    new_path="bugtrace/trunk/src/bugtrace/Bugxplore.py",
                    new_version=None,
                ),
                changes=bugxplore_changes,
                text="\n".join(lines[18:]) + "\n",
            ),
        ]

        results = list(wtp.parse_patch(text))
        self.assert_diffs_equal(results, expected)

    def test_svn_default_patch(self):
        with open("tests/casefiles/svn-default.patch") as f:
            text = f.read()

        lines = text.splitlines()

        csc_changes = [
            (
                None,
                1,
                "# This is a basic script I wrote to run " "Bugxplore over the dataset",
            ),
            (None, 2, ""),
            (None, 3, ""),
            (8, None, "from Main import main"),
            (9, None, "from Main import _make_dir"),
            (None, 11, "from Bugxplore import main"),
            (None, 12, "from Bugxplore import _make_dir"),
        ]

        diffxplore_changes = indent(
            4,
            [
                (
                    49,
                    None,
                    "optparser.set_defaults(output_dir='/tmp/sctdiffs',"
                    "project_name='default_project')",
                ),
                (None, 49, "optparser.set_defaults(output_dir='/tmp/diffs')"),
                (
                    53,
                    None,
                    "optparser.add_option('-a', '--append', "
                    "action='store_true', dest='app', default=False, "
                    "help='Append to existing MethTerms2 document')",
                ),
                (None, 53, ""),
            ],
        )

        bugxplore_changes = indent(
            4,
            [
                (
                    86,
                    None,
                    "optparser.set_defaults(output_dir='/tmp/bugs',"
                    "project_name='default_project')",
                ),
                (None, 86, "optparser.set_defaults(output_dir='/tmp/bugs')"),
                (
                    91,
                    None,
                    "optparser.add_option('-a', '--append', "
                    "action='store_true', dest='app', default=False, "
                    "help='Append to existing MethTerms2 document')",
                ),
                (None, 91, ""),
            ],
        )

        expected = [
            diffobj(
                header=headerobj(
                    index_path="bugtrace/trunk/src/bugtrace/csc.py",
                    old_path="bugtrace/trunk/src/bugtrace/csc.py",
                    old_version=None,
                    new_path="bugtrace/trunk/src/bugtrace/csc.py",
                    new_version=None,
                ),
                changes=csc_changes,
                text="\n".join(lines[:12]) + "\n",
            ),
            diffobj(
                header=headerobj(
                    index_path="bugtrace/trunk/src/bugtrace/Diffxplore.py",
                    old_path="bugtrace/trunk/src/bugtrace/Diffxplore.py",
                    old_version=None,
                    new_path="bugtrace/trunk/src/bugtrace/Diffxplore.py",
                    new_version=None,
                ),
                changes=diffxplore_changes,
                text="\n".join(lines[12:22]) + "\n",
            ),
            diffobj(
                header=headerobj(
                    index_path="bugtrace/trunk/src/bugtrace/Bugxplore.py",
                    old_path="bugtrace/trunk/src/bugtrace/Bugxplore.py",
                    old_version=None,
                    new_path="bugtrace/trunk/src/bugtrace/Bugxplore.py",
                    new_version=None,
                ),
                changes=bugxplore_changes,
                text="\n".join(lines[22:]) + "\n",
            ),
        ]
        results = list(wtp.parse_patch(text))
        self.assert_diffs_equal(results, expected)

    def test_git_patch(self):
        with open("tests/casefiles/git.patch") as f:
            text = f.read()

        lines = text.splitlines()

        novel_frame_changes = indent(
            4,
            [
                (135, 135, "public void actionPerformed(ActionEvent e) {"),
                (136, 136, ""),
                (137, 137, '    if (e.getActionCommand().equals("OPEN")) {'),
                (138, None, "        prefsDialog(prefs.getImportPane());"),
                (None, 138, "        prefs.selectImportPane();"),
                (None, 139, "        prefsDialog();"),
                (139, 140, '    } else if (e.getActionCommand().equals("SET")) {'),
                (140, None, "        prefsDialog(prefs.getRepoPane());"),
                (None, 141, "        prefs.selectRepoPane();"),
                (None, 142, "        prefsDialog();"),
                (141, 143, '    } else if (e.getActionCommand().equals("PREFS"))'),
                (142, 144, "        prefsDialog();"),
                (143, 145, '    else if (e.getActionCommand().equals("EXIT"))'),
                (158, 160, " * Create dialog to handle user preferences"),
                (159, 161, " */"),
                (160, 162, "public void prefsDialog() {"),
                (161, None, ""),
                (162, 163, "    prefs.setVisible(true);"),
                (163, 164, "}"),
                (164, 165, ""),
                (165, None, "public void prefsDialog(Component c) {"),
                (166, None, "    prefs.setSelectedComponent(c);"),
                (167, None, "    prefsDialog();"),
                (168, None, "}"),
                (169, None, ""),
                (170, 166, "/**"),
                (
                    171,
                    167,
                    " * Open software tutorials, " "most likely to be hosted online",
                ),
                (172, 168, " * "),
            ],
        )

        novel_frame_path = "novel/src/java/edu/ua/eng/software/novel/NovelFrame.java"
        novel_frame = diffobj(
            header=headerobj(
                index_path=None,
                old_path=novel_frame_path,
                old_version="aae63fe",
                new_path=novel_frame_path,
                new_version="5abbc99",
            ),
            changes=novel_frame_changes,
            text="\n".join(lines[:34]) + "\n",
        )

        novel_pref_frame_path = (
            "novel/src/java/edu/ua/eng/software/novel/NovelPrefPane.java"
        )

        novel_pref_frame = diffobj(
            header=headerobj(
                index_path=None,
                old_path=novel_pref_frame_path,
                old_version="a63b57e",
                new_path=novel_pref_frame_path,
                new_version="919f413",
            ),
            changes=[
                (18, 18, ""),
                (19, 19, "    public abstract void apply();"),
                (20, 20, ""),
                (None, 21, "    public abstract void applyPrefs();"),
                (None, 22, ""),
                (21, 23, "    public abstract boolean isChanged();"),
                (22, 24, ""),
                (23, 25, "    protected Preferences prefs;"),
            ],
            text="\n".join(lines[34:]) + "\n",
        )

        expected = [novel_frame, novel_pref_frame]

        results = list(wtp.parse_patch(text))

        self.assert_diffs_equal(results, expected)

    def test_git_oneline_add(self):
        with open("tests/casefiles/git-oneline-add.diff") as f:
            text = f.read()

        lines = text.splitlines()

        expected = [
            diffobj(
                header=headerobj(
                    index_path=None,
                    old_path="/dev/null",
                    old_version="0000000",
                    new_path="oneline.txt",
                    new_version="f56f98d",
                ),
                changes=[(None, 1, "Adding a one-line file.")],
                text="\n".join(lines[:34]) + "\n",
            )
        ]

        results = list(wtp.parse_patch(text))

        self.assert_diffs_equal(results, expected)

    def test_git_oneline_change(self):
        with open("tests/casefiles/git-oneline-change.diff") as f:
            text = f.read()

        lines = text.splitlines()

        expected = [
            diffobj(
                header=headerobj(
                    index_path=None,
                    old_path="oneline.txt",
                    old_version="f56f98d",
                    new_path="oneline.txt",
                    new_version="169ceeb",
                ),
                changes=[
                    (1, None, "Adding a one-line file."),
                    (None, 1, "Changed a one-line file."),
                ],
                text="\n".join(lines[:34]) + "\n",
            )
        ]

        results = list(wtp.parse_patch(text))
        self.assert_diffs_equal(results, expected)

    def test_git_oneline_rm(self):
        with open("tests/casefiles/git-oneline-rm.diff") as f:
            text = f.read()

        lines = text.splitlines()

        expected = [
            diffobj(
                header=headerobj(
                    index_path=None,
                    old_path="oneline.txt",
                    old_version="169ceeb",
                    new_path="/dev/null",
                    new_version="0000000",
                ),
                changes=[(1, None, "Changed a one-line file.")],
                text="\n".join(lines[:34]) + "\n",
            )
        ]

        results = list(wtp.parse_patch(text))
        self.assert_diffs_equal(results, expected)

    def test_git_new_empty_file(self):
        with open("tests/casefiles/git-new-empty-file.diff") as f:
            text = f.read()

        lines = text.splitlines()

        expected = [
            diffobj(
                header=headerobj(
                    index_path=None,
                    old_path="/dev/null",
                    old_version="0000000",
                    new_path="somefile.txt",
                    new_version="e69de29",
                ),
                changes=[],
                text="\n".join(lines[:34]) + "\n",
            )
        ]

        results = list(wtp.parse_patch(text))
        self.assert_diffs_equal(results, expected)

    def test_git_header(self):
        with open("tests/casefiles/git-header.diff") as f:
            text = f.read()

        expected = headerobj(
            index_path=None,
            old_path="bugtrace/patch.py",
            old_version="8910dfd",
            new_path="bugtrace/patch.py",
            new_version="456e34f",
        )

        results = wtp.patch.parse_git_header(text)
        self.assertEqual(results, expected)

        results_main = wtp.patch.parse_header(text)
        self.assertEqual(results_main, expected)

    def test_git_header_long(self):
        with open("tests/casefiles/git-header-long.diff") as f:
            text = f.read()

        expected = headerobj(
            index_path=None,
            old_path="bugtrace/patch.py",
            old_version="18910dfd",
            new_path="bugtrace/patch.py",
            new_version="2456e34f",
        )

        results = wtp.patch.parse_git_header(text)
        self.assertEqual(results, expected)

        results_main = wtp.patch.parse_header(text)
        self.assertEqual(results_main, expected)

    def test_git_binary_files(self):
        with open("tests/casefiles/git-binary-files.diff") as f:
            text = f.read()

        expected = headerobj(
            index_path=None,
            old_path="/dev/null",
            old_version="0000000",
            new_path="project/media/i/asc.gif",
            new_version="71e31ac",
        )

        results = wtp.patch.parse_git_header(text)
        self.assertEqual(results, expected)

        results_main = wtp.patch.parse_header(text)
        self.assertEqual(results_main, expected)

    def test_svn_header(self):
        with open("tests/casefiles/svn-header.diff") as f:
            text = f.read()

        expected = headerobj(
            index_path="bugtrace/trunk/src/bugtrace/csc.py",
            old_path="bugtrace/trunk/src/bugtrace/csc.py",
            old_version=12783,
            new_path="bugtrace/trunk/src/bugtrace/csc.py",
            new_version=12784,
        )
        results = wtp.patch.parse_svn_header(text)
        self.assertEqual(results, expected)

        results_main = wtp.patch.parse_header(text)
        self.assertEqual(results_main, expected)

    def test_cvs_header(self):
        with open("tests/casefiles/cvs-header.diff") as f:
            text = f.read()

        path = (
            "org.eclipse.core.resources"
            "/src/org/eclipse/core/internal/localstore/"
            "SafeChunkyInputStream.java"
        )

        expected = headerobj(
            index_path=path,
            old_path=path,
            old_version="1.6.4.1",
            new_path=path,
            new_version="1.8",
        )
        results = wtp.patch.parse_cvs_header(text)
        self.assertEqual(results, expected)

        results_main = wtp.patch.parse_header(text)
        self.assertEqual(results_main, expected)

    def test_unified_header(self):
        with open("tests/casefiles/unified-header.diff") as f:
            text = f.read()

        expected = headerobj(
            index_path=None,
            old_path="/tmp/o",
            old_version="2012-12-22 06:43:35.000000000 -0600",
            new_path="/tmp/n",
            new_version="2012-12-23 20:40:50.000000000 -0600",
        )

        results = wtp.patch.parse_unified_header(text)
        self.assertEqual(results, expected)

        results_main = wtp.patch.parse_header(text)
        self.assertEqual(results_main, expected)

    def test_unified_header_notab(self):
        with open("tests/casefiles/unified-header-notab.diff") as f:
            text = f.read()

        expected = headerobj(
            index_path=None,
            old_path="/tmp/some file",
            old_version="2012-12-22 06:43:35.000000000 -0600",
            new_path="/tmp/n",
            new_version="2012-12-23 20:40:50.000000000 -0600",
        )

        results = wtp.patch.parse_unified_header(text)
        self.assertEqual(results, expected)

        results_main = wtp.patch.parse_header(text)
        self.assertEqual(results_main, expected)

    def test_unified_diff(self):
        with open(datapath("diff-unified.diff")) as f:
            text = f.read()

        # off with your head!
        text_diff = "\n".join(text.splitlines()[2:]) + "\n"

        expected = [
            (1, None, "The Way that can be told of is not the eternal Way;"),
            (2, None, "The name that can be named is not the eternal name."),
            (3, 1, "The Nameless is the origin of Heaven and Earth;"),
            (4, None, "The Named is the mother of all things."),
            (None, 2, "The named is the mother of all things."),
            (None, 3, ""),
            (5, 4, "Therefore let there always be non-being,"),
            (6, 5, "  so we may see their subtlety,"),
            (7, 6, "And let there always be being,"),
            (9, 8, "The two are the same,"),
            (10, 9, "But after they are produced,"),
            (11, 10, "  they have different names."),
            (None, 11, "They both may be called deep and profound."),
            (None, 12, "Deeper and more profound,"),
            (None, 13, "The door of all subtleties!"),
        ]

        results = list(wtp.patch.parse_unified_diff(text_diff))
        self.assert_diffs_equal(results, expected)

        expected_main = diffobj(
            header=headerobj(
                index_path=None,
                old_path="lao",
                old_version="2013-01-05 16:56:19.000000000 -0600",
                new_path="tzu",
                new_version="2013-01-05 16:56:35.000000000 -0600",
            ),
            changes=expected,
            text=text,
        )
        results_main = next(wtp.patch.parse_patch(text))
        self.assert_diffs_equal(results_main, expected_main)

    def test_unified2_diff(self):
        with open(datapath("diff-unified2.diff")) as f:
            text = f.read()

        # off with your head!
        text_diff = "\n".join(text.splitlines()[2:]) + "\n"

        expected = [
            (None, 2, "The named is the mother of all things."),
        ]

        results = list(wtp.patch.parse_unified_diff(text_diff))
        self.assert_diffs_equal(results, expected)

        expected_main = diffobj(
            header=headerobj(
                index_path=None,
                old_path="abc",
                old_version="2013-01-05 16:56:19.000000000 -0600",
                new_path="efg",
                new_version="2013-01-05 16:56:35.000000000 -0600",
            ),
            changes=expected,
            text=text,
        )
        results_main = next(wtp.patch.parse_patch(text))
        self.assert_diffs_equal(results_main, expected_main)

    def test_diff_unified_with_does_not_include_extra_lines(self):
        with open("tests/casefiles/diff-unified-blah.diff") as f:
            text = f.read()

        changes = [
            (1, None, "The Way that can be told of is not the eternal Way;"),
            (2, None, "The name that can be named is not the eternal name."),
            (3, 1, "The Nameless is the origin of Heaven and Earth;"),
            (4, None, "The Named is the mother of all things."),
            (None, 2, "The named is the mother of all things."),
            (None, 3, ""),
            (5, 4, "Therefore let there always be non-being,"),
            (6, 5, "  so we may see their subtlety,"),
            (7, 6, "And let there always be being,"),
            (9, 8, "The two are the same,"),
            (10, 9, "But after they are produced,"),
            (11, 10, "  they have different names."),
            (None, 11, "They both may be called deep and profound."),
            (None, 12, "Deeper and more profound,"),
            (None, 13, "The door of all subtleties!"),
        ]

        expected = [
            diffobj(
                header=headerobj(
                    index_path=None,
                    old_path="lao",
                    old_version="2013-01-05 16:56:19.000000000 -0600",
                    new_path="tzu",
                    new_version="2013-01-05 16:56:35.000000000 -0600",
                ),
                changes=changes,
                text=text,
            )
        ]

        results = list(wtp.patch.parse_patch(text))
        self.assert_diffs_equal(results, expected)

    def test_diff_context_with_does_not_include_extra_lines(self):
        with open("tests/casefiles/diff-context-blah.diff") as f:
            text = f.read()

        changes = [
            (1, None, "The Way that can be told of is not the eternal Way;"),
            (2, None, "The name that can be named is not the eternal name."),
            (3, 1, "The Nameless is the origin of Heaven and Earth;"),
            (4, None, "The Named is the mother of all things."),
            (None, 2, "The named is the mother of all things."),
            (None, 3, ""),
            (5, 4, "Therefore let there always be non-being,"),
            (6, 5, "  so we may see their subtlety,"),
            (7, 6, "And let there always be being,"),
            (9, 8, "The two are the same,"),
            (10, 9, "But after they are produced,"),
            (11, 10, "  they have different names."),
            (None, 11, "They both may be called deep and profound."),
            (None, 12, "Deeper and more profound,"),
            (None, 13, "The door of all subtleties!"),
        ]

        expected = [
            diffobj(
                header=headerobj(
                    index_path=None,
                    old_path="lao",
                    old_version="2013-01-05 16:56:19.000000000 -0600",
                    new_path="tzu",
                    new_version="2013-01-05 16:56:35.000000000 -0600",
                ),
                changes=changes,
                text=text,
            )
        ]

        results = list(wtp.patch.parse_patch(text))
        self.assert_diffs_equal(results, expected)

    def test_diff_default_with_does_not_include_extra_lines(self):
        with open("tests/casefiles/diff-default-blah.diff") as f:
            text = f.read()

        changes = [
            (1, None, "The Way that can be told of is not the eternal Way;"),
            (2, None, "The name that can be named is not the eternal name."),
            (4, None, "The Named is the mother of all things."),
            (None, 2, "The named is the mother of all things."),
            (None, 3, ""),
            (None, 11, "They both may be called deep and profound."),
            (None, 12, "Deeper and more profound,"),
            (None, 13, "The door of all subtleties!"),
        ]

        expected = [diffobj(header=None, changes=changes, text=text)]

        results = list(wtp.patch.parse_patch(text))
        self.assert_diffs_equal(results, expected)

    def test_context_header(self):
        with open("tests/casefiles/context-header.diff") as f:
            text = f.read()

        expected = headerobj(
            index_path=None,
            old_path="/tmp/o",
            old_version="2012-12-22 06:43:35.000000000 -0600",
            new_path="/tmp/n",
            new_version="2012-12-23 20:40:50.000000000 -0600",
        )

        results = wtp.patch.parse_context_header(text)
        self.assertEqual(results, expected)

        results_main = wtp.patch.parse_header(text)
        self.assertEqual(results_main, expected)

    def test_context_diff(self):
        with open(datapath("diff-context.diff")) as f:
            text = f.read()

        # off with your head!
        text_diff = "\n".join(text.splitlines()[2:]) + "\n"

        expected = [
            (1, None, "The Way that can be told of is not the eternal Way;"),
            (2, None, "The name that can be named is not the eternal name."),
            (3, 1, "The Nameless is the origin of Heaven and Earth;"),
            (4, None, "The Named is the mother of all things."),
            (None, 2, "The named is the mother of all things."),
            (None, 3, ""),
            (5, 4, "Therefore let there always be non-being,"),
            (6, 5, "  so we may see their subtlety,"),
            (7, 6, "And let there always be being,"),
            (9, 8, "The two are the same,"),
            (10, 9, "But after they are produced,"),
            (11, 10, "  they have different names."),
            (None, 11, "They both may be called deep and profound."),
            (None, 12, "Deeper and more profound,"),
            (None, 13, "The door of all subtleties!"),
        ]

        results = list(wtp.patch.parse_context_diff(text_diff))
        self.assert_diffs_equal(results, expected)

        expected_main = diffobj(
            header=headerobj(
                index_path=None,
                old_path="lao",
                old_version="2013-01-05 16:56:19.000000000 -0600",
                new_path="tzu",
                new_version="2013-01-05 16:56:35.000000000 -0600",
            ),
            changes=expected,
            text=text,
        )
        results_main = next(wtp.patch.parse_patch(text))
        self.assert_diffs_equal(results_main, expected_main)

    def test_context_diff_issue39(self):
        with open(datapath("issue39-bash42-003.patch")) as f:
            text = f.read()

        # off with your head!
        text_diff = "\n".join(text.splitlines()[2:]) + "\n"

        expected = [
            (295, 331, "\t\t{"),
            (296, 332, "\t\t  pat++;"),
            (None, 333, "\t\t  bracklen++;"),
            (
                297,
                334,
                "\t\t  if (*pat == ']')\t/* right bracket can appear as equivalence class "
                "*/",
            ),
            (298, None, "\t\t    pat++;"),
            (None, 335, "\t\t    {"),
            (None, 336, "\t\t      pat++;"),
            (None, 337, "\t\t      bracklen++;"),
            (None, 338, "\t\t    }"),
            (299, 339, "\t\t  in_equiv = 1;"),
        ]

        results = list(wtp.patch.parse_context_diff(text_diff))
        self.assert_diffs_equal(results, expected)

        expected_main = diffobj(
            header=headerobj(
                index_path=None,
                old_path="../bash-4.2-patched/lib/glob/gmisc.c",
                old_version="2011-02-05 16:11:17.000000000 -0500",
                new_path="lib/glob/gmisc.c",
                new_version="2011-02-18 23:53:42.000000000 -0500",
            ),
            changes=expected,
            text=text,
        )
        results_main = next(wtp.patch.parse_patch(text))
        self.assert_diffs_equal(results_main, expected_main)

    def test_ed_diff(self):
        with open(datapath("diff-ed.diff")) as f:
            text = f.read()

        expected = [
            (1, None, None),
            (2, None, None),
            (4, None, None),
            (None, 2, "The named is the mother of all things."),
            (None, 3, ""),
            (None, 11, "They both may be called deep and profound."),
            (None, 12, "Deeper and more profound,"),
            (None, 13, "The door of all subtleties!"),
        ]

        results = list(wtp.patch.parse_ed_diff(text))
        self.assert_diffs_equal(results, expected)

        expected_main = [diffobj(header=None, changes=expected, text=text)]
        results_main = list(wtp.patch.parse_patch(text))
        self.assert_diffs_equal(results_main, expected_main)

    def test_rcs_diff(self):
        with open(datapath("diff-rcs.diff")) as f:
            text = f.read()

        expected = [
            (1, None, None),
            (2, None, None),
            (4, None, None),
            (None, 2, "The named is the mother of all things."),
            (None, 3, ""),
            (None, 11, "They both may be called deep and profound."),
            (None, 12, "Deeper and more profound,"),
            (None, 13, "The door of all subtleties!"),
        ]

        results = list(wtp.patch.parse_rcs_ed_diff(text))
        self.assert_diffs_equal(results, expected)

        expected_main = [diffobj(header=None, changes=expected, text=text)]
        results_main = list(wtp.patch.parse_patch(text))
        self.assert_diffs_equal(results_main, expected_main)

    def test_embedded_diff_in_comment(self):
        with open("tests/casefiles/embedded-diff.comment") as f:
            text = f.read()

        changes = indent(
            10,
            [
                (2182, 2182, "case Token.GETELEM:"),
                (2183, 2183, "    decompileElementGet((ElementGet) node);"),
                (2184, 2184, "    break;"),
                (None, 2185, "case Token.THIS:"),
                (None, 2186, "    decompiler.addToken(node.getType());"),
                (None, 2187, "    break;"),
                (2185, 2188, "default:"),
                (2186, 2189, '    Kit.codeBug("unexpected token: "'),
                (2187, 2190, "                " "+ Token.typeToName(node.getType()));"),
            ],
        )

        expected = [
            diffobj(
                header=headerobj(
                    index_path=None,
                    old_path="src/org/mozilla/javascript/IRFactory.java",
                    old_version=None,
                    new_path="src/org/mozilla/javascript/IRFactory.java",
                    new_version=None,
                ),
                changes=changes,
                text=text,
            )
        ]

        results = list(wtp.patch.parse_patch(text))
        self.assert_diffs_equal(results, expected)

    def test_mozilla_527452_5_comment(self):
        with open("tests/casefiles/mozilla-527452-5.comment") as f:
            text = f.read()

        lines = text.splitlines()
        path = (
            "js_instrumentation_proxy/src/org/mozilla/"
            "javascript/ast/StringLiteral.java"
        )
        header = headerobj(
            index_path=path,
            old_path=path,
            old_version=5547,
            new_path=path,
            new_version=None,
        )

        changes = indent(
            8,
            [
                (
                    112,
                    112,
                    "// TODO(stevey):  make sure this unescapes " "everything properly",
                ),
                (113, 113, "String q = String.valueOf(getQuoteCharacter());"),
                (114, 114, r'String rep = "\\\\" + q;'),
                (115, None, "String s = value.replaceAll(q, rep);"),
                (None, 115, r'String s = value.replace("\\", "\\\\");'),
                (None, 116, "s = s.replaceAll(q, rep);"),
                (116, 117, r's = s.replaceAll("\n", "\\\\n");'),
                (117, 118, r's = s.replaceAll("\r", "\\\\r");'),
                (118, 119, r's = s.replaceAll("\t", "\\\\t");'),
            ],
        )
        text = "\n".join(lines[2:]) + "\n"

        expected = [diffobj(header=header, changes=changes, text=text)]

        results = list(wtp.patch.parse_patch(text))
        self.assert_diffs_equal(results, expected)

    def test_dos_unified_cvs(self):
        with open("tests/casefiles/mozilla-560291.diff") as f:
            text = f.read()

        path = "src/org/mozilla/javascript/ast/ArrayComprehensionLoop.java"
        lines = text.splitlines()
        header = headerobj(
            index_path=path,
            old_path=path,
            old_version="1.1",
            new_path=path,
            new_version="15 Sep 2011 02:26:05 -0000",
        )

        expected = [
            diffobj(
                header=header,
                changes=[
                    (79, 79, "    @Override"),
                    (80, 80, "    public String toSource(int depth) {"),
                    (81, 81, "        return makeIndent(depth)"),
                    (82, None, '                + " for ("'),
                    (None, 82, '                + " for " '),
                    (None, 83, '                + (isForEach()?"each ":"")'),
                    (None, 84, '                + "("'),
                    (83, 85, "                + iterator.toSource(0)"),
                    (84, 86, '                + " in "'),
                    (85, 87, "                + iteratedObject.toSource(0)"),
                ],
                text="\n".join(lines[2:]) + "\n",
            )
        ]

        results = list(wtp.patch.parse_patch(text))
        self.assert_diffs_equal(results, expected)

    def test_old_style_cvs(self):
        with open("tests/casefiles/mozilla-252983.diff") as f:
            text = f.read()

        changes = [
            (
                1,
                None,
                "This file version: $Id: CHANGELOG,v 1.1.1.1 "
                "2007/01/25 15:59:02 inonit Exp $",
            ),
            (
                None,
                1,
                "This file version: $Id: CHANGELOG,v 1.1 "
                "2007/01/25 15:59:02 inonit Exp $",
            ),
            (2, 2, ""),
            (3, 3, "Changes since Rhino 1.6R5"),
            (4, 4, "========================="),
        ]

        expected = [
            diffobj(
                header=headerobj(
                    index_path="mozilla/js/rhino/CHANGELOG",
                    old_path="mozilla/js/rhino/CHANGELOG",
                    old_version="1.1.1.1",
                    new_path="mozilla/js/rhino/CHANGELOG",
                    new_version="1.1",  # or 'Thu Jan 25 10:59:02 2007'
                ),
                changes=changes,
                text=text,
            )
        ]

        results = wtp.patch.parse_cvs_header(text)
        self.assertEqual(results, expected[0].header)

        results = wtp.patch.parse_header(text)
        self.assertEqual(results, expected[0].header)

        results = list(wtp.patch.parse_patch(text))
        self.assert_diffs_equal(results, expected)

    def test_mozilla_252983_versionless(self):
        with open("tests/casefiles/mozilla-252983-versionless.diff") as f:
            text = f.read()

        changes = [
            (
                1,
                None,
                "This file version: $Id: CHANGELOG,v 1.1.1.1 "
                "2007/01/25 15:59:02 inonit Exp $",
            ),
            (
                None,
                1,
                "This file version: $Id: CHANGELOG,v 1.1 "
                "2007/01/25 15:59:02 inonit Exp $",
            ),
            (2, 2, ""),
            (3, 3, "Changes since Rhino 1.6R5"),
            (4, 4, "========================="),
        ]

        expected = [
            diffobj(
                header=headerobj(
                    index_path="mozilla/js/rhino/CHANGELOG",
                    old_path="mozilla/js/rhino/CHANGELOG",
                    old_version=None,
                    new_path="mozilla/js/rhino/CHANGELOG",
                    new_version=None,
                ),
                changes=changes,
                text=text,
            )
        ]

        results = wtp.patch.parse_header(text)
        self.assertEqual(results, expected[0].header)

        results = list(wtp.patch.parse_patch(text))
        self.assert_diffs_equal(results, expected)

    def test_apache_attachment_2241(self):
        with open("tests/casefiles/apache-attachment-2241.diff") as f:
            text = f.read()

        lines = text.splitlines()

        header = headerobj(
            index_path=None,
            old_path=(
                r"src\main\org\apache\tools\ant" r"\taskdefs\optional\pvcs\Pvcs.orig"
            ),
            old_version="Sat Jun 22 16:11:58 2002",
            new_path=(
                r"src\main\org\apache\tools\ant" r"\taskdefs\optional\pvcs\Pvcs.java"
            ),
            new_version="Fri Jun 28 10:55:50 2002",
        )

        changes = [
            (91, 91, " *"),
            (
                92,
                92,
                ' * @author <a href="mailto:tchristensen@nordija.com">'
                "Thomas Christensen</a>",
            ),
            (
                93,
                93,
                ' * @author <a href="mailto:donj@apogeenet.com">' "Don Jeffery</a>",
            ),
            (
                94,
                None,
                ' * @author <a href="snewton@standard.com">' "Steven E. Newton</a>",
            ),
            (
                None,
                94,
                ' * @author <a href="mailto:snewton@standard.com">'
                "Steven E. Newton</a>",
            ),
            (95, 95, " */"),
            (96, 96, "public class Pvcs extends org.apache.tools.ant.Task {"),
            (97, 97, "    private String pvcsbin;"),
        ]

        text = "\n".join(lines) + "\n"

        expected = [diffobj(header=header, changes=changes, text=text)]

        results = list(wtp.patch.parse_patch(text))
        self.assert_diffs_equal(results, expected)

    def test_space_in_path_header(self):
        with open("tests/casefiles/eclipse-attachment-126343.header") as f:
            text = f.read()

        expected = headerobj(
            index_path=(
                "test plugin/org/eclipse/jdt/debug/testplugin/"
                "ResumeBreakpointListener.java"
            ),
            old_path="/dev/null",
            old_version="1 Jan 1970 00:00:00 -0000",
            new_path=(
                "test plugin/org/eclipse/jdt/debug/testplugin/"
                "ResumeBreakpointListener.java"
            ),
            new_version="1 Jan 1970 00:00:00 -0000",
        )

        results = wtp.patch.parse_header(text)
        self.assertEqual(results, expected)

    def test_svn_mixed_line_ends(self):
        with open("tests/casefiles/svn-mixed_line_ends.patch") as f:
            text = f.read()

        expected_header = headerobj(
            index_path=("java/org/apache/catalina/loader/WebappClassLoader.java"),
            old_path="java/org/apache/catalina/loader/WebappClassLoader.java",
            old_version=1346371,
            new_path="java/org/apache/catalina/loader/WebappClassLoader.java",
            new_version=None,
        )

        results = list(wtp.patch.parse_patch(text))
        self.assertEqual(results[0].header, expected_header)

    def test_huge_patch(self):
        start_time = time.time()
        text = """diff --git a/huge.file b/huge.file
index 0000000..1111111 100644
--- a/huge.file
+++ a/huge.file
@@ -3,13 +3,1000007 @@
 00000000
 11111111
 22222222
-33333333
-44444444
+55555555
+66666666
"""
        for n in range(0, 1000000):
            text += "+" + hex(n) + "\n"
        result = list(wtp.patch.parse_patch(text))
        self.assertEqual(1, len(result))
        self.assertEqual(1000007, len(result[0].changes))
        # This is 2x the usual time for CI to allow for some slow tests
        # Really all we care about is that this parses faster than it used to (200s+)
        self.assertGreater(20, time.time() - start_time)

    def test_git_bin_patch(self):
        text = """---
 fox.bin   | Bin 0 -> 44 bytes
 fox.txt   |   2 +-
 lorem.bin | Bin 0 -> 446 bytes
 lorem.zip | Bin 431 -> 432 bytes
 4 files changed, 1 insertion(+), 1 deletion(-)
 create mode 100644 fox.bin
 create mode 100644 lorem.bin

diff --git a/fox.bin b/fox.bin
new file mode 100644
index 0000000000000000000000000000000000000000..e7683ad05fd121a9ca86cab5a827d471d29b4d4f
GIT binary patch
literal 44
ycmWH^NL45-%}mZ#NGi%N&r?XtuTaP;%`GTa$S+GRQYZmR=Ok8DDx~D6GXMZ<wh!6>

literal 0
HcmV?d00001

diff --git a/fox.txt b/fox.txt
index ff3bb63..8fe2a4b 100644
--- a/fox.txt
+++ b/fox.txt
@@ -1 +1 @@
-The quick brown fox jumps over the lazy dog
\ No newline at end of file
+The quick brown fox jumps over the lazy dog.
\ No newline at end of file
diff --git a/lorem.bin b/lorem.bin
new file mode 100644
index 0000000000000000000000000000000000000000..aef2724fd9ff72caf4eb1ac8333f0b5b322d82fb
GIT binary patch
literal 446
zcmXw#&2d992!vD07T|eRB)42s0Fkh>Gy1ax9+w~Fm)wMaW%v8+Q!6-@SL9y$#G*l}
z+6Ae%rODKMLNW(eV!J^Lqq#K40+haL&oHecme~?Bvp0hqihPGW)J|zdm0J@?;oarH
zmq8nAXrppJ9#KlY;O<;#ecAL3ed<g!G4=*8MQZA&@*d*izVwphh+(LN@fx1`86ZyC
zf%h#bZVFBhPiIy(OdV5yv}K(UJU$-1_=s~Fb|NWsEk$A}|AZot<LWnxp>0DLGNbT$
z;NzKem<F)LV9-+%O)-~zFiWULtcEc=v$joflZvCs%aENL{d#4hAnVe(yS0~XLpC4=
Lj`hdY>+$vrMRcVJ

literal 0
HcmV?d00001

diff --git a/lorem.zip b/lorem.zip
index 0f6beb70488e2b29fcaadf724b6f48ef0ab5bc4e..3c8a65bf1a97bb4180c83a0e31352b4edb4c245e 100644
GIT binary patch
delta 275
zcmZ3_yn#6)z?+#xgn@y9gP}7+C2a4}O*1$c85s5gF(-ozLr#8CYOY>MMM-D~Cj+xl
z?ABymATF)oW?*D_!OXw_CQK(BEOa*HaEZRjWV65P$+T=Pg^u?VBeY_ymt>hupAyrM
zu_ldGFZao&vTKV}cPYzE-4`VHX!@1~7xxOUc%}T}z;fqZ+pf4>{#%je`L@mdh12$@
z##~QSCtp2z)oM{#R?hTKa+j9=zO;TxpG;eTRQ}78>li9e@lU*`!E<hhw&gFg7Dwam
z8SImV7?t(so$}Jyl=3cb^RC<rY)d+m{}%R^{b303W@M6M#^TAz$&AWOMzNDS7!}#P
Jfj(wn0067{YH|Po

delta 274
zcmdnMyq-BCz?+#xgn@y9gW*b=N|;w+e?B`S1H&F5=46mz$jL8C&DATZC<zVWWMKXf
zwKe%I5SLbPGcdBeU}j(d6Q&am7CIYpxJ2J%vRS9J^XV)mjz|9|Mrg$d2bs?H_R@1O
z3ERvx-K;3mI{Tu~UBN!DcuoF~-cc7`ykS}Oi(}X0%ZjnlS&LuR*=$}?c38P&;q6b7
zte+;GeDx$tHc;Din|CGu%S*K{!-L%UoHcs4e@O{%uz6ZO@ty`xpT$&}TIoXzX1boS
zo-D+utS58IOJh^YyS&Z2axbtg=}i7x*!zt+z?+dtjv0#|C#NtfGku7f+{viO<^}XH
G0|Nj=Vq`=B

-- 
2.25.1
"""
        result = list(wtp.patch.parse_patch(text))
        assert result
        assert len(result) == 4
        assert (
            result[0].changes[0].line
            == b"The quick brown fox jumps over the lazy dog\x00"
        )
        assert (
            result[1].changes[0].line == "The quick brown fox jumps over the lazy dog"
        )
        assert (
            result[1].changes[1].line == "The quick brown fox jumps over the lazy dog."
        )
        assert (
            result[2].changes[0].line
            == b"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt"
            b" ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco"
            b" laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit"
            b" in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat"
            b" cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\x00"
        )
        assert len(result[3].changes) == 0


if __name__ == "__main__":
    unittest.main()
