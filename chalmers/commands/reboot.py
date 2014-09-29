'''
'''
from __future__ import unicode_literals, print_function

import logging
from subprocess import Popen, check_output, CalledProcessError, PIPE
import sys

from chalmers import errors


python_exe = sys.executable
chalmers_script = sys.argv[0]
chalmers_tab_entry = '@reboot %s %s start -a' % (python_exe, chalmers_script)

log = logging.getLogger('chalmers.reboot')

def get_crontab():
    try:
        output = check_output(['crontab', '-l']).strip()
    except CalledProcessError:
        raise errors.ChalmersError("Could not read crontab")

    return output.split('\n')

def set_crontab(tab):

    new_cron_tab = '\n'.join(tab) + '\n'

    p0 = Popen(['crontab'], stdin=PIPE)
    p0.communicate(input=new_cron_tab)


def main(args):

    tab_lines = get_crontab()

    if chalmers_tab_entry in tab_lines:
        log.info("Chalmers crontab instruction already exists")
    else:
        log.info("Adding chalmers instruction to crontab")
        tab_lines.append(chalmers_tab_entry)

        set_crontab(tab_lines)

        log.info("All chalmers programs will not run on boot")


def remove(args):

    tab_lines = get_crontab()

    if chalmers_tab_entry in tab_lines:
        log.info("Removing chalmers instruction from crontab")
        tab_lines.remove(chalmers_tab_entry)

        set_crontab(tab_lines)

    else:
        log.info("Chalmers crontab instruction does not exist")

def add_parser(subparsers):
    parser = subparsers.add_parser('run-on-startup',
                                   help='Start all chalmers programs on machine startup',
                                   description=__doc__)
    parser.set_defaults(main=main)

    parser = subparsers.add_parser('dont-run-on-startup',
                                   help="Don't start chalmers on machine startup",
                                   description=__doc__)
    parser.set_defaults(main=remove)