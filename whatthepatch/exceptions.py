class WhatThePatchException(Exception):
    pass


class HunkException(WhatThePatchException):
    def __init__(self, msg, hunk=None):
        self.hunk = hunk
        if hunk is not None:
            super(HunkException, self).__init__('{msg}, in hunk #{n}'.format(
                msg=msg,
                n=hunk,
            ))
        else:
            super(HunkException, self).__init__(msg)


class ApplyException(HunkException):
    pass


class ParseException(HunkException, ValueError):
    pass
