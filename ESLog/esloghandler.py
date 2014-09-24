# -*- coding: utf-8 -*-

from datetime import datetime
import logging

from elasticsearch import Elasticsearch


class ESLogHandler(logging.Handler):
    def __init__(self, host, index, doc_type="log", level=logging.NOTSET):
        logging.Handler.__init__(self)
        
        self.index = index
        self.doc_type = doc_type
        
        self.es = Elasticsearch(host)

        # Set the default log level.
        self.setLevel(level)
    # end __init__

    def emit(self, record):
        # Break the record down to a dictionary
        message = dict()
        message["timestamp"] = datetime.now().isoformat()
        message["level"] = record.levelname
        message["name"] = record.name
        message["lineno"] = record.lineno
        message["message"] = record.msg
        
        self.es.index(index=self.index, doc_type=self.doc_type, body=message)
    # end emit
# end ESLogHandler