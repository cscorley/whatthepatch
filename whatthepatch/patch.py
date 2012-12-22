#!/usr/bin/env python2.6
#
# [The "New BSD" license]
# Copyright (c) 2012 The Board of Trustees of The University of Alabama
# All rights reserved.
#
# See LICENSE for details.

from __future__ import print_function
import re



# used by CVS, subversion, git
unified_header_old_line = re.compile('^--- ([-/._\w ]+)[\s]*([\s\S]*)$')
unified_header_new_line = re.compile('^\+\+\+ ([-/._\w ]+)[\s]*([\s\S]*)$')
unified_hunk_start = re.compile('^@@ -(\d+),?(\d*) \+(\d+),?(\d*) @@$')
unified_change = re.compile('^([-+ ])([\s\S]*)$')

context_header_old_line = re.compile('^\*\*\* ([-/._\w ]+)[\s]*([\s\S]*)$')
context_header_new_line = unified_header_new_line
context_hunk_start = re.compile('^\*\*\* (\d+),(\d+) \*\*\*$')
context_hunk_mid = re.compile('^--- (\d+),(\d+) ---$')
context_change = re.compile('^([-+ !]) ([\s\S]*)$')

ed_hunk_start = re.compile('^(\d+),?(\d*)([acd])$')
ed_hunk_end = re.compile('^.$')

# much like forward ed, but no 'c' type
rcs_ed_hunk_start = re.compile('^([ad])(\d+) ?(\d*)$')

default_hunk_start = re.compile('^(\d+),?(\d*)([acd])(\d+),?(\d*)$')
default_hunk_mid = re.compile('^---$')
defualt_change = re.compile('^([><]) ([\s\S]*)$')

# Headers
#
# used by CVS, subversion
index_header = re.compile('^Index: ([-/._\w ]+)$')

# used by CVS
rcs_header = re.compile('^RCS file: ([-/._\w ]+),\w{1}$')

git_index_header = re.compile('index ([\w]{7})..([\w]{7}) \d+')
svn_header_end_part = re.compile('\((?:working copy|revision (\d+))\)')

# necessary?
# can we just use some lib to parse the date for us?
cvs_header_end_part1 = re.compile('(\d{4})[-/](\d{2})[-/](\d{2}) (\d{2}):(\d{2}):(\d{2})')
cvs_header_end_part2 = re.compile('(\d+) (\w{3}) (\d{4}) (\d{2}):(\d{2}):(\d{2})')

# cvs header: split at tab, first item is file, second is date, third is
# rev, but can't do this because when a patch is copy/pasted, editors
# could mangle the tabs into spaces
cvs_header_end_part = re.compile('([\s\S]+)[\s]+[\d.]+')

# cvs header example
"""
Index: org.eclipse.core.resources/src/org/eclipse/core/internal/localstore/SafeChunkyInputStream.java
===================================================================
RCS file: /cvsroot/eclipse/org.eclipse.core.resources/src/org/eclipse/core/internal/localstore/SafeChunkyInputStream.java,v
retrieving revision 1.6.4.1
retrieving revision 1.8
diff -u -r1.6.4.1 -r1.8
--- org.eclipse.core.resources/src/org/eclipse/core/internal/localstore/SafeChunkyInputStream.java	23 Jul 2001 17:51:45 -0000	1.6.4.1
+++ org.eclipse.core.resources/src/org/eclipse/core/internal/localstore/SafeChunkyInputStream.java	17 May 2002 20:27:56 -0000	1.8
@@ -1 +1 @@
"""

# svn header example
"""
Index: bug_cartographer/bug_method.py
===================================================================
--- bug_cartographer/bug_method.py  (revision 6534)
+++ bug_cartographer/bug_method.py  (working copy)
@@ -1,80 +0,0 @@
"""

# git header example
"""
diff --git a/bugtrace/patch.py b/bugtrace/patch.py
index a3aa076..52821d9 100644
--- a/bugtrace/patch.py
+++ b/bugtrace/patch.py
@@ -9,24 +9,68 @@
"""


def parse_patch(text):
    if type(text) == str:
        lines = text.split('\n')
    else:
        lines = text

    # Find the beginning of the first diff in the patch file
    first = 0
    while   ((not lines[first].startswith('Index:'))
            and (not lines[first].startswith('diff'))
            and (not lines[first].startswith('--- '))
            and (not lines[first].startswith('*** '))):
        first += 1
        if first == len(lines):
            return

    # temp holds a range of lines corresponding to a single diff
    temp = []
    # diffs contains each diff within the patch file
    diffs = []
    # start is the first line of the current diff
    start = first

    # Split each diff and append those to the diffs list.  We also must
    # ensure that the lines start with the same beginning as the first
    # diff as the other beginnings will appear as well anyway.
    for i in range(first+1,len(lines)):
        if (lines[i].startswith('Index:') and lines[first].startswith('Index:')):
            for j in range(start,i):
                temp.append(lines[j])
            diffs.append(temp)
            temp = []
            start = i
        elif (lines[i].startswith('diff') and lines[first].startswith('diff')):
            for j in range(start,i):
                temp.append(lines[j])
            diffs.append(temp)
            temp = []
            start = i
        elif (lines[i].startswith('*** ') and lines[first].startswith('*** ')):
            for j in range(start,i):
                temp.append(lines[j])
            diffs.append(temp)
            temp = []
            start = i
        elif (lines[i].startswith('--- ') and lines[first].startswith('--- ')):
            for j in range(start,i):
                temp.append(lines[j])
            diffs.append(temp)
            temp = []
            start = i

    # Writes last division since no more 'Index' lines to match
    for j in range(start,len(lines)):
        temp.append(lines[j])
    diffs.append(temp)

    for diff in diffs:
        h = parse_header(diff)
        d = parse_diff(diff)


def parse_header(text):
    parsers = [parse_git_header, parse_svn_header, parse_cvs_header,
            parse_unified_header, parse_context_header]

    return parse_things(parsers, text)

def parse_diff(text):
    parsers = [parse_unified_diff, parse_context_diff,
            parse_default_diff, parse_ed_diff, parse_rcs_ed_diff]

    return parse_things(parsers, text)

def parse_things(parsers, text):
    for p in parsers:
        try:
            return p(text)
        except Exception:
            pass

    return None

def parse_git_header(text):
    pass
def parse_svn_header(text):
    pass
def parse_cvs_header(text):
    pass
def parse_unified_header(text):
    pass
def parse_context_header(text):
    pass

def parse_default_diff(text):
    """
0a1,6
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
    for i in range(0, len(text)):
        yield (i+1, i+1, text[i])

def parse_unified_diff(text):
    """
--- /path/to/original   ''timestamp''
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
    for i in range(0, len(text)):
        yield (i+1, i+1, text[i])

def parse_context_diff(text):
    """
*** /path/to/original   ''timestamp''
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
    for i in range(0, len(text)):
        yield (i+1, i+1, text[i])

def parse_ed_diff(text):
    """
 24a

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
    for i in range(0, len(text)):
        yield (i+1, i+1, text[i])

def parse_rcs_ed_diff(text):
    for i in range(0, len(text)):
        yield (i+1, i+1, text[i])
