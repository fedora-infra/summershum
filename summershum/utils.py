import hashlib
import os
import shutil
import sys

import requests

from subprocess import Popen, PIPE

from model import Package, create_session

import logging
log = logging.getLogger("summershum")


def download_lookaside(message, lookaside_url, tmpdir):
    """ For a provided pkg updated, download the sources. """

    url = '%(base_url)s/%(pkg_name)s/%(sources)s/%(md5)s/%(sources)s' % (
        {
            'base_url': lookaside_url, 'pkg_name': message['name'],
            'sources': message['filename'], 'md5': message['md5sum']
        }
    )

    local_filename = "/".join([tmpdir, message['filename']])

    req = requests.get(url, stream=True)
    with open(local_filename, 'wb') as stream:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                stream.write(chunk)
                stream.flush()


def get_sha1sum(session, message, tmpdir):
    """ Extract the content of the file extracted from the fedmsg message
    and browse the sources of the specified package and for each of the
    files in the sources get their sha1sum.
    """
    local_filename = "/".join([tmpdir, message['filename']])

    if not os.path.exists(local_filename):
        raise IOError('File %s not found' % local_filename)

    # FIXME: support gems
    if local_filename.endswith('.gem'):
        return

    cmd = ['rpmdev-extract', '-C', tmpdir, local_filename]
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    if proc.returncode:
        raise IOError(
            'Something went wrong when extracting %s' % local_filename)

    filename = proc.communicate()[0].split('\n')[0].split('/')[0]

    if not filename:
        log.warning("No files extracted from %r" % local_filename)
        return

    filename = "/".join([tmpdir, filename])

    count, stored = 0, 0
    for entry in walk_directory(filename):
        count = count + 1
        pkgobj = Package.exists(session, message['md5sum'], entry[0])
        if not pkgobj:
            pkgobj = Package(
                pkg_name=message['name'],
                filename=entry[0],
                sha1sum=entry[1],
                pkg_file=message['filename'],
                pkg_sum=message['md5sum']
            )
            session.add(pkgobj)
            stored = stored + 1
        else:
            pass
    session.commit()

    if filename and os.path.exists(filename):
        shutil.rmtree(filename)
        os.unlink(local_filename)

    log.info("Stored %i of %i files" % (stored, count))


def walk_directory(directory):
    """ Return a tuple (filename, sha1) for every files present in the
    specified folder and do so recursively.
    """
    for root, dirnames, filenames in os.walk(directory):

        for filename in filenames:
            file_path = os.path.join(root, filename)
            with open(file_path) as stream:
                sha = hashlib.sha1(stream.read()).hexdigest()
                yield (file_path, sha)
