# -*- coding: utf-8 -*-

import re
import subprocess

from . import patch
from .snippets import which, remove

def apply_patch(diffs):
    """ Not ready for use yet """
    pass

    if isinstance(diffs, patch.diff):
        diffs = [diffs]

    for diff in diffs:
        if diff.header.old_path == '/dev/null':
            text = []
        else:
            with open(diff.header.old_path) as f:
                text = f.read()

        new_text = apply_diff(diff, text)
        with open(diff.header.new_path, 'w') as f:
            f.write(new_text)

def apply_diff(diff, text, use_patch=False):
    try:
        lines = text.splitlines()
    except AttributeError:
        lines = list(text)

    if use_patch:
        # call out to patch program
        patchexec = which('patch')
        assert patchexec # patch program does not exist

        filepath = '/tmp/wtp-' + str(hash(diff.header))
        oldfilepath = filepath + '.old'
        newfilepath = filepath + '.new'
        rejfilepath = filepath + '.rej'
        patchfilepath = filepath + '.patch'
        with open(oldfilepath, 'w') as f:
            f.write('\n'.join(lines) + '\n')

        with open(patchfilepath, 'w') as f:
            f.write(diff.text)

        args = [patchexec,
                '--quiet',
                '-o', newfilepath,
                '-i', patchfilepath,
                '-r', rejfilepath,
                oldfilepath
                ]
        ret = subprocess.call(args)


        with open(newfilepath) as f:
            lines = f.read().splitlines()

        try:
            with open(rejfilepath) as f:
                rejlines = f.read().splitlines()
        except IOError:
            rejlines = None

        remove(oldfilepath)
        remove(newfilepath)
        remove(rejfilepath)
        remove(patchfilepath)

        # do this last to ensure files get cleaned up
        assert ret == 0 # patch return code is success

        return lines, rejlines

    # check that the source text matches the context of the diff
    for old, new, line in diff.changes:
        # might have to check for line is None here for ed scripts
        if old is not None and line is not None:
            assert len(lines) >= old
            assert lines[old-1] == line

    # for calculating the old line
    r = 0
    i = 0

    for old, new, line in diff.changes:
        if old is not None and new is None:
            del lines[old-1-r+i]
            r += 1
        elif old is None and new is not None:
            lines.insert(new-1, line)
            i += 1
        elif old is not None and new is not None:
            # are we crazy?
            #assert new == old - r + i

            # Sometimes, people remove hunks from patches, making these
            # numbers completely unreliable. Because they're jerks.
            pass

    return lines



