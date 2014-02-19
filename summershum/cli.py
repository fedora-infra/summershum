import requests
import json

import fedmsg.config

import summershum.core
import summershum.model

import logging
try:
    # Python2.7 and later
    from logging.config import dictConfig
except ImportError:
    # For Python2.6, we rely on a third party module.
    from logutils.dictconfig import dictConfig


log = logging.getLogger("summershum")


def __get_messages(datagrepper_url):
    """ Retrieves git.lookaside.new messages from datagrepper. """

    rows_per_page = 10

    def _load_page(page):
        param = {
            'topic': 'org.fedoraproject.prod.git.lookaside.new',
            'order': 'desc',
            'page': page,
            'rows_per_page': rows_per_page,
        }

        response = requests.get(datagrepper_url + 'raw/', params=param)
        return json.loads(response.text)

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

    dictConfig(config.get('logging', {'version': 1}))
    log.info("Starting summershum ingestion")

    fedmsg.init(**config)

    session = summershum.model.create_session(
        config['summershum.sqlalchemy.url'],
        create=True,
    )

    datagrepper_url = config['summershum.datagrepper']
    messages = __get_messages(datagrepper_url)
    for message in messages:
        msg = message['msg']
        summershum.core.ingest(
            session=session,
            msg=msg,
            config=config,
        )
