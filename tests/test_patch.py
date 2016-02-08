# -*- coding: utf-8 -*-

import whatthepatch as wtp


import unittest
import os
from io import StringIO

module_path = os.path.dirname(__file__)
datapath = lambda fname: os.path.join(module_path, 'casefiles', fname)


class PatchTestSuite(unittest.TestCase):

    def test_default_diff(self):
        with open(datapath('diff-default.diff')) as f:
            text = f.read()

        expected = [
            (1, None,   'The Way that can be told of is not the eternal Way;'),
            (2, None,   'The name that can be named is not the eternal name.'),
            (4, None,   'The Named is the mother of all things.'),
            (None, 2,   'The named is the mother of all things.'),
            (None, 3,   ''),
            (None, 11,  'They both may be called deep and profound.'),
            (None, 12,  'Deeper and more profound,'),
            (None, 13,  'The door of all subtleties!')
        ]

        results = list(wtp.patch.parse_default_diff(text))
        self.assertEqual(results, expected)

        expected_main = [wtp.patch.diffobj(header=None, changes=expected, text=text)]
        results_main = list(wtp.patch.parse_patch(text))
        self.assertEqual(results_main, expected_main)

    def test_svn_unified_patch(self):
        with open('tests/casefiles/svn-unified.patch') as f:
            text = f.read()

        lines = text.splitlines()

        expected = [
                wtp.patch.diffobj(
                    header=wtp.patch.header(
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
                        ],
                    text = '\n'.join(lines[:22]) + '\n'
                   ),
                wtp.patch.diffobj(
                    header=wtp.patch.header(
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
                        ],
                    text = '\n'.join(lines[22:40]) + '\n'
                    ),
                wtp.patch.diffobj(
                    header=wtp.patch.header(
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
                        ],
                    text = '\n'.join(lines[40:]) + '\n'
                    )
                    ]

        results = list(wtp.parse_patch(text))

        self.assertEqual(results, expected)

    def test_svn_context_patch(self):
        with open('tests/casefiles/svn-context.patch') as f:
            text = f.read()

        lines = text.splitlines()

        expected = [
                wtp.patch.diffobj(
                    header=wtp.patch.header(
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
                        ],
                    text = '\n'.join(lines[:32]) + '\n'
                   ),
                wtp.patch.diffobj(
                    header=wtp.patch.header(
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
                        ],
                    text = '\n'.join(lines[32:61]) + '\n'
                    ),
                wtp.patch.diffobj(
                    header=wtp.patch.header(
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
                        ],
                    text = '\n'.join(lines[61:]) + '\n'
                    )
                    ]

        results = list(wtp.parse_patch(text))

        self.assertEqual(results, expected)

    def test_svn_git_patch(self):
        with open('tests/casefiles/svn-git.patch') as f:
            text = f.read()

        lines = text.splitlines()

        expected = [
                wtp.patch.diffobj(
                    header=wtp.patch.header(
                        index_path='bugtrace/trunk/src/bugtrace/csc.py',
                        old_path='projects/bugs/bugtrace/trunk/src/bugtrace/csc.py',
                        old_version=12783,
                        new_path='projects/bugs/bugtrace/trunk/src/bugtrace/csc.py',
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
                        ],
                    text = '\n'.join(lines[:23]) + '\n'
                   ),
                wtp.patch.diffobj(
                    header=wtp.patch.header(
                        index_path='bugtrace/trunk/src/bugtrace/Diffxplore.py',
                        old_path='projects/bugs/bugtrace/trunk/src/bugtrace/Diffxplore.py',
                        old_version=12783,
                        new_path='projects/bugs/bugtrace/trunk/src/bugtrace/Diffxplore.py',
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
                        ],
                    text = '\n'.join(lines[23:42]) + '\n'
                    ),
                wtp.patch.diffobj(
                    header=wtp.patch.header(
                        index_path='bugtrace/trunk/src/bugtrace/Bugxplore.py',
                        old_path='projects/bugs/bugtrace/trunk/src/bugtrace/Bugxplore.py',
                        old_version=12783,
                        new_path='projects/bugs/bugtrace/trunk/src/bugtrace/Bugxplore.py',
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
                        ],
                    text = '\n'.join(lines[42:]) + '\n'
                    )
                    ]


        results = list(wtp.parse_patch(text))

        self.assertEqual(results, expected)

    def test_svn_rcs_patch(self):
        with open('tests/casefiles/svn-rcs.patch') as f:
            text = f.read()

        lines = text.splitlines()
        expected = [
                wtp.patch.diffobj(
                    header=wtp.patch.header(
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
                        (8, None, None),
                        (9, None, None),
                        (None, 11, 'from Bugxplore import main'),
                        (None, 12, 'from Bugxplore import _make_dir'),
                        ],
                    text = '\n'.join(lines[:10]) + '\n'
                   ),
                wtp.patch.diffobj(
                    header=wtp.patch.header(
                        index_path = 'bugtrace/trunk/src/bugtrace/Diffxplore.py',
                        old_path='bugtrace/trunk/src/bugtrace/Diffxplore.py',
                        old_version=None,
                        new_path='bugtrace/trunk/src/bugtrace/Diffxplore.py',
                        new_version=None,
                        ),
                    changes=[
                        (49, None, None),
                        (None, 49, "    optparser.set_defaults(output_dir='/tmp/diffs')"),
                        (53, None, None),
                        (None, 53, ''),
                        ],
                    text = '\n'.join(lines[10:18]) + '\n'
                    ),
                wtp.patch.diffobj(
                    header=wtp.patch.header(
                        index_path = 'bugtrace/trunk/src/bugtrace/Bugxplore.py',
                        old_path='bugtrace/trunk/src/bugtrace/Bugxplore.py',
                        old_version=None,
                        new_path='bugtrace/trunk/src/bugtrace/Bugxplore.py',
                        new_version=None,
                        ),
                    changes=[
                        (86, None, None),
                        (None, 86, "    optparser.set_defaults(output_dir='/tmp/bugs')"),
                        (91, None, None),
                        (None, 91, ''),
                        ],
                    text = '\n'.join(lines[18:]) + '\n'
                    )
                    ]

        results = list(wtp.parse_patch(text))
        self.assertEqual(results, expected)


    def test_svn_default_patch(self):
        with open('tests/casefiles/svn-default.patch') as f:
            text = f.read()

        lines = text.splitlines()

        expected = [
                wtp.patch.diffobj(
                    header=wtp.patch.header(
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
                        ],
                    text = '\n'.join(lines[:12]) + '\n'
                   ),
                wtp.patch.diffobj(
                    header=wtp.patch.header(
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
                        ],
                    text = '\n'.join(lines[12:22]) + '\n'
                    ),
                wtp.patch.diffobj(
                    header=wtp.patch.header(
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
                        ],
                    text = '\n'.join(lines[22:]) + '\n'
                    )
                    ]
        results = list(wtp.parse_patch(text))
        self.assertEqual(results, expected)


    def test_git_patch(self):
        with open('tests/casefiles/git.patch') as f:
            text = f.read()

        lines = text.splitlines()

        expected = [
                wtp.patch.diffobj(
                    header=wtp.patch.header(
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
                        (172, 168, '     * ')],
                    text = '\n'.join(lines[:34]) + '\n'
                    ),
                    wtp.patch.diffobj(
                        header=wtp.patch.header(
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
                            (23, 25, '    protected Preferences prefs;')],
                        text = '\n'.join(lines[34:]) + '\n'
                        )
                    ]

        results = list(wtp.parse_patch(text))

        self.assertEqual(results, expected)

    def test_git_oneline_add(self):
        with open('tests/casefiles/git-oneline-add.diff') as f:
            text = f.read()

        lines = text.splitlines()

        expected = [
            wtp.patch.diffobj(
                header=wtp.patch.header(
                    index_path=None,
                    old_path='/dev/null',
                    old_version='0000000',
                    new_path='oneline.txt',
                    new_version='f56f98d'
                ),
                changes=[
                    (None, 1, 'Adding a one-line file.')
                ],
                text='\n'.join(lines[:34]) + '\n'
            )
        ]

        results = list(wtp.parse_patch(text))

        self.assertEqual(results, expected)

    def test_git_oneline_change(self):
        with open('tests/casefiles/git-oneline-change.diff') as f:
            text = f.read()

        lines = text.splitlines()

        expected = [
            wtp.patch.diffobj(
                header=wtp.patch.header(
                    index_path=None,
                    old_path='oneline.txt',
                    old_version='f56f98d',
                    new_path='oneline.txt',
                    new_version='169ceeb'
                ),
                changes=[
                    (1, None, 'Adding a one-line file.'),
                    (None, 1, 'Changed a one-line file.')
                ],
                text='\n'.join(lines[:34]) + '\n'
            )
        ]

        results = list(wtp.parse_patch(text))
        self.assertEqual(results, expected)

    def test_git_oneline_rm(self):
        with open('tests/casefiles/git-oneline-rm.diff') as f:
            text = f.read()

        lines = text.splitlines()

        expected = [
            wtp.patch.diffobj(
                header=wtp.patch.header(
                    index_path=None,
                    old_path='oneline.txt',
                    old_version='169ceeb',
                    new_path='/dev/null',
                    new_version='0000000'
                ),
                changes=[
                    (1, None, 'Changed a one-line file.')
                ],
                text='\n'.join(lines[:34]) + '\n'
            )
        ]

        results = list(wtp.parse_patch(text))
        self.assertEqual(results, expected)

    def test_git_header(self):
        with open('tests/casefiles/git-header.diff') as f:
            text = f.read()

        expected = wtp.patch.header(
                index_path = None,
                old_path = 'bugtrace/patch.py',
                old_version = '8910dfd',
                new_path = 'bugtrace/patch.py',
                new_version = '456e34f')

        results = wtp.patch.parse_git_header(text)
        self.assertEqual(results, expected)

        results_main = wtp.patch.parse_header(text)
        self.assertEqual(results_main, expected)

    def test_git_header_long(self):
        with open('tests/casefiles/git-header-long.diff') as f:
            text = f.read()

        expected = wtp.patch.header(
                index_path = None,
                old_path = 'bugtrace/patch.py',
                old_version = '18910dfd',
                new_path = 'bugtrace/patch.py',
                new_version = '2456e34f')

        results = wtp.patch.parse_git_header(text)
        self.assertEqual(results, expected)

        results_main = wtp.patch.parse_header(text)
        self.assertEqual(results_main, expected)

    def test_svn_header(self):
        with open('tests/casefiles/svn-header.diff') as f:
            text = f.read()

        expected = wtp.patch.header(
                index_path = 'bugtrace/trunk/src/bugtrace/csc.py',
                old_path = 'bugtrace/trunk/src/bugtrace/csc.py',
                old_version = 12783,
                new_path = 'bugtrace/trunk/src/bugtrace/csc.py',
                new_version = 12784)
        results = wtp.patch.parse_svn_header(text)
        self.assertEqual(results, expected)

        results_main = wtp.patch.parse_header(text)
        self.assertEqual(results_main, expected)

    def test_cvs_header(self):
        with open('tests/casefiles/cvs-header.diff') as f:
            text = f.read()

        expected = wtp.patch.header(
                index_path = 'org.eclipse.core.resources/src/org/eclipse/core/internal/localstore/SafeChunkyInputStream.java',
                old_path = 'org.eclipse.core.resources/src/org/eclipse/core/internal/localstore/SafeChunkyInputStream.java',
                old_version = '1.6.4.1',
                new_path = 'org.eclipse.core.resources/src/org/eclipse/core/internal/localstore/SafeChunkyInputStream.java',
                new_version = '1.8')
        results = wtp.patch.parse_cvs_header(text)
        self.assertEqual(results, expected)

        results_main = wtp.patch.parse_header(text)
        self.assertEqual(results_main, expected)

    def test_unified_header(self):
        with open('tests/casefiles/unified-header.diff') as f:
            text = f.read()

        expected = wtp.patch.header(
                index_path = None,
                old_path = '/tmp/o',
                old_version = '2012-12-22 06:43:35.000000000 -0600',
                new_path = '/tmp/n',
                new_version = '2012-12-23 20:40:50.000000000 -0600')

        results = wtp.patch.parse_unified_header(text)
        self.assertEqual(results, expected)

        results_main = wtp.patch.parse_header(text)
        self.assertEqual(results_main, expected)

    def test_unified_header_notab(self):
        with open('tests/casefiles/unified-header-notab.diff') as f:
            text = f.read()

        expected = wtp.patch.header(
                index_path = None,
                old_path = '/tmp/some file',
                old_version = '2012-12-22 06:43:35.000000000 -0600',
                new_path = '/tmp/n',
                new_version = '2012-12-23 20:40:50.000000000 -0600')

        results = wtp.patch.parse_unified_header(text)
        self.assertEqual(results, expected)

        results_main = wtp.patch.parse_header(text)
        self.assertEqual(results_main, expected)


    def test_unified_diff(self):
        with open(datapath('diff-unified.diff')) as f:
            text = f.read()

        # off with your head!
        text_diff = '\n'.join(text.splitlines()[2:]) + '\n'

        expected = [
            (1, None,   'The Way that can be told of is not the eternal Way;'),
            (2, None,   'The name that can be named is not the eternal name.'),
            (3, 1,      'The Nameless is the origin of Heaven and Earth;'),
            (4, None,   'The Named is the mother of all things.'),
            (None, 2,   'The named is the mother of all things.'),
            (None, 3,   ''),
            (5, 4,       'Therefore let there always be non-being,'),
            (6, 5,      '  so we may see their subtlety,'),
            (7, 6,      'And let there always be being,'),
            (9, 8,      'The two are the same,'),
            (10, 9,     'But after they are produced,'),
            (11, 10,    '  they have different names.'),
            (None, 11,  'They both may be called deep and profound.'),
            (None, 12,  'Deeper and more profound,'),
            (None, 13,  'The door of all subtleties!')
        ]

        results = list(wtp.patch.parse_unified_diff(text_diff))
        self.assertEqual(results, expected)

        expected_main = wtp.patch.diffobj(header=
                                          wtp.patch.header(index_path=None,
                                                           old_path='lao',
                                                           old_version='2013-01-05 16:56:19.000000000 -0600',
                                                           new_path='tzu',
                                                           new_version='2013-01-05 16:56:35.000000000 -0600'
                                                           ),
                                          changes=expected,
                                          text=text)
        results_main = next(wtp.patch.parse_patch(text))
        self.assertEqual(results_main, expected_main)

    def test_diff_unified_with_does_not_include_extra_lines(self):
        with open('tests/casefiles/diff-unified-blah.diff') as f:
            text = f.read()


        expected = [
            wtp.patch.diffobj(
                header=wtp.patch.header(
                    index_path=None,
                    old_path='lao',
                    old_version='2013-01-05 16:56:19.000000000 -0600',
                    new_path='tzu',
                    new_version='2013-01-05 16:56:35.000000000 -0600'
                    ),
                changes=[
                    (1, None, 'The Way that can be told of is not the eternal Way;'),
                    (2, None, 'The name that can be named is not the eternal name.'),
                    (3, 1, 'The Nameless is the origin of Heaven and Earth;'),
                    (4, None, 'The Named is the mother of all things.'),
                    (None, 2, 'The named is the mother of all things.'),
                    (None, 3, ''),
                    (5, 4, 'Therefore let there always be non-being,'),
                    (6, 5, '  so we may see their subtlety,'),
                    (7, 6, 'And let there always be being,'),
                    (9, 8, 'The two are the same,'),
                    (10, 9, 'But after they are produced,'),
                    (11, 10, '  they have different names.'),
                    (None, 11, 'They both may be called deep and profound.'),
                    (None, 12, 'Deeper and more profound,'),
                    (None, 13, 'The door of all subtleties!')],
                text=text)
                ]


        results = list(wtp.patch.parse_patch(text))
        self.assertEqual(results, expected)

    def test_diff_context_with_does_not_include_extra_lines(self):
        with open('tests/casefiles/diff-context-blah.diff') as f:
            text = f.read()


        expected = [
            wtp.patch.diffobj(
                header=wtp.patch.header(
                    index_path=None,
                    old_path='lao',
                    old_version='2013-01-05 16:56:19.000000000 -0600',
                    new_path='tzu',
                    new_version='2013-01-05 16:56:35.000000000 -0600'
                    ),
                changes=[
                    (1, None, 'The Way that can be told of is not the eternal Way;'),
                    (2, None, 'The name that can be named is not the eternal name.'),
                    (3, 1, 'The Nameless is the origin of Heaven and Earth;'),
                    (4, None, 'The Named is the mother of all things.'),
                    (None, 2, 'The named is the mother of all things.'),
                    (None, 3, ''),
                    (5, 4, 'Therefore let there always be non-being,'),
                    (6, 5, '  so we may see their subtlety,'),
                    (7, 6, 'And let there always be being,'),
                    (9, 8, 'The two are the same,'),
                    (10, 9, 'But after they are produced,'),
                    (11, 10, '  they have different names.'),
                    (None, 11, 'They both may be called deep and profound.'),
                    (None, 12, 'Deeper and more profound,'),
                    (None, 13, 'The door of all subtleties!')],
                text=text)
                ]


        results = list(wtp.patch.parse_patch(text))
        self.assertEqual(results, expected)

    def test_diff_default_with_does_not_include_extra_lines(self):
        with open('tests/casefiles/diff-default-blah.diff') as f:
            text = f.read()

        expected = [
            wtp.patch.diffobj(
                header=None,
                changes=[
                    (1, None, 'The Way that can be told of is not the eternal Way;'),
                    (2, None, 'The name that can be named is not the eternal name.'),
                    (4, None, 'The Named is the mother of all things.'),
                    (None, 2, 'The named is the mother of all things.'),
                    (None, 3, ''),
                    (None, 11, 'They both may be called deep and profound.'),
                    (None, 12, 'Deeper and more profound,'),
                    (None, 13, 'The door of all subtleties!')],
                text=text)
                ]


        results = list(wtp.patch.parse_patch(text))
        self.assertEqual(results, expected)


    def test_context_header(self):
        with open('tests/casefiles/context-header.diff') as f:
            text = f.read()


        expected = wtp.patch.header(
                index_path = None,
                old_path = '/tmp/o',
                old_version = '2012-12-22 06:43:35.000000000 -0600',
                new_path = '/tmp/n',
                new_version = '2012-12-23 20:40:50.000000000 -0600')

        results = wtp.patch.parse_context_header(text)
        self.assertEqual(results, expected)

        results_main = wtp.patch.parse_header(text)
        self.assertEqual(results_main, expected)


    def test_context_diff(self):
        with open(datapath('diff-context.diff')) as f:
            text = f.read()

        # off with your head!
        text_diff = '\n'.join(text.splitlines()[2:]) + '\n'

        expected = [
                    (1, None, 'The Way that can be told of is not the eternal Way;'),
                    (2, None, 'The name that can be named is not the eternal name.'),
                    (3, 1, 'The Nameless is the origin of Heaven and Earth;'),
                    (4, None, 'The Named is the mother of all things.'),
                    (None, 2, 'The named is the mother of all things.'),
                    (None, 3, ''),
                    (5, 4, 'Therefore let there always be non-being,'),
                    (6, 5, '  so we may see their subtlety,'),
                    (7, 6, 'And let there always be being,'),
                    (9, 8, 'The two are the same,'),
                    (10, 9, 'But after they are produced,'),
                    (11, 10, '  they have different names.'),
                    (None, 11, 'They both may be called deep and profound.'),
                    (None, 12, 'Deeper and more profound,'),
                    (None, 13, 'The door of all subtleties!'),
                ]

        results = list(wtp.patch.parse_context_diff(text_diff))
        self.assertEqual(results, expected)


        expected_main = wtp.patch.diffobj(header=
                                          wtp.patch.header(index_path=None,
                                                           old_path='lao',
                                                           old_version='2013-01-05 16:56:19.000000000 -0600',
                                                           new_path='tzu',
                                                           new_version='2013-01-05 16:56:35.000000000 -0600'
                                                           ),
                                          changes=expected,
                                          text=text)
        results_main = next(wtp.patch.parse_patch(text))
        self.assertEqual(results_main, expected_main)

    def test_ed_diff(self):
        with open(datapath('diff-ed.diff')) as f:
            text = f.read()

        expected = [
            (1, None, None),
            (2, None, None),
            (4, None, None),
            (None, 2,   'The named is the mother of all things.'),
            (None, 3,   ''),
            (None, 11,  'They both may be called deep and profound.'),
            (None, 12,  'Deeper and more profound,'),
            (None, 13,  'The door of all subtleties!')
        ]


        results = list(wtp.patch.parse_ed_diff(text))
        self.assertEqual(results, expected)

        expected_main = [wtp.patch.diffobj(header=None, changes=expected, text=text)]
        results_main = list(wtp.patch.parse_patch(text))
        self.assertEqual(results_main, expected_main)

    def test_rcs_diff(self):
        with open(datapath('diff-rcs.diff')) as f:
            text = f.read()

        expected = [
            (1, None, None),
            (2, None, None),
            (4, None, None),
            (None, 2,   'The named is the mother of all things.'),
            (None, 3,   ''),
            (None, 11,  'They both may be called deep and profound.'),
            (None, 12,  'Deeper and more profound,'),
            (None, 13,  'The door of all subtleties!')
        ]


        results = list(wtp.patch.parse_rcs_ed_diff(text))
        self.assertEqual(results, expected)

        expected_main = [wtp.patch.diffobj(header=None, changes=expected, text=text)]
        results_main = list(wtp.patch.parse_patch(text))
        self.assertEqual(results_main, expected_main)

    def test_embedded_diff_in_comment(self):
        with open('tests/casefiles/embedded-diff.comment') as f:
            text = f.read()

        expected = [
                wtp.patch.diffobj(
                    header=wtp.patch.header(
                        index_path=None,
                        old_path='src/org/mozilla/javascript/IRFactory.java',
                        old_version=None,
                        new_path='src/org/mozilla/javascript/IRFactory.java',
                        new_version=None,
                        ),
                    changes=[
                        (2182, 2182, '          case Token.GETELEM:'),
                        (2183, 2183, '              decompileElementGet((ElementGet) node);'),
                        (2184, 2184, '              break;'),
                        (None, 2185, '          case Token.THIS:'),
                        (None, 2186, '              decompiler.addToken(node.getType());'),
                        (None, 2187, '              break;'),
                        (2185, 2188, '          default:'),
                        (2186, 2189, '              Kit.codeBug("unexpected token: "'),
                        (2187, 2190, '                          + Token.typeToName(node.getType()));'),
                        ],
                    text=text
                   ),
                ]

        results = list(wtp.patch.parse_patch(text))
        self.assertEqual(results, expected)

    def test_mozilla_527452_5_comment(self):
        with open('tests/casefiles/mozilla-527452-5.comment') as f:
            text = f.read()

        lines = text.splitlines()

        expected = [
                wtp.patch.diffobj(
                    header=wtp.patch.header(
                        index_path='js_instrumentation_proxy/src/org/mozilla/javascript/ast/StringLiteral.java',
                        old_path='js_instrumentation_proxy/src/org/mozilla/javascript/ast/StringLiteral.java',
                        old_version=5547,
                        new_path='js_instrumentation_proxy/src/org/mozilla/javascript/ast/StringLiteral.java',
                        new_version=None,
                        ),
                    changes=[
                        (112, 112, '        // TODO(stevey):  make sure this unescapes everything properly'),
                        (113, 113, '        String q = String.valueOf(getQuoteCharacter());'),
                        (114, 114, '        String rep = "\\\\\\\\" + q;'), # escape the escape that's escaping an escape. wut
                        (115, None, '        String s = value.replaceAll(q, rep);'),
                        (None, 115, '        String s = value.replace("\\\\", "\\\\\\\\");'),
                        (None, 116, '        s = s.replaceAll(q, rep);'),
                        (116, 117, '        s = s.replaceAll("\\n", "\\\\\\\\n");'),
                        (117, 118, '        s = s.replaceAll("\\r", "\\\\\\\\r");'),
                        (118, 119, '        s = s.replaceAll("\\t", "\\\\\\\\t");')
                        ],
                    text = '\n'.join(lines[2:]) + '\n'
                   ),
                ]

        results = list(wtp.patch.parse_patch(text))
        self.assertEqual(results, expected)

    def test_dos_unified_cvs(self):
        with open('tests/casefiles/mozilla-560291.diff') as f:
            text = f.read()

        lines = text.splitlines()

        expected = [
            wtp.patch.diffobj(
                header=wtp.patch.header(
                    index_path='src/org/mozilla/javascript/ast/ArrayComprehensionLoop.java',
                    old_path='src/org/mozilla/javascript/ast/ArrayComprehensionLoop.java',
                    old_version='1.1',
                    new_path='src/org/mozilla/javascript/ast/ArrayComprehensionLoop.java',
                    new_version='15 Sep 2011 02:26:05 -0000'
                ),
                changes=[
                    (79, 79, '    @Override'),
                    (80, 80, '    public String toSource(int depth) {'),
                    (81, 81, '        return makeIndent(depth)'),
                    (82, None, '                + " for ("'),
                    (None, 82, '                + " for " '),
                    (None, 83, '                + (isForEach()?"each ":"")'),
                    (None, 84, '                + "("'),
                    (83, 85, '                + iterator.toSource(0)'),
                    (84, 86, '                + " in "'),
                    (85, 87, '                + iteratedObject.toSource(0)')
                ],
                text = '\n'.join(lines[2:]) + '\n'
            )
        ]

        results = list(wtp.patch.parse_patch(text))
        self.assertEqual(results, expected)


    def test_old_style_cvs(self):
        with open('tests/casefiles/mozilla-252983.diff') as f:
            text = f.read()

        expected = [
                wtp.patch.diffobj(
                    header=wtp.patch.header(
                        index_path='mozilla/js/rhino/CHANGELOG',
                        old_path='mozilla/js/rhino/CHANGELOG',
                        old_version='1.1.1.1',
                        new_path='mozilla/js/rhino/CHANGELOG',
                        new_version='1.1', # or 'Thu Jan 25 10:59:02 2007'
                        ),
                    changes=[
                        (1, None, 'This file version: $Id: CHANGELOG,v 1.1.1.1 2007/01/25 15:59:02 inonit Exp $'),
                        (None, 1, 'This file version: $Id: CHANGELOG,v 1.1 2007/01/25 15:59:02 inonit Exp $'),
                        (2, 2, ''),
                        (3, 3, 'Changes since Rhino 1.6R5'),
                        (4, 4, '========================='),
                        ],
                    text=text
                   ),
                ]

        results = wtp.patch.parse_cvs_header(text)
        self.assertEqual(results, expected[0].header)

        results = wtp.patch.parse_header(text)
        self.assertEqual(results, expected[0].header)

        results = list(wtp.patch.parse_patch(text))
        self.assertEqual(results, expected)

    def test_mozilla_252983_versionless(self):
        with open('tests/casefiles/mozilla-252983-versionless.diff') as f:
            text = f.read()

        expected = [
                wtp.patch.diffobj(
                    header=wtp.patch.header(
                        index_path='mozilla/js/rhino/CHANGELOG',
                        old_path='mozilla/js/rhino/CHANGELOG',
                        old_version=None,
                        new_path='mozilla/js/rhino/CHANGELOG',
                        new_version=None,
                        ),
                    changes=[
                        (1, None, 'This file version: $Id: CHANGELOG,v 1.1.1.1 2007/01/25 15:59:02 inonit Exp $'),
                        (None, 1, 'This file version: $Id: CHANGELOG,v 1.1 2007/01/25 15:59:02 inonit Exp $'),
                        (2, 2, ''),
                        (3, 3, 'Changes since Rhino 1.6R5'),
                        (4, 4, '========================='),
                        ],
                    text=text
                   ),
                ]

        results = wtp.patch.parse_header(text)
        self.assertEqual(results, expected[0].header)

        results = list(wtp.patch.parse_patch(text))
        self.assertEqual(results, expected)

    def test_apache_attachment_2241(self):
        with open('tests/casefiles/apache-attachment-2241.diff') as f:
            text = f.read()

        lines = text.splitlines()

        expected = [
                wtp.patch.diffobj(
                    header=wtp.patch.header(
                        index_path=None,
                        old_path='src\\main\\org\\apache\\tools\\ant\\taskdefs\\optional\\pvcs\\Pvcs.orig',
                        old_version='Sat Jun 22 16:11:58 2002',
                        new_path='src\\main\\org\\apache\\tools\\ant\\taskdefs\\optional\\pvcs\\Pvcs.java',
                        new_version='Fri Jun 28 10:55:50 2002'
                        ),
                    changes=[
                        (91, 91, ' *'),
                        (92, 92, ' * @author <a href="mailto:tchristensen@nordija.com">Thomas Christensen</a>'),
                        (93, 93, ' * @author <a href="mailto:donj@apogeenet.com">Don Jeffery</a>'),
                        (94, None, ' * @author <a href="snewton@standard.com">Steven E. Newton</a>'),
                        (None, 94, ' * @author <a href="mailto:snewton@standard.com">Steven E. Newton</a>'),
                        (95, 95, ' */'),
                        (96, 96, 'public class Pvcs extends org.apache.tools.ant.Task {'),
                        (97, 97, '    private String pvcsbin;')
                        ],
                    text= '\n'.join(lines) + '\n'
                   ),
                ]

        results = list(wtp.patch.parse_patch(text))
        self.assertEqual(results, expected)

    def test_space_in_path_header(self):
        with open('tests/casefiles/eclipse-attachment-126343.header') as f:
            text = f.read()

        expected = wtp.patch.header(
                index_path = 'test plugin/org/eclipse/jdt/debug/testplugin/ResumeBreakpointListener.java',
                old_path = '/dev/null',
                old_version = '1 Jan 1970 00:00:00 -0000',
                new_path = 'test plugin/org/eclipse/jdt/debug/testplugin/ResumeBreakpointListener.java',
                new_version = '1 Jan 1970 00:00:00 -0000'
                )

        results = wtp.patch.parse_header(text)
        self.assertEqual(results, expected)

    def test_svn_mixed_line_ends(self):
        with open('tests/casefiles/svn-mixed_line_ends.patch') as f:
            text = f.read()

        expected_header = wtp.patch.header(
                index_path='java/org/apache/catalina/loader/WebappClassLoader.java',
                old_path='java/org/apache/catalina/loader/WebappClassLoader.java',
                old_version=1346371,
                new_path='java/org/apache/catalina/loader/WebappClassLoader.java',
                new_version=None)

        results = list(wtp.patch.parse_patch(text))
        self.assertEqual(results[0].header, expected_header)


if __name__ == '__main__':
    unittest.main()
