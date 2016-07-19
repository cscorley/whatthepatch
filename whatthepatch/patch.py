# -*- coding: utf-8 -*-

import re
from collections import namedtuple

from .snippets import split_by_regex, findall_regex

header = namedtuple('header',
        'index_path old_path old_version new_path new_version')

diffobj = namedtuple('diff', 'header changes text')

file_timestamp_str = '(.+?)(?:\t|:|  +)(.*)'
# .+? was previously [^:\t\n\r\f\v]+

# general diff regex
diffcmd_header = re.compile('^diff.* (.+) (.+)$')
unified_header_index = re.compile('^Index: (.+)$')
unified_header_old_line = re.compile('^--- ' + file_timestamp_str + '$')
unified_header_new_line = re.compile('^\+\+\+ ' + file_timestamp_str + '$')
unified_hunk_start = re.compile('^@@ -(\d+),?(\d*) \+(\d+),?(\d*) @@(.*)$')
unified_change = re.compile('^([-+ ])(.*)$')

context_header_old_line = re.compile('^\*\*\* ' + file_timestamp_str + '$')
context_header_new_line = re.compile('^--- ' + file_timestamp_str + '$')
context_hunk_start = re.compile('^\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*$')
context_hunk_old = re.compile('^\*\*\* (\d+),?(\d*) \*\*\*\*$')
context_hunk_new = re.compile('^--- (\d+),?(\d*) ----$')
context_change = re.compile('^([-+ !]) (.*)$')

ed_hunk_start = re.compile('^(\d+),?(\d*)([acd])$')
ed_hunk_end = re.compile('^.$')
# much like forward ed, but no 'c' type
rcs_ed_hunk_start = re.compile('^([ad])(\d+) ?(\d*)$')

default_hunk_start = re.compile('^(\d+),?(\d*)([acd])(\d+),?(\d*)$')
default_hunk_mid = re.compile('^---$')
default_change = re.compile('^([><]) (.*)$')

# Headers

# git has a special index header and no end part
git_diffcmd_header = re.compile('^diff --git a/(.+) b/(.+)$')
git_header_index = re.compile('^index ([a-f0-9]+)..([a-f0-9]+) ?(\d*)$')
git_header_old_line = re.compile('^--- (.+)$')
git_header_new_line = re.compile('^\+\+\+ (.+)$')
git_header_file_mode = re.compile('^(new|deleted) file mode \d{6}$')
git_header_binary_file = re.compile('^Binary files (.+) and (.+) differ')

bzr_header_index = re.compile("=== (.+)")
bzr_header_old_line = unified_header_old_line
bzr_header_new_line = unified_header_new_line

svn_header_index = unified_header_index
svn_header_timestamp_version = re.compile('\((?:working copy|revision (\d+))\)')
svn_header_timestamp = re.compile('.*(\(.*\))$')

cvs_header_index = unified_header_index
cvs_header_rcs = re.compile('^RCS file: (.+)(?:,\w{1}$|$)')
cvs_header_timestamp = re.compile('(.+)\t([\d.]+)')
cvs_header_timestamp_colon = re.compile(':([\d.]+)\t(.+)')
old_cvs_diffcmd_header = re.compile('^diff.* (.+):(.*) (.+):(.*)$')


def parse_patch(text):
    try:
        lines = text.splitlines()
    except AttributeError:
        lines = text

    # maybe use this to nuke all of those line endings?
    #lines = [x.splitlines()[0] for x in lines]
    lines = [x if len(x) == 0 else x.splitlines()[0] for x in lines]

    check = [
            unified_header_index,
            diffcmd_header,
            cvs_header_rcs,
            git_header_index,
            context_header_old_line,
            unified_header_old_line,
            ]

    for c in check:
        diffs = split_by_regex(lines, c)
        if len(diffs) > 1:
            break

    for diff in diffs:
        difftext = '\n'.join(diff) + '\n'
        h = parse_header(diff)
        d = parse_diff(diff)
        if h or d:
            yield diffobj(header=h, changes=d, text=difftext)

def parse_header(text):
    h = parse_scm_header(text)
    if h is None:
        h = parse_diff_header(text)
    return h

