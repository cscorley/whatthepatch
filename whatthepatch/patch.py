#!/usr/bin/env python2.6
#
# [The "New BSD" license]
# Copyright (c) 2012 The Board of Trustees of The University of Alabama
# All rights reserved.
#
# See LICENSE for details.

from __future__ import print_function
import re
from collections import namedtuple

import dateutil.parser

from snippets import split_by_regex, findall_regex

date_header = namedtuple('date_header',
        'old_path old_datetime new_path new_datetime')
revision_header = namedtuple('revision_header',
        'old_path old_rev new_path new_rev')

header = namedtuple('header',
        'old_path old_version new_path new_version')

# general diff regex
diff_command_header = re.compile('^diff ([\s\S]+)$')
unified_index_header = re.compile('^Index: ([\s\S]+)$')
unified_header_old_line = re.compile('^--- ([-/._\w]+)\s+([\s\S]*)$')
unified_header_new_line = re.compile('^\+\+\+ ([-/._\w]+)\s+([\s\S]*)$')
unified_hunk_start = re.compile('^@@ -(\d+),?(\d*) \+(\d+),?(\d*) @@$')
unified_change = re.compile('^([-+ ])([\s\S]*)$')

context_header_old_line = re.compile('^\*\*\* ([-/._\w]+)\s+([\s\S]*)$')
context_header_new_line = unified_header_old_line
context_hunk_start = re.compile('^\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*$')
context_hunk_old = re.compile('^\*\*\* (\d+),(\d+) \*\*\*\*$')
context_hunk_new = re.compile('^--- (\d+),(\d+) ----$')
context_change = re.compile('^([-+ !]) ([\s\S]*)$')

ed_hunk_start = re.compile('^(\d+),?(\d*)([acd])$')
ed_hunk_end = re.compile('^.$')
# much like forward ed, but no 'c' type
rcs_ed_hunk_start = re.compile('^([ad])(\d+) ?(\d*)$')

default_hunk_start = re.compile('^(\d+),?(\d*)([acd])(\d+),?(\d*)$')
default_hunk_mid = re.compile('^---$')
default_change = re.compile('^([><]) ([\s\S]*)$')

# Headers

# git has a special index header and no end part
git_index_header = re.compile('index ([\w]{7})..([\w]{7}) \d+')
git_header_old_line = re.compile('^--- a/([\s\S]+)$')
git_header_new_line = re.compile('^\+\+\+ b/([\s\S]+)$')

bzr_index_header = re.compile("=== ([\s\S]+)")
bzr_header_old_line = unified_header_old_line
bzr_header_new_line = unified_header_new_line

svn_index_header = unified_index_header
svn_header_old_line = unified_header_old_line
svn_header_new_line = unified_header_new_line
svn_header_end_part = re.compile('\((?:working copy|revision (\d+))\)')

cvs_index_header = unified_index_header
cvs_rcs_header = re.compile('^RCS file: ([\s\S]+),\w{1}$')
cvs_header_old_line = unified_header_old_line
cvs_header_new_line = unified_header_new_line
cvs_header_end_part = re.compile('([\s\S]+)\s+([\d.]+)')

# old date regex -- will try to replace with datetime parsing
cvs_header_end_part1 = re.compile('(\d{4})[-/](\d{2})[-/](\d{2}) (\d{2}):(\d{2}):(\d{2})')
cvs_header_end_part2 = re.compile('(\d+) (\w{3}) (\d{4}) (\d{2}):(\d{2}):(\d{2})')


def parse_patch(text):
    if type(text) == str:
        lines = text.split('\n')
    else:
        lines = text

    diffs = split_by_regex(lines, unified_index_header)
    if len(diffs) == 0:
        diffs = split_by_regex(lines, diff_command_header)
    if len(diffs) == 0:
        diffs = split_by_regex(lines, unified_header_old_line)
    if len(diffs) == 0:
        diffs = split_by_regex(lines, context_header_old_line)

    for diff in diffs:
        h = parse_header(diff)
        d = parse_diff(diff)


def parse_header(text):
    parsers = [parse_cvs_header, parse_git_header, parse_svn_header,
            parse_unified_header, parse_context_header]

    return parse_things(parsers, text)

def parse_diff(text):
    parsers = [parse_unified_diff, parse_context_diff,
            parse_default_diff, parse_ed_diff, parse_rcs_ed_diff]

    return parse_things(parsers, text)

def parse_things(parsers, text):
    for p in parsers:
        try:
            res = p(text)
            if res:
                return res
        except Exception:
            pass

    return None

def parse_git_header(text):
    if type(text) == str:
        lines = text.split('\n')
    else:
        lines = text

    headers = findall_regex(lines, git_index_header)
    if len(headers) == 0:
        return None

    while len(lines) > 0:
        g = git_index_header.match(lines[0])
        o = git_header_old_line.match(lines[0])
        del lines[0]
        if g:
            over = g.group(1)
            nver = g.group(2)
            g = None
        if o:
            n = git_header_new_line.match(lines[0])
            del lines[0]
            if n:
                return header(old_path = o.group(1),
                        old_version = over,
                        new_path = n.group(1),
                        new_version = nver)

    return None

