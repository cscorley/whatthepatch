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

from snippets import split_by_regex, findall_regex

header = namedtuple('header',
        'index_path old_path old_version new_path new_version')

diffobj = namedtuple('diff', 'header changes text')

# general diff regex
diff_command_header = re.compile('^diff [\s\S]* ([\s\S]+) ([\s\S]+)$')
unified_index_header = re.compile('^Index: ([\s\S]+)$')
unified_header_old_line = re.compile('^--- ([-/._\w]+)\s+([\s\S]*)$')
unified_header_new_line = re.compile('^\+\+\+ ([-/._\w]+)\s+([\s\S]*)$')
unified_hunk_start = re.compile('^@@ -(\d+),?(\d*) \+(\d+),?(\d*) @@([\s\S]*)$')
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
git_diff_command_header = re.compile('^diff --git a/([\s\S]+) b/([\s\S]+)$')
git_index_header = re.compile('index ([\w]{7})..([\w]{7}) \d+')
git_header_old_line = re.compile('^--- ([\s\S]+)$')
git_header_new_line = re.compile('^\+\+\+ ([\s\S]+)$')
git_file_mode = re.compile('^(new|deleted) file mode \d{6}$')

bzr_index_header = re.compile("=== ([\s\S]+)")
bzr_header_old_line = unified_header_old_line
bzr_header_new_line = unified_header_new_line

svn_index_header = unified_index_header
svn_header_old_line = unified_header_old_line
svn_header_new_line = unified_header_new_line
svn_header_timestamp = re.compile('\((?:working copy|revision (\d+))\)')

cvs_index_header = unified_index_header
cvs_rcs_header = re.compile('^RCS file: ([\s\S]+),\w{1}$')
cvs_header_old_line = unified_header_old_line
cvs_header_new_line = unified_header_new_line
cvs_header_timestamp = re.compile('([\s\S]+)\s+([\d.]+)')

# old date regex -- will try to replace with datetime parsing
cvs_header_timestamp1 = re.compile('(\d{4})[-/](\d{2})[-/](\d{2}) (\d{2}):(\d{2}):(\d{2})')
cvs_header_timestamp2 = re.compile('(\d+) (\w{3}) (\d{4}) (\d{2}):(\d{2}):(\d{2})')


def parse_patch(text):
    if type(text) == str:
        lines = text.split('\n')
    else:
        lines = text

    check = [
            unified_index_header,
            diff_command_header,
            cvs_rcs_header,
            git_index_header,
            context_header_old_line,
            unified_header_old_line,
            ]

    for c in check:
        diffs = split_by_regex(lines, c)
        if len(diffs) > 1:
            break

    for diff in diffs:
        difftext = '\n'.join(diff)
        h = parse_header(diff)
        d = parse_diff(diff)
        if d:
            yield diffobj(header=h, changes=d, text=difftext)

def parse_header(text):
    h = parse_scm_header(text)
    if h is None:
        h = parse_diff_header(text)
    return h

def parse_scm_header(text):
    if type(text) == str:
        lines = text.split('\n')
    else:
        lines = text
    check = [
            (git_index_header, parse_git_header),
            (cvs_rcs_header, parse_cvs_header),
            (svn_index_header, parse_svn_header),
            ]

    for c in check:
        diffs = findall_regex(lines, c[0])
        if len(diffs) > 0:
            git_opt = findall_regex(lines, git_diff_command_header)
            if len(git_opt) > 0:
                res = c[1](lines)
                old_path = res.old_path
                new_path = res.new_path
                if old_path.startswith('a/'):
                    old_path = old_path[2:]

                if new_path.startswith('b/'):
                    new_path = new_path[2:]

                return header(
                        index_path=res.index_path,
                        old_path = old_path,
                        old_version = res.old_version,
                        new_path = new_path,
                        new_version = res.new_version
                        )
            else:
                res = c[1](lines)

            return res

    return None

def parse_diff_header(text):
    if type(text) == str:
        lines = text.split('\n')
    else:
        lines = text
    check = [
            (unified_header_new_line, parse_unified_header),
            (context_header_old_line, parse_context_header),
            (diff_command_header, parse_diff_command_header),
            ]

    for c in check:
        diffs = findall_regex(lines, c[0])
        if len(diffs) > 0:
            return c[1](lines)

    return None # no header?


def parse_diff(text):
    if type(text) == str:
        lines = text.split('\n')
    else:
        lines = text
    check = [
            (unified_hunk_start, parse_unified_diff),
            (context_hunk_start, parse_context_diff),
            (default_hunk_start, parse_default_diff),
            (ed_hunk_start, parse_ed_diff),
            (rcs_ed_hunk_start, parse_rcs_ed_diff),
            ]

    for c in check:
        diffs = findall_regex(lines, c[0])
        if len(diffs) > 0:
            return c[1](lines)

