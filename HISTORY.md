# next

Nothing yet :)

# 1.0.7

- PR #62 fix: incorrect regular expression matching diffcmd (Thanks, @jingfelix)
- Support up to 3.13
- Drop support up to 3.8

# 1.0.6

- PR #60 Improve huge_patch test (Thanks, @arkamar)
- Support up to 3.12
- Drop support up to 3.7

# 1.0.5

- PR #57 bugfix:min line in binary diff (Thanks, @babenek and @abbradar)

# 1.0.4

- PR #53 git binary patch support (Thanks, @babenek)
- PR #51 Remove redundant wheel dep from pyproject.toml (Thanks, @mgorny)
- Add basic nix release support

# 1.0.3

- PR #46 Code optimization for unified diff parsing (Thanks, @babenek)
- Package using build module and pyproject.toml
- Support up to 3.11
- Drop support up to 3.6

# 1.0.2

- Support up to 3.9
- PR #42 Fix unified diff parse error (Thanks, @kkpattern)

# 1.0.1

- PR #37 Replace nose with pytest (Thanks, @MeggyCal)
- PR #39 Fix bug where context diffs would not parse (Thanks, @FallenSky2077)

# 1.0.0

- Issue #26 fix where hardcoded "/tmp" reference was being used
- Support up to Python 3.8
- Drop support for Python 2, 3.4

Dev-only:

- Bump Code of Conduct to 2.0
- Setup Github Actions for package publishing
- Setup Github Actions for build and testing
  - Move off Travis and Tox in favor of Github Actions

# 0.0.6

- PR #13 Support for reverse patching (Thanks, @graingert)
  - This is a breaking change that converted the parsed tuples into namedtuples
    and added the hunk number to that tuple
- PR #20 Support up to Python 3.7, drop support for 3.3 (Thanks, @graingert)
- Issue #18 fix for empty file adds in git

# 0.0.5

- PR #6 Added better support for binary files. (Thanks, @ramusus)
- PR #3 Added support for git index revision ids that have more than 7
  characters (Thanks, @jopereria)

# 0.0.4

- PR #2 Bug fix for one-liner diffs (Thanks, @thoward)
- Issue #1 fix where some old real test cases were left failing
- Added a Code of Conduct
- Added support for Python 3.5

# 0.0.3

- Better matching for almost all patch headers
- Support patches that have entire hunks removed
- Support git patches that are missing index header file modes
- Moved to MIT license
- Officially adopt Python 3

# 0.0.2

- Initial support to apply parsed patches
- Support diffs that do not have headers

# 0.0.1

- The very first release that included parsing support for patches in unified
  diff format, context diff format, ed diff format, git, bazaar, subversion, and
  cvs.
