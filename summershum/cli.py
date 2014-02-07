import fedmsg.config

import summershum.core
import summershum.utils

import logging
import logging.config

log = logging.getLogger("summershum")


def main():
    config = fedmsg.config.load_config()
    config.update({
        'name': 'relay_inbound',
        'active': True,
    })

    logging.config.dictConfig(config.get('logging', {'version': 1}))
    log.info("Starting summershum ingestion")

    fedmsg.init(**config)

    session = summershum.utils.create_session(
        config['summershum.sqlalchemy.url'],
        create=True,
    )

    messages = summershum.utils.__get_messages()
    for message in messages:
        msg = message['msg']
        summershum.core.ingest(
            session=session,
            msg=msg,
        )
