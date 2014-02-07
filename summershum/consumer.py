import fedmsg.consumers
import summershum.utils

import logging
log = logging.getLogger("summershum")


class SummerShumConsumer(fedmsg.consumers.FedmsgConsumer):
    topic = 'org.fedoraproject.prod.git.lookaside.new'
    config_key = 'summershum.enabled'

    def __init__(self, *args, **kwargs):
        super(SummerShumConsumer, self).__init__(*args, **kwargs)
        log.info("Ready for ingestion")

    def consume(self, msg):
        msg = msg['body']['msg']
        log.info("Ingesting %r" % msg.get('filename'))
        fedmsg.publish(
            topic='ingest.start',
            msg=dict(original=msg),
        )
        try:
            summershum.utils.download_lookaside(msg)
            summershum.utils.get_sha1sum(msg)
        except Exception as e:
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
                msg=dict(original=msg),
            )