def parse_git_header(text):
    if type(text) == str:
        lines = text.split('\n')
    else:
        lines = text

    headers = findall_regex(lines, git_index_header)
    if len(headers) == 0:
        return None

    over = None
    nver = None
    while len(lines) > 0:
        g = git_index_header.match(lines[0])
        # git always has it's own special headers
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
                old_path = o.group(1)
                new_path = n.group(1)
                if old_path.startswith('a/'):
                    old_path = old_path[2:]

                if new_path.startswith('b/'):
                    new_path = new_path[2:]

                return header(
                        index_path = None,
                        old_path = old_path,
                        old_version = over,
                        new_path = new_path,
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
        i = svn_index_header.match(lines[0])
        del lines[0]
        if i:
            diff_header = parse_diff_header(lines)
            if diff_header:
                oend = svn_header_timestamp.match(diff_header.old_version)
                nend = svn_header_timestamp.match(diff_header.new_version)
                if oend and nend:
                    return header(
                            index_path = i.group(1),
                            old_path = diff_header.old_path,
                            old_version = int(oend.group(1)),
                            new_path = diff_header.new_path,
                            new_version = int(nend.group(1)))
                return header(
                        index_path = i.group(1),
                        old_path = diff_header.old_path,
                        old_version = diff_header.old_version,
                        new_path = diff_header.new_path,
                        new_version = diff_header.new_version,
                        )
            return header(
                    index_path = i.group(1),
                    old_path = i.group(1),
                    old_version = None,
                    new_path = i.group(1),
                    new_version = None,
                    )

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
        i = cvs_index_header.match(lines[0])
        del lines[0]
        if i:
            diff_header = parse_diff_header(lines)
            if diff_header:
                oend = cvs_header_timestamp.match(diff_header.old_version)
                nend = cvs_header_timestamp.match(diff_header.new_version)
                if oend and nend:
                    return header(
                            index_path = i.group(1),
                            old_path = diff_header.old_path,
                            old_version = oend.group(2),
                            new_path = diff_header.new_path,
                            new_version = nend.group(2))
                return header(
                        index_path = i.group(1),
                        old_path = diff_header.old_path,
                        old_version = diff_header.old_version,
                        new_path = diff_header.new_path,
                        new_version = diff_header.new_version,
                        )
            return header(
                    index_path = i.group(1),
                    old_path = i.group(1),
                    old_version = None,
                    new_path = i.group(1),
                    new_version = None,
                    )

    return None

def parse_diff_command_header(text):
    if type(text) == str:
        lines = text.split('\n')
    else:
        lines = text

    headers = findall_regex(lines, diff_command_header)
    if len(headers) == 0:
        return None

    while len(lines) > 0:
        d = diff_command_header.match(lines[0])
        del lines[0]
        if d:
            return header(
                    index_path = None,
                    old_path = d.group(1),
                    old_version = None,
                    new_path = d.group(2),
                    new_version = None,
                    )

    return None

def parse_unified_header(text):
    if type(text) == str:
        lines = text.split('\n')
    else:
        lines = text

    headers = findall_regex(lines, unified_header_new_line)
    if len(headers) == 0:
        return None

    while len(lines) > 0:
        o = unified_header_old_line.match(lines[0])
        del lines[0]
        if o:
            n = unified_header_new_line.match(lines[0])
            del lines[0]
            if n:
                return header(
                        index_path = None,
                        old_path = o.group(1),
                        old_version = o.group(2),
                        new_path = n.group(1),
                        new_version = n.group(2),
                        )

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
                return header(
                        index_path = None,
                        old_path = o.group(1),
                        old_version = o.group(2),
                        new_path = n.group(1),
                        new_version = n.group(2),
                        )

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

    if len(changes) > 0:
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
            h = None

            # reset counters
            j = 0
            k = 0
        elif c:
            kind = c.group(1)
            line = c.group(2)
            c = None

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

        del lines[0]

    if len(changes) > 0:
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

    if len(changes) > 0:
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

    r = 0
    i = 0

    changes = list()

    hunks = split_by_regex(lines, ed_hunk_start)
    hunks.reverse()
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
                                r += 1
                                k += 1
                                old_end -= 1

                            # I basically have no idea why this works
                            # for these tests.
                            changes.append((None, old - r + i + k + j, hunk[0]))
                            i += 1
                            j += 1
                        elif hunk_kind == 'a':
                            changes.append((None, old - r + i + 1, hunk[0]))
                            i += 1
                        elif hunk_kind == 'd':
                            k = 0
                            while old_end >= old:
                                changes.append((old + k, None, None))
                                r += 1
                                k += 1
                                old_end -= 1

                        del hunk[0]



    if len(changes) > 0:
        return changes

    return None

def parse_rcs_ed_diff(text):
    # much like forward ed, but no 'c' type
    if type(text) == str:
        lines = text.split('\n')
    else:
        lines = text

    old = 0
    new = 0
    j = 0
    size = 0
    total_change_size = 0

    changes = list()


    hunks = split_by_regex(lines, rcs_ed_hunk_start)
    for hunk in hunks:
        if len(hunk):
            j = 0
            while len(hunk) > 0:
                o = rcs_ed_hunk_start.match(hunk[0])
                del hunk[0]
                if o:
                    hunk_kind = o.group(1)
                    old = int(o.group(2))
                    size = int(o.group(3))


                    if hunk_kind == 'a':
                        old += total_change_size + 1
                        total_change_size += size
                        while size > 0 and len(hunk) > 0:
                            changes.append((None, old + j, hunk[0]))
                            j += 1
                            size -= 1

                            del hunk[0]

                    elif hunk_kind == 'd':
                        total_change_size -= size
                        while size > 0:
                            changes.append((old + j, None, None))
                            j += 1
                            size -= 1

    if len(changes) > 0:
        return changes

    return None