def parse_scm_header(text):
    try:
        lines = text.splitlines()
    except AttributeError:
        lines = text

    check = [
            (git_header_index, parse_git_header),
            (old_cvs_diffcmd_header, parse_cvs_header),
            (cvs_header_rcs, parse_cvs_header),
            (svn_header_index, parse_svn_header),
            ]

    for regex, parser in check:
        diffs = findall_regex(lines, regex)
        if len(diffs) > 0:
            git_opt = findall_regex(lines, git_diffcmd_header)
            if len(git_opt) > 0:
                res = parser(lines)
                if res:
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
                res = parser(lines)

            return res

    return None

def parse_diff_header(text):
    try:
        lines = text.splitlines()
    except AttributeError:
        lines = text

    check = [
            (unified_header_new_line, parse_unified_header),
            (context_header_old_line, parse_context_header),
            (diffcmd_header, parse_diffcmd_header),
            # TODO:
            # git_header can handle version-less unified headers, but
            # will trim a/ and b/ in the paths if they exist...
            (git_header_new_line, parse_git_header),
            ]

    for regex, parser in check:
        diffs = findall_regex(lines, regex)
        if len(diffs) > 0:
            return parser(lines)

    return None # no header?


def parse_diff(text):
    try:
        lines = text.splitlines()
    except AttributeError:
        lines = text

    check = [
            (unified_hunk_start, parse_unified_diff),
            (context_hunk_start, parse_context_diff),
            (default_hunk_start, parse_default_diff),
            (ed_hunk_start, parse_ed_diff),
            (rcs_ed_hunk_start, parse_rcs_ed_diff),
            ]

    for hunk, parser in check:
        diffs = findall_regex(lines, hunk)
        if len(diffs) > 0:
            return parser(lines)