def parse_svn_header(text):
    if type(text) == str:
        lines = text.split('\n')
    else:
        lines = text

    headers = findall_regex(lines, svn_index_header)
    if len(headers) == 0:
        return None

    while len(lines) > 0:
        o = svn_header_old_line.match(lines[0])
        del lines[0]
        if o:
            n = svn_header_new_line.match(lines[0])
            del lines[0]
            if n:
                oend = svn_header_end_part.match(o.group(2))
                nend = svn_header_end_part.match(n.group(2))
                if oend and nend:
                    return header(old_path = o.group(1),
                            old_version = int(oend.group(1)),
                            new_path = n.group(1),
                            new_version = int(nend.group(1)))

    return None

def parse_cvs_header(text):
    if type(text) == str:
        lines = text.split('\n')
    else:
        lines = text

    headers = findall_regex(lines, cvs_rcs_header)
    if len(headers) == 0:
        return None

    while len(lines) > 0:
        o = cvs_header_old_line.match(lines[0])
        del lines[0]
        if o:
            n = cvs_header_new_line.match(lines[0])
            del lines[0]
            if n:
                oend = cvs_header_end_part.match(o.group(2))
                nend = cvs_header_end_part.match(n.group(2))
                if oend and nend:
                    return header(old_path = o.group(1),
                            old_version = oend.group(2),
                            new_path = n.group(1),
                            new_version = nend.group(2))

    return None

def parse_unified_header(text):
    if type(text) == str:
        lines = text.split('\n')
    else:
        lines = text

    headers = findall_regex(lines, unified_header_old_line)
    if len(headers) == 0:
        return None

    while len(lines) > 0:
        o = unified_header_old_line.match(lines[0])
        del lines[0]
        if o:
            n = unified_header_new_line.match(lines[0])
            del lines[0]
            if n:
                return header(old_path = o.group(1),
                        old_version = dateutil.parser.parse(o.group(2)),
                        new_path = n.group(1),
                        new_version = dateutil.parser.parse(n.group(2)))

    return None

def parse_context_header(text):
    if type(text) == str:
        lines = text.split('\n')
    else:
        lines = text

    headers = findall_regex(lines, context_header_old_line)
    if len(headers) == 0:
        return None

    while len(lines) > 0:
        o = context_header_old_line.match(lines[0])
        del lines[0]
        if o:
            n = context_header_new_line.match(lines[0])
            del lines[0]
            if n:
                return header(old_path = o.group(1),
                        old_version = dateutil.parser.parse(o.group(2)),
                        new_path = n.group(1),
                        new_version = dateutil.parser.parse(n.group(2)))

    return None


def parse_default_diff(text):
    if type(text) == str:
        lines = text.split('\n')
    else:
        lines = text

    old = 0
    new = 0
    j = 0
    k = 0

    changes = list()

    hunks = split_by_regex(lines, default_hunk_start)
    for hunk in hunks:
        if len(hunk):
            j = 0
            k = 0
            while len(hunk) > 0:
                o = default_hunk_start.match(hunk[0])
                c = default_change.match(hunk[0])
                del hunk[0]
                if o:
                    old = int(o.group(1))
                    new = int(o.group(4))
                    hunk_kind = o.group(3)
                elif c:
                    kind = c.group(1)
                    line = c.group(2)

                    if kind == '<':
                        changes.append((old + j, None, line))
                        j += 1
                    elif kind == '>':
                        changes.append((None, new + k, line))
                        k += 1

    if len(changes):
        return changes

    return None

def parse_unified_diff(text):
    if type(text) == str:
        lines = text.split('\n')
    else:
        lines = text

    old = 0
    new = 0
    j = 0
    k = 0

    changes = list()
    while len(lines) > 0:
        h = unified_hunk_start.match(lines[0])
        c = unified_change.match(lines[0])
        if h:
            old = int(h.group(1))
            new = int(h.group(3))

            # reset counters
            j = 0
            k = 0
            h = None
        elif c:
            kind = c.group(1)
            line = c.group(2)

            if kind == '-':
                changes.append((old + j, None, line))
                j += 1
            elif kind == '+':
                changes.append((None, new + k, line))
                k += 1
            elif kind == ' ':
                changes.append((old + j, new + k, line))
                j += 1
                k += 1
        else:
            return None


            c = None

        del lines[0]

    if len(lines):
        return None

    if len(changes):
        return changes

    return None



