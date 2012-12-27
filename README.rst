What The Patch!?
================

What The Patch!? is a Python 2 library for parsing patch files.
It's only purpose is to read a patch file and get it into some
usable form by other programs.

Features
---------

- Parsing of all ``diff`` formats (except forwarded ed):

  - normal, context, unified, ed script, and rcs ed script

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
-----

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


.. code-block:: python

    >>> import whatthepatch.patch
    >>> with open('somechanges.patch') as f:
    ...     text = f.read()
    ...
    >>> for diff in whatthepatch.patch.parse_patch(text):
    ...     print(diff)
    ...
    diff(header=header(index_path=None,
                    old_path='lao',
                    old_version='2012-12-26 23:16:54.000000000 -0600',
                    new_path='tzu',
                    new_version='2012-12-26 23:16:50.000000000 -0600'
                    ),
        changes=[
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
        )

*Edited to show structure of the results*

The changes are listed as they are in the patch, but instead of the +/- syntax
of the patch, we get a tuple of two numbers and the text of the line.
What these numbers indicate are as follows:

#. ``( 1, None, ... )`` indicates line 1 of the file lao was **removed**.
#. ``( None, 2, ... )`` indicates line 2 of the file tzu was **inserted**.
#. ``( 5, 4, ... )`` indicates that line 5 of lao, and line 4 of tzu are **equal**.

Please note that not all patch formats provide the actual lines modified, so some 
results will have the text portion of the tuple set to ``None``.

