"""
A Seano formatter that prints to stdout the proposed next product version
number, based on data in the given Seano query.

Secondarily, this formatter is also one of the official examples of how to
write a formatter.
"""

import argparse
import json
import logging
import re
import sys
from seano_cli.utils import SeanoFatalError

log = logging.getLogger(__name__)


def format_semver(*args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', action='store', default='-', help='Input file; use a single hyphen for stdin')

    ns = parser.parse_args(args)

    if ns.src in ['-']:
        data = sys.stdin.read()
    else:
        with open(ns.src, 'r') as f:
            data = f.read()

    try:
        data = json.loads(data)
    except json.decoder.JSONDecodeError as e:
        raise SeanoFatalError('Unable to parse Seano query output: %s' % (e,))

    print(recalculate_current_semver(data))


def recalculate_current_semver(data):
    try:
        release = data['releases'][0]
    except:
        raise SeanoFatalError('Product has no releases')

    major_kws = data.get('semver_major') or ['upgrade']
    minor_kws = data.get('semver_minor') or ['features']

    parent_versions = release.get('after') or []
    parent_versions = [x['name'] for x in parent_versions if not x.get('is-backstory')]
    parent_version = max(map(_parse_semver, parent_versions + ['0.0.0']))

    all_note_keys = set(sum([[str(x) for x in note.keys()] for note in release.get('notes') or []], []))

    if all_note_keys.intersection(major_kws):
        return _bump_major(parent_version)

    if all_note_keys.intersection(minor_kws):
        return _bump_minor(parent_version)

    return _bump_patch(parent_version)


def _parse_semver(version):
    m = re.search(r'^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)', version)
    if m:
        return (int(m.group('major')), int(m.group('minor')), int(m.group('patch')))
    log.warning('Unable to interpret as a SemVer: %s', version)
    return (0, 0, 0)


def _bump_major(curver):
    return '%d.0.0' % (curver[0] + 1,)


def _bump_minor(curver):
    return '%d.%d.0' % (curver[0], curver[1] + 1)


def _bump_patch(curver):
    return '%d.%d.%d' % (curver[0], curver[1], curver[2] + 1)
