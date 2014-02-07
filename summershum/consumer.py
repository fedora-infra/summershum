import fedmsg.consumers
import summershum.utils


class SummerShumConsumer(fedmsg.consumers.FedmsgConsumer):
    topic = 'org.fedoraproject.prod.git.lookaside.new'
    config_key = 'summershum.enabled'

    def consume(self, msg):
        msg = msg['body']['msg']
        self.log.info("Ingesting %r" % msg.get('filename'))
        fedmsg.publish(
            topic='ingest.start',
            msg=dict(original=msg),
        )
        try:
            summershum.utils.download_lookaside(msg)
            summershum.utils.get_sha1sum(msg)
        except Exception as e:
            self.log.error("Failed to ingest %r %r" % (msg.get('filename'), e))
            fedmsg.publish(
                topic='ingest.fail',
                msg=dict(
                    original=msg,
                    error=str(e),
                ),
            )
        else:
            self.log.info("Done ingesting %r" % msg.get('filename'))
            fedmsg.publish(
                topic='ingest.complete',
                msg=dict(original=msg),
            )
