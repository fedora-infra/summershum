import fedmsg.consumers
import summershum.utils

class SummerShumConsumer(fedmsg.consumers.FedmsgConsumer):
    topic = 'org.fedoraproject.prod.git.lookaside.new'
    config_key = 'summershum'

    def consume(self, msg):
        fedmsg.publish(
            topic='ingest.start',
            msg=dict(original=message['msg']),
        )
        try:
            summershum.utils.download_lookaside(message['msg'])
            summershum.utils.get_sha1sum(message['msg'])
        except Exception as e:
            fedmsg.publish(
                topic='ingest.fail',
                msg=dict(
                    original=message['msg'],
                    error=str(e),
                ),
            )
        else:
            fedmsg.publish(
                topic='ingest.complete',
                msg=dict(original=message['msg']),
            )
