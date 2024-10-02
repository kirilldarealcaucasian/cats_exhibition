from logging import StreamHandler, getLogger
from datetime import datetime

from pythonjsonlogger import jsonlogger

from common.config import settings

__all__ = ("logger",)

logger = getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname


# setup logger
log_handler = StreamHandler()
json_log_formatter = CustomJsonFormatter('%(timestamp)s %(level)s %(pathname)s: %(message)s')
log_handler.setFormatter(fmt=json_log_formatter)
logger.addHandler(hdlr=log_handler)
