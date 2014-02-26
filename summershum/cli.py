import optparse
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


def __get_messages(datagrepper_url, msg_id=None):
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

    if msg_id:
        param = {
                    'id': msg_id,
                    }

        response = requests.get(datagrepper_url + 'id/', params=param)
        data = json.loads(response.text)

        yield data

    else:
        # Make an initial query just to get the number of pages
        data = _load_page(page=1)
        pages = data['pages']

        for page in range(1, pages+1):
            log.info("Requesting page %i of %i from datagrepper" % (page, pages))
            data = _load_page(page)
            for message in data['raw_messages']:
                yield message


def parse_args():
    parser = optparse.OptionParser()
    parser.add_option("--id", dest="msg_id", default=None,
                      help="Process the specified message")
    parser.add_option("--force", dest="force", default=False,
                       action="store_true",
                       help="Force processing the sources even if the database"
                           "already knows it")

    return parser.parse_args()

def main():
    opts, args = parse_args()

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
    messages = __get_messages(datagrepper_url, opts.msg_id)
    for message in messages:
        msg = message['msg']
        summershum.core.ingest(
            session=session,
            msg=msg,
            config=config,
            msg_id=message.get('msg_id', None),
            force=opts.force,
        )