def parse_git_header(text):
    try:
        lines = text.splitlines()
    except AttributeError:
        lines = text

    # headers = findall_regex(lines, git_header_old_line)
    # if len(headers) == 0:
    #     return None

    over = nver = old_path = new_path = None
    while len(lines) > 1:
        g = git_header_index.match(lines[0])
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
        binary = git_header_binary_file.match(lines[0])
        if binary:
            old_path = binary.group(1)
            new_path = binary.group(2)
        if old_path and new_path:
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
    try:
        lines = text.splitlines()
    except AttributeError:
        lines = text

    headers = findall_regex(lines, svn_header_index)
    if len(headers) == 0:
        return None

    while len(lines) > 0:
        i = svn_header_index.match(lines[0])
        del lines[0]
        if i:
            diff_header = parse_diff_header(lines)
            if diff_header:
                opath = diff_header.old_path
                over = diff_header.old_version
                if over:
                    oend = svn_header_timestamp_version.match(over)
                    if oend and oend.group(1):
                        over = int(oend.group(1))
                elif opath:
                    ts = svn_header_timestamp.match(opath)
                    if ts:
                        opath = opath[:-len(ts.group(1))]
                        oend = svn_header_timestamp_version.match(ts.group(1))
                        if oend and oend.group(1):
                            over = int(oend.group(1))

                npath = diff_header.new_path
                nver = diff_header.new_version
                if nver:
                    nend = svn_header_timestamp_version.match(diff_header.new_version)
                    if nend and nend.group(1):
                        nver = int(nend.group(1))
                elif npath:
                    ts = svn_header_timestamp.match(npath)
                    if ts:
                        npath = npath[:-len(ts.group(1))]
                        nend = svn_header_timestamp_version.match(ts.group(1))
                        if nend and nend.group(1):
                            nver = int(nend.group(1))

                if type(over) != int:
                    over = None

                if type(nver) != int:
                    nver = None

                return header(
                        index_path = i.group(1),
                        old_path = opath,
                        old_version = over,
                        new_path = npath,
                        new_version = nver,
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
    try:
        lines = text.splitlines()
    except AttributeError:
        lines = text

    headers = findall_regex(lines, cvs_header_rcs)
    headers_old = findall_regex(lines, old_cvs_diffcmd_header)

    if headers:
        # parse rcs style headers
        while len(lines) > 0:
            i = cvs_header_index.match(lines[0])
            del lines[0]
            if i:
                diff_header = parse_diff_header(lines)
                if diff_header:
                    over = diff_header.old_version
                    if over:
                        oend = cvs_header_timestamp.match(over)
                        oend_c = cvs_header_timestamp_colon.match(over)
                        if oend:
                            over = oend.group(2)
                        elif oend_c:
                            over = oend_c.group(1)

                    nver = diff_header.new_version
                    if nver:
                        nend = cvs_header_timestamp.match(nver)
                        nend_c = cvs_header_timestamp_colon.match(nver)
                        if nend:
                            nver = nend.group(2)
                        elif nend_c:
                            nver = nend_c.group(1)

                    return header(
                            index_path = i.group(1),
                            old_path = diff_header.old_path,
                            old_version = over,
                            new_path = diff_header.new_path,
                            new_version = nver,
                            )
                return header(
                        index_path = i.group(1),
                        old_path = i.group(1),
                        old_version = None,
                        new_path = i.group(1),
                        new_version = None,
                        )
    elif headers_old:
        # parse old style headers
        while len(lines) > 0:
            i = cvs_header_index.match(lines[0])
            del lines[0]
            if i:
                d = old_cvs_diffcmd_header.match(lines[0])
                if d:
                    _ = parse_diff_header(lines) # will get rid of the useless stuff for us
                    over = d.group(2)
                    if not over:
                        over = None

                    nver = d.group(4)
                    if not nver:
                        nver = None
                    return header(
                            index_path = i.group(1),
                            old_path = d.group(1),
                            old_version = over,
                            new_path = d.group(3),
                            new_version = nver,
                            )

                return header(
                        index_path = i.group(1),
                        old_path = i.group(1),
                        old_version = None,
                        new_path = i.group(1),
                        new_version = None,
                        )

    return None

def parse_diffcmd_header(text):
    try:
        lines = text.splitlines()
    except AttributeError:
        lines = text

    headers = findall_regex(lines, diffcmd_header)
    if len(headers) == 0:
        return None

    while len(lines) > 0:
        d = diffcmd_header.match(lines[0])
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
    try:
        lines = text.splitlines()
    except AttributeError:
        lines = text

    headers = findall_regex(lines, unified_header_new_line)
    if len(headers) == 0:
        return None

    while len(lines) > 1:
        o = unified_header_old_line.match(lines[0])
        del lines[0]
        if o:
            n = unified_header_new_line.match(lines[0])
            del lines[0]
            if n:
                over = o.group(2)
                if len(over) == 0:
                    over = None

                nver = n.group(2)
                if len(nver) == 0:
                    never = None

                return header(
                        index_path = None,
                        old_path = o.group(1),
                        old_version = over,
                        new_path = n.group(1),
                        new_version = nver,
                        )

    return None

def parse_context_header(text):
    try:
        lines = text.splitlines()
    except AttributeError:
        lines = text

    headers = findall_regex(lines, context_header_old_line)
    if len(headers) == 0:
        return None

    while len(lines) > 1:
        o = context_header_old_line.match(lines[0])
        del lines[0]
        if o:
            n = context_header_new_line.match(lines[0])
            del lines[0]
            if n:
                over = o.group(2)
                if len(over) == 0:
                    over = None

                nver = n.group(2)
                if len(nver) == 0:
                    never = None

                return header(
                        index_path = None,
                        old_path = o.group(1),
                        old_version = over,
                        new_path = n.group(1),
                        new_version = nver,
                        )

    return None


def parse_default_diff(text):
    try:
        lines = text.splitlines()
    except AttributeError:
        lines = text

    old = 0
    new = 0
    old_len = 0
    new_len = 0
    r = 0
    i = 0

    changes = list()

    hunks = split_by_regex(lines, default_hunk_start)
    for hunk in hunks:
        if len(hunk):
            r = 0
            i = 0
            while len(hunk) > 0:
                h = default_hunk_start.match(hunk[0])
                c = default_change.match(hunk[0])
                del hunk[0]
                if h:
                    old = int(h.group(1))
                    if len(h.group(2)) > 0:
                        old_len = int(h.group(2)) - old + 1
                    else:
                        old_len = 0

                    new = int(h.group(4))
                    if len(h.group(5)) > 0:
                        new_len = int(h.group(5)) - new + 1
                    else:
                        new_len = 0

                    hunk_kind = h.group(3)
                elif c:
                    kind = c.group(1)
                    line = c.group(2)

                    if kind == '<' and (r != old_len or r == 0):
                        changes.append((old + r, None, line))
                        r += 1
                    elif kind == '>' and (i != new_len or i == 0):
                        changes.append((None, new + i, line))
                        i += 1

    if len(changes) > 0:
        return changes

    return None

def parse_unified_diff(text):
    try:
        lines = text.splitlines()
    except AttributeError:
        lines = text

    old = 0
    new = 0
    r = 0
    i = 0

    changes = list()

    hunks = split_by_regex(lines, unified_hunk_start)
    for hunk in hunks:
        # reset counters
        r = 0
        i = 0
        while len(hunk) > 0:
            h = unified_hunk_start.match(hunk[0])
            del hunk[0]
            if h:
                old = int(h.group(1))
                if len(h.group(2)) > 0:
                    old_len = int(h.group(2))
                else:
                    old_len = 0

                new = int(h.group(3))
                if len(h.group(4)) > 0:
                    new_len = int(h.group(4))
                else:
                    new_len = 0

                h = None
                break

        while len(hunk) > 0:
            c = unified_change.match(hunk[0])
            if c:
                kind = c.group(1)
                line = c.group(2)
                c = None

                if kind == '-' and (r != old_len or r == 0):
                    changes.append((old + r, None, line))
                    r += 1
                elif kind == '+' and (i != new_len or i == 0):
                    changes.append((None, new + i, line))
                    i += 1
                elif kind == ' ' and r != old_len and i != new_len:
                    changes.append((old + r, new + i, line))
                    r += 1
                    i += 1

            del hunk[0]

    if len(changes) > 0:
        return changes

    return None



def parse_context_diff(text):
    try:
        lines = text.splitlines()
    except AttributeError:
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
                    old_len = int(o.group(2)) + 1 - old
                    while len(new_hunk) > 0:
                        n = context_hunk_new.match(new_hunk[0])
                        del new_hunk[0]
                        if n:
                            new = int(n.group(1))
                            new_len = int(n.group(2)) + 1 - new
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

                        if kind == '-' and (j != old_len or j == 0):
                            changes.append((old + j, None, line))
                            j += 1
                        elif kind == ' ' and ((j != old_len and k != new_len)
                                              or (j == 0 or k == 0)):
                            changes.append((old + j, new + k, line))
                            j += 1
                            k += 1
                        elif kind == '+' or kind == '!':
                            raise ValueError("Got unexpected change in removal hunk: " + kind)

            elif len(old_hunk) == 0 and len(new_hunk) > 0:
                # only insertions left?
                while len(new_hunk) > 0:
                    c = context_change.match(new_hunk[0])
                    del new_hunk[0]
                    if c:
                        kind = c.group(1)
                        line = c.group(2)

                        if kind == '+' and (k != new_len or k == 0):
                            changes.append((None, new + k, line))
                            k += 1
                        elif kind == ' ' and ((j != old_len and k != new_len)
                                              or (j == 0 or k == 0)):
                            changes.append((old + j, new + k, line))
                            j += 1
                            k += 1
                        elif kind == '-' or kind == '!':
                            raise ValueError("Got unexpected change in insertion hunk: " + kind)
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
                    elif okind == '-' or okind == '!' and (j != old_len or j == 0):
                        changes.append((old + j, None, oline))
                        j += 1
                        del old_hunk[0]
                    elif nkind == '+' or nkind == '!' and (k != old_len or k == 0):
                        changes.append((None, new + k, nline))
                        k += 1
                        del new_hunk[0]
                    else:
                        return None

    if len(changes) > 0:
        return changes

    return None


def parse_ed_diff(text):
    try:
        lines = text.splitlines()
    except AttributeError:
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
                    if hunk_kind == 'd':
                        k = 0
                        while old_end >= old:
                            changes.append((old + k, None, None))
                            r += 1
                            k += 1
                            old_end -= 1
                    else:
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

                            del hunk[0]



    if len(changes) > 0:
        return changes

    return None

def parse_rcs_ed_diff(text):
    # much like forward ed, but no 'c' type
    try:
        lines = text.splitlines()
    except AttributeError:
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
