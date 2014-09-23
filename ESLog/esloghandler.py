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
               
        self.url = urllib.parse.urlparse(url)
        
        print(self.url)
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
