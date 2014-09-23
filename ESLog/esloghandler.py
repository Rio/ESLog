# -*- coding: utf-8 -*-

from datetime import datetime
import logging
import os
import json
import urllib.request
import urllib.parse


class ESLogHandler(logging.Handler):
    def __init__(self, url, index=None, doc_type="log", level=logging.NOTSET):
        logging.Handler.__init__(self, level=level)

        # Parse the url
        self.url = urllib.parse.urlparse(url)

        # If no scheme is given, set it to http
        if not self.url.scheme:
            self.url.scheme = "http"

        # If a scheme is given but it is not http, raise an exception
        elif self.url.scheme != "http":
            raise ValueError("Only HTTP is supported.")

        # If no port is given default to 9200
        if not self.url.port:
            self.url.port = "9200"

        # If no path is given or it is only a / use thi index and doc_type to construct one.
        if not self.url.path or self.url.path == "/":
            # an index is mandatory for Elasticsearch, doc_type too but it defaults to log
            if not index:
                raise ValueError("Elasticsearch index cannot be ommitted.")

            else:
                self.url.path = os.path.join("/", index, doc_type)
    # end __init__

    def emit(self, record):
        # Break the record down to a dictionary
        message = dict()
        message["timestamp"] = datetime.now().isoformat()
        message["level"] = record.levelname
        message["name"] = record.name
        message["lineno"] = record.lineno
        message["message"] = record.msg

        json_message = json.dumps(message)
        json_message_bytes = json_message.encode("utf8")

        urllib.request.urlopen(self.url, data=json_message_bytes)
    # end emit
# end ESLogHandler
