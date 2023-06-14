import logging

import backoff
import requests
from requests.exceptions import ConnectionError


class DeliveryClient(object):
    """Client class for interacting with the mailing list."""

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.admin_url = '/api/v1/admin/'

    @backoff.on_exception(wait_gen=backoff.expo, exception=Exception)
    def send(self, delivery_type, group, template_id, subject, priority):
        """Sends scheduled mailing for processing."""
        body = {
            'delivery_type': delivery_type,
            'priority': priority,
            'body': {
                'group': group,
                'template_id': str(template_id),
                'subject': subject
            },
        }
        url = f'http://{self.host}:{self.port}{self.admin_url}'
        try:
            return requests.post(url, json=body)
        except ConnectionError as e:
            logging.error('Trying to connect {url}.'.format(url=url))
            raise ConnectionError(e) from e
