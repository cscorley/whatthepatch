#!/usr/bin/env python2.6
#
# [The "New BSD" license]
# Copyright (c) 2012 The Board of Trustees of The University of Alabama
# All rights reserved.
#
# See LICENSE for details.

from __future__ import print_function
import re

class Enum(set):
    # http://stackoverflow.com/a/2182437
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

DIFF = Enum(['delete', 'insert', 'equal'])

#chunk_startu = re.compile('@@ -(\d+),(\d+) \+(\d+),(\d+) @@')
chunk_startu = re.compile('@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@')
chunk_startc = re.compile('\*\*\* (\d+),(\d+) \*\*\*')
chunk_midc = re.compile('--- (\d+),(\d+) ---')

cvs_old_file_line = re.compile('--- ([-/._\w ]+)[\s]*(\d{4})[-/](\d{2})[-/](\d{2}) (\d{2}):(\d{2}):(\d{2})')
cvs_old_file_month = re.compile('--- ([-/._\w ]+)[\s]*(\d+) (\w{3}) (\d{4}) (\d{2}):(\d{2}):(\d{2})')
cvs_new_file_line = re.compile('\+\+\+ ([-/._\w ]+)[\s]*(\d{4})[-/](\d{2})[-/](\d{2}) (\d{2}):(\d{2}):(\d{2})')
cvs_new_file_month = re.compile('\+\+\+ ([-/._\w ]+)[\s]*(\d+) (\w{3}) (\d{4}) (\d{2}):(\d{2}):(\d{2})')


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
        d = parse_diff(diff)

def parse_diff(text):
    res = parse_default_diff(text)

    if res is None:
        res = parse_unified_diff(text)

    if res is None:
        res = parse_context_diff(text)

    if res is None:
        res = parse_ed_diff(text)

    return res

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
        yield (DIFF.equal, i+1, i+1, text[i])

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
        yield (DIFF.equal, i+1, i+1, text[i])

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
        yield (DIFF.equal, i+1, i+1, text[i])

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
        yield (DIFF.equal, i+1, i+1, text[i])
