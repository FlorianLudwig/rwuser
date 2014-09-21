import random
import string
import time
from hashlib import sha256

import perm
import rwdb


PASSWORD_RESET_EXPIRY = 24 * 60 * 60


class User(rwdb.Document, perm.UserBase):
    first_name = rwdb.Field(unicode)
    last_name = rwdb.Field(unicode)
    email = rwdb.Field(unicode)
    password = rwdb.Field(unicode)
    salt = rwdb.Field(unicode, default='')
    groups = rwdb.Field(list)
    is_deleted = rwdb.Field(bool, default=False)

    def generate_password(self, pw):
        """generate password hash"""
        if isinstance(pw, unicode):
            pw = pw.encode('utf-8')

        if not self.salt:
            # we use a 32 byte string, with each char of the string
            # having 100 possibilities we are at
            #  log2( 100**32 ) ~= 212 bits
            # of added salt
            chars = [random.choice(string.printable) for x in xrange(32)]
            self.salt = ''.join(chars)

        pw = sha256(pw).hexdigest()
        ret = sha256(pw + self.salt).hexdigest()
        for i in xrange(1328):
            ret = sha256(ret).hexdigest()
        return ret

    def set_password(self, pw):
        self.password = self.generate_password(pw)

    def check_password(self, pw):
        return self.generate_password(pw) == self.password

    def generate_password_reset_token(self):
        chars = [random.choice(string.ascii_letters + string.digits) for x in xrange(12)]
        self['password_reset_token'] = ''.join(chars)
        self['password_reset_expiry'] = time.time() + PASSWORD_RESET_EXPIRY
        return self['password_reset_token']

