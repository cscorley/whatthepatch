class WhatThePatchException(Exception):
    pass


class ApplyException(WhatThePatchException):
    pass


class ParseException(WhatThePatchException, ValueError):
    def init(self, msg, hunk=None):
        self.hunk = hunk
        if hunk is not None:
            super(ParseException, self).__init__('{msg}, in hunk #{n}'.format(
                msg=msg,
                n=hunk,
            ))
        else:
            super(ParseException, self).__init__(msg)