def parse_context_diff(text):
    if type(text) == str:
        lines = text.split('\n')
    else:
        lines = text

    old = 0
    new = 0
    j = 0
    k = 0

    changes = list()
    old_lines = list()
    new_lines = list()

    hunks = split_by_regex(lines, context_hunk_start)
    for hunk in hunks:
        if len(hunk):
            j = 0
            k = 0
            parts = split_by_regex(hunk, context_hunk_new)
            if len(parts) != 2:
                raise ValueError("Context diff invalid")

            old_hunk = parts[0]
            new_hunk = parts[1]

            while len(old_hunk) > 0:
                o = context_hunk_old.match(old_hunk[0])
                del old_hunk[0]
                if o:
                    old = int(o.group(1))
                    while len(new_hunk) > 0:
                        n = context_hunk_new.match(new_hunk[0])
                        del new_hunk[0]
                        if n:
                            new = int(n.group(1))
                            break
                    break

            # now have old and new set, can start processing?
            if len(old_hunk) > 0 and len(new_hunk) == 0:
                # only removes left?
                while len(old_hunk) > 0:
                    c = context_change.match(old_hunk[0])
                    del old_hunk[0]
                    if c:
                        kind = c.group(1)
                        line = c.group(2)

                        if kind == '-':
                            changes.append((old + j, None, line))
                            j += 1
                        elif kind == ' ':
                            changes.append((old + j, new + k, line))
                            j += 1
                            k += 1
                        elif kind == '+' or kind == '!':
                            raise ValueError("Wat1" + kind)

            elif len(old_hunk) == 0 and len(new_hunk) > 0:
                # only insertions left?
                while len(new_hunk) > 0:
                    c = context_change.match(new_hunk[0])
                    del new_hunk[0]
                    if c:
                        kind = c.group(1)
                        line = c.group(2)

                        if kind == '+':
                            changes.append((None, new + k, line))
                            k += 1
                        elif kind == ' ':
                            changes.append((old + j, new + k, line))
                            j += 1
                            k += 1
                        elif kind == '-' or kind == '!':
                            raise ValueError("Wat2" + kind)
            else:
                # both
                while len(old_hunk) > 0 and len(new_hunk) > 0:
                    oc = context_change.match(old_hunk[0])
                    nc = context_change.match(new_hunk[0])
                    okind = None
                    nkind = None

                    if oc:
                        okind = oc.group(1)
                        oline = oc.group(2)

                    if nc:
                        nkind = nc.group(1)
                        nline = nc.group(2)

                    if not (oc or nc):
                        del old_hunk[0]
                        del new_hunk[0]
                    elif okind == ' ' and nkind == ' ' and oline == nline:
                        changes.append((old + j, new + k, oline))
                        j += 1
                        k += 1
                        del old_hunk[0]
                        del new_hunk[0]
                    elif okind == '-' or okind == '!':
                        changes.append((old + j, None, oline))
                        j += 1
                        del old_hunk[0]
                    elif nkind == '+' or nkind == '!':
                        changes.append((None, new + k, nline))
                        k += 1
                        del new_hunk[0]
                    else:
                        return None

    if len(changes):
        return changes

    return None


def parse_ed_diff(text):
    if type(text) == str:
        lines = text.split('\n')
    else:
        lines = text

    old = 0
    new = 0
    j = 0
    k = 0

    changes = list()

    hunks = split_by_regex(lines, ed_hunk_start)
    for hunk in hunks:
        if len(hunk):
            j = 0
            k = 0
            while len(hunk) > 0:
                o = ed_hunk_start.match(hunk[0])
                del hunk[0]
                if o:
                    old = int(o.group(1))
                    if len(o.group(2)):
                        old_end = int(o.group(2))
                    else:
                        old_end = old

                    hunk_kind = o.group(3)
                    while len(hunk) > 0:
                        e = ed_hunk_end.match(hunk[0])
                        if e:
                            pass
                        elif hunk_kind == 'c':
                            k = 0
                            while old_end >= old:
                                changes.append((old + k, None, None))
                                k += 1
                                old_end -= 1

                            changes.append((None, old + j, hunk[0]))
                            j += 1
                            # math! \o/
                        elif hunk_kind == 'a':
                            changes.append((None, old + j + 1, hunk[0]))
                            j += 1
                        elif hunk_kind == 'd':
                            k = 0
                            while old_end >= old:
                                changes.append((old + k, None, None))
                                k += 1
                                old_end -= 1

                        del hunk[0]



    if len(changes):
        return changes

    return None

def parse_rcs_ed_diff(text):
    # much like forward ed, but no 'c' type
    rcs_ed_hunk_start = re.compile('^([ad])(\d+) ?(\d*)$')
    if type(text) == str:
        lines = text.split('\n')
    else:
        lines = text

    old = 0
    new = 0
    j = 0
    k = 0
    just_deleted = False

    changes = list()

    hunks = split_by_regex(lines, rcs_ed_hunk_start)
    for hunk in hunks:
        if len(hunk):
            j = 0
            k = 0
            while len(hunk) > 0:
                o = rcs_ed_hunk_start.match(hunk[0])
                del hunk[0]
                if o:
                    old = int(o.group(2))
                    size = int(o.group(3))

                    hunk_kind = o.group(1)
                    if hunk_kind == 'a':
                        while len(hunk) > 0:
                            if just_deleted:
                                changes.append((None, old + j, hunk[0]))
                            else:
                                changes.append((None, old + j+1, hunk[0]))
                            j += 1

                            del hunk[0]
                        just_deleted = False
                    elif hunk_kind == 'd':
                        while size > 0:
                            changes.append((old + j, None, None))
                            j += 1
                            size -= 1
                        just_deleted = True # lol joke diffs

    if len(changes):
        return changes

    return None
