# -*- coding=utf-8 -*-
import os
import sys
import logging
import argparse
import argcomplete

import tornado.ioloop
import rw.cli
from rw import gen
import fpt
import perm

import rwuser
import rwuser.model


ARG_PARSER = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawTextHelpFormatter)


@gen.coroutine
def _user():
    email = raw_input('E-Mail:')
    user = yield rwuser.model.User.find(email=email).find_one()

    if not user:
        user = rwuser.model.User()
        user.email = email
        user.first_name = raw_input('First Name:')
        user.last_name = raw_input('Last Name:')
    user['admin'] = True
    user.set_password(raw_input('Password:'))

    for role in perm.KNOWN_ROLES.values():
        has_role = user.has_role(role)
        msg = 'User {}? [{}]'.format(
            role.name,
            'Yn' if has_role else 'yN'
        )
        answer = raw_input(msg).strip().lower()
        if answer:
            if answer == 'y':
                user.add_role(role)
            else:
                user.remove_role(role)

    if '_id' in user:
        yield user.sync_db()
    else:
        yield user.insert()


def user(args):
    ioloop = tornado.ioloop.IOLoop.instance()
    scope = rw.cli.setup_app(args.module, ioloop=ioloop)
    with scope():
        ioloop.run_sync(_user)


def main():
    """Entry point of rw cli"""
    # check logging
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    logging.basicConfig(level=getattr(logging, log_level),
                        format='%(asctime)s %(name)s[%(levelname)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    ARG_PARSER.add_argument('-m', '--module', type=str)

    argcomplete.autocomplete(ARG_PARSER)
    args = ARG_PARSER.parse_args()

    if args.module is None:
        # if executed within a project automatically determine module
        if os.path.exists('setup.py'):
            data = fpt.get_setup_data('setup.py')
            pkgs = data.get('packages', [])
            if len(pkgs) == 1:
                args.module = pkgs[0]
            elif len(pkgs) > 1:
                print('Available module')
                for i, pkg in enumerate(data['packages']):
                    print('{}. {}'.format(i, pkg))
                selected = None
                while selected not in pkgs:
                    selected = raw_input('Select module: ')
                    if selected.isdigit():
                        i = int(selected)
                        if 0 <= i <= len(pkgs):
                            selected = pkgs[i]
                args.module = selected

    if args.module is None:
        print('Module not specified')
        sys.exit(1)

    user(args)




