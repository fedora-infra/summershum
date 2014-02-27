import summershum.utils
import summershum.model

import fedmsg
import logging
import tempfile
import os
import shutil
log = logging.getLogger("summershum")


def ingest(session, msg, config, msg_id=None, force=False):
    tmpdir = tempfile.mkdtemp()
    extras = {}
    try:
        found = summershum.model.File.by_tar_sum(session, msg['md5sum'])

        if found and not force:
            log.info("Skipping %r, sum found in the db" % msg.get('filename'))
            return

        log.info("Ingesting %r - package: %r - msg_id: %r" % (
            msg.get('filename'), msg.get('name'), msg_id))

        # This ends up just being spammy on the bus when we run the cli.
        #fedmsg.publish(
        #    topic='ingest.start',
        #    msg=dict(original=msg),
        #)

        lookaside_url = config['summershum.lookaside']

        summershum.utils.download_lookaside(msg, lookaside_url, tmpdir)
        extras = summershum.utils.calculate_sums(session, msg, tmpdir) or {}
    except Exception as e:
        log.exception(e)
        log.error("Failed to ingest %r %r" % (msg.get('filename'), e))
        fedmsg.publish(
            topic='ingest.fail',
            msg=dict(
                original=msg,
                error=str(e),
            ),
        )
    else:
        log.info("Done ingesting %r" % msg.get('filename'))
        fedmsg.publish(
            topic='ingest.complete',
            msg=dict(original=msg, **extras),
        )
        if tmpdir and os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
