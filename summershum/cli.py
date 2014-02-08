import requests
import json

import fedmsg.config

import summershum.core
import summershum.utils

import logging
import logging.config

log = logging.getLogger("summershum")

# TODO -- get this from the fedmsg config
DATAGREPPER_URL = 'https://apps.fedoraproject.org/datagrepper/raw/'


def __get_messages():
    """ Retrieves git.lookaside.new messages from datagrepper. """

    rows_per_page = 10

    def _load_page(page):
        param = {
            'topic': 'org.fedoraproject.prod.git.lookaside.new',
            'order': 'desc',
            'page': page,
            'rows_per_page': rows_per_page,
        }

        req = requests.get(DATAGREPPER_URL, params=param)

        data = json.loads(req.text)
        return data

    # Make an initial query just to get the number of pages
    data = _load_page(page=1)
    pages = data['pages']

    for page in range(1, pages+1):
        log.info("Requesting page %i of %i from datagrepper" % (page, pages))
        data = _load_page(page)
        for message in data['raw_messages']:
            yield message


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

    messages = __get_messages()
    for message in messages:
        msg = message['msg']
        summershum.core.ingest(
            session=session,
            msg=msg,
        )
