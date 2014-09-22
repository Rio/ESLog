# -*- coding: utf-8 -*-

from datetime import datetime
import logging
import json
import uuid
import zmq


class ZLogHandler(logging.Handler):
    def __init__(self, host, level=logging.NOTSET):
        logging.Handler.__init__(self)

        ctx = zmq.Context.instance()
        self.socket = ctx.socket(zmq.DEALER)
        self.socket.connect(host)

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

        # serialize it to json
        #json_message = json.dumps(message)

        # Build a request for zurl in ZHTTP format
        request = dict()
        request["id"] = str(uuid.uuid4())
        request["method"] = "POST"
        request["uri"] = "http://localhost:9200/cube/log"
        request["body"] = message

        # Serialize the entire message to json and
        # prepend it with a "J" so zurl knows what format it is in.
        json_request = "J" + json.dumps(request)
        json_request_bytes = json_request.encode("utf8")

        self.socket.send_multipart([bytes(), json_request_bytes])
    # end emit
# end ZLogHandler
