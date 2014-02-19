import fedmsg.consumers
import summershum.core
import summershum.model

import logging
log = logging.getLogger("summershum")


class SummerShumConsumer(fedmsg.consumers.FedmsgConsumer):
    topic = 'org.fedoraproject.prod.git.lookaside.new'
    config_key = 'summershum.enabled'

    def __init__(self, *args, **kwargs):
        super(SummerShumConsumer, self).__init__(*args, **kwargs)
        log.info("Initializing db session")
        self.session = summershum.model.create_session(
            self.hub.config['summershum.sqlalchemy.url'],
            create=True,
        )
        log.info("Ready for ingestion")

    def consume(self, msg):
        msg = msg['body']['msg']
        summershum.core.ingest(
            session=self.session,
            msg=msg,
            config=self.hub.config,
        )
