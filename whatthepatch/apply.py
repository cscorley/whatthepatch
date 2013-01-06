#!/usr/bin/env python2.6
#
# [The "New BSD" license]
# Copyright (c) 2012 The Board of Trustees of The University of Alabama
# All rights reserved.
#
# See LICENSE for details.

from __future__ import print_function
import re

import patch

def apply_patch(diffs):
    if type(diffs) == patch.diff:
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

def apply_diff(diff, text):
    if type(text) == str:
        lines = text.split('\n')
    else:
        lines = text

    # check that the source text matches the context of the diff
    for old, new, line in diff.changes:
        # might have to check for line is None here for ed scripts
        if old is not None and line is not None:
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
            assert new == old - r + i

    return lines




