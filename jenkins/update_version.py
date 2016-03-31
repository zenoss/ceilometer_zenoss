#!/usr/bin/env python

import re
import os
import pkg_resources

def git_version_suffix():
    '''
    Return git version suffix such as "7-e478558".

    The format is number of commits since the last tag followed by the
    hash of the most recent commit. It is created using the following
    command:

        echo $(git log --oneline origin/master..origin/develop | wc -l | awk '{print $1}')-$(git rev-parse --short origin/develop)

    Note that this currently assumes we're on the develop branch for
    a git-flow repository.
    '''
    branch = os.environ.get('GIT_BRANCH')
    if not branch or branch == 'origin/master':
        return ''

    # Something like 20-6d48e8c if branch is 20 commits ahead of master.
    suffix = os.popen(
        "echo $(git log --format='%h' origin/master..{branch} | "
        "wc -l | "
        "awk '{{print $1}}')-$(git rev-parse --short {branch})"
        .format(branch=branch),
    ).read().strip()

    # Append +feature/<name> if this is a feature branch.
    branch_match = re.match(r'^origin/feature/(.+)$', branch)
    if branch_match:
        suffix = '{}+{}'.format(suffix, branch_match.group(1))

    return suffix


def update_version():
    '''
    Modify version inside project's setup.py.

    - Add <#>-<git-hash> suffix if version ends with dev.
    '''
    changed_version = False

    with open('setup.py', 'r') as original_file:
        with open('setup.py.new', 'w') as new_file:
            version_match = re.compile(
                r'^(\s*)version\s*=\s*[\'"]([^\'\"]+)[\'"]').search

            for line in original_file:
                match = version_match(line)
                if match:
                    spaces = match.group(1)
                    version_string = match.group(2)
                    version_tuple = pkg_resources.parse_version(version_string)
                    if version_tuple[-2] == '*@':
                        new_version = ''.join((
                            version_string,
                            git_version_suffix()))

                        changed_version = True
                        line = '{}version="{}",\n'.format(spaces, new_version)

                new_file.write(line)

    if changed_version:
        os.rename('setup.py.new', 'setup.py')
    else:
        os.remove('setup.py.new')

if __name__ == "__main__":
    update_version()
