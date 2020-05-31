What The Patch!?
================

.. image:: https://travis-ci.org/cscorley/whatthepatch.svg?style=flat
    :target: https://travis-ci.org/cscorley/whatthepatch

What The Patch!? is a library for both parsing and applying patch files.

Features
---------

- Parsing of almost all ``diff`` formats (except forwarded ed):

  - normal (default, --normal)
  - copied context (-c, --context)
  - unified context (-u, --unified)
  - ed script (-e, --ed)
  - rcs ed script (-n, --rcs)

- Parsing of several SCM patches:

  - CVS
  - SVN
  - Git

Installation
------------

To install What The Patch!?, simply:

.. code-block:: bash

    $ pip install whatthepatch

Usage
=====

Let us say we have a patch file containing some changes, aptly named
'somechanges.patch':

.. code-block:: diff

    --- lao	2012-12-26 23:16:54.000000000 -0600
    +++ tzu	2012-12-26 23:16:50.000000000 -0600
    @@ -1,7 +1,6 @@
    -The Way that can be told of is not the eternal Way;
    -The name that can be named is not the eternal name.
     The Nameless is the origin of Heaven and Earth;
    -The Named is the mother of all things.
    +The named is the mother of all things.
    +
     Therefore let there always be non-being,
       so we may see their subtlety,
      And let there always be being,
    @@ -9,3 +8,6 @@
     The two are the same,
     But after they are produced,
       they have different names.
    +They both may be called deep and profound.
    +Deeper and more profound,
    +The door of all subtleties!


Parsing
-------

Here is how we would use What The Patch!? in Python to get the changeset for
each diff in the patch:

.. code-block:: python

    >>> import whatthepatch
    >>> import pprint
    >>> with open('tests/casefiles/diff-unified.diff') as f:
    ...     text = f.read()
    ...
    >>> for diff in whatthepatch.parse_patch(text):
    ...     print(diff) # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    ...
    diff(header=header(index_path=None,
                       old_path='lao',
                       old_version='2013-01-05 16:56:19.000000000 -0600',
                       new_path='tzu',
                       new_version='2013-01-05 16:56:35.000000000 -0600'),
         changes=[Change(old=1, new=None, line='The Way that can be told of is not the eternal Way;', hunk=1),
                  Change(old=2, new=None, line='The name that can be named is not the eternal name.', hunk=1),
                  Change(old=3, new=1, line='The Nameless is the origin of Heaven and Earth;', hunk=1),
                  Change(old=4, new=None, line='The Named is the mother of all things.', hunk=1),
                  Change(old=None, new=2, line='The named is the mother of all things.', hunk=1),
                  Change(old=None, new=3, line='', hunk=1),
                  Change(old=5, new=4, line='Therefore let there always be non-being,', hunk=1),
                  Change(old=6, new=5, line='  so we may see their subtlety,', hunk=1),
                  Change(old=7, new=6, line='And let there always be being,', hunk=1),
                  Change(old=9, new=8, line='The two are the same,', hunk=2),
                  Change(old=10, new=9, line='But after they are produced,', hunk=2),
                  Change(old=11, new=10, line='  they have different names.', hunk=2),
                  Change(old=None, new=11, line='They both may be called deep and profound.', hunk=2),
                  Change(old=None, new=12, line='Deeper and more profound,', hunk=2),
                  Change(old=None, new=13, line='The door of all subtleties!', hunk=2)],
         text='...')

The changes are listed as they are in the patch, but instead of the +/- syntax
of the patch, we get a tuple of two numbers and the text of the line.
What these numbers indicate are as follows:

#. ``( old=1, new=None, ... )`` indicates line 1 of the file lao was **removed**.
#. ``( old=None, new=2, ... )`` indicates line 2 of the file tzu was **inserted**.
#. ``( old=5, new=4, ... )`` indicates that line 5 of lao and line 4 of tzu are **equal**.

Please note that not all patch formats provide the actual lines modified, so some
results will have the text portion of the tuple set to ``None``.

Applying
--------

To apply a diff to some lines of text, first read the patch and parse it.

.. code-block:: python

    >>> import whatthepatch
    >>> with open('tests/casefiles/diff-default.diff') as f:
    ...     text = f.read()
    ...
    >>> with open('tests/casefiles/lao') as f:
    ...     lao = f.read()
    ...
    >>> diff = [x for x in whatthepatch.parse_patch(text)]
    >>> diff = diff[0]
    >>> tzu = whatthepatch.apply_diff(diff, lao)
    >>> tzu  # doctest: +NORMALIZE_WHITESPACE
    ['The Nameless is the origin of Heaven and Earth;',
     'The named is the mother of all things.',
     '',
     'Therefore let there always be non-being,',
     '  so we may see their subtlety,',
     'And let there always be being,',
     '  so we may see their outcome.',
     'The two are the same,',
     'But after they are produced,',
     '  they have different names.',
     'They both may be called deep and profound.',
     'Deeper and more profound,',
     'The door of all subtleties!']

If apply does not satisfy your needs and you are on a system that has `patch`
in `PATH`, you can also call `apply_diff(diff, lao, use_patch=True)`. The
default is False, and patch is not necessary to apply diffs to text.

Contribute
==========

#. Fork this repository
#. Create a new branch to work on
#. Commit your tests and/or changes
#. Push and create a pull request here!

