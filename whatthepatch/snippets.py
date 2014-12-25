# -*- coding: utf-8 -*-

import os
from shutil import rmtree


# order preserving uniq for lists
def uniq(L):
    seen = {}
    result = []
    for item in L:
        if item in seen:
            continue
        seen[item] = 1
        result.append(item)
    return result


# exception handling mkdir -p
def make_dir(dir):
    try:
        os.makedirs(dir)
    except os.error as e:
        if 17 == e.errno:
            # the directory already exists
            pass
        else:
            raise e

def remove(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)

# file line length
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

# find all indices of a list of strings that match a regex
def findall_regex(l, r):
    found = list()
    for i in range(0, len(l)):
        k = r.match(l[i])
        if k:
            found.append(i)
            k = None

    return found

def split_by_regex(l, r):
    splits = list()
    indices = findall_regex(l, r)
    k = None
    for i in indices:
        if k is None:
            splits.append(l[0:i])
            k = i
        else:
            splits.append(l[k:i])
            k = i

    splits.append(l[k:])

    return splits

# http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None
