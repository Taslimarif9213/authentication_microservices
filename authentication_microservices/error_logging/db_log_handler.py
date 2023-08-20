import logging

from core.settings.base import db_logger

db_default_formatter = logging.Formatter()


def log_error(error, error_code=None):
    db_logger.exception(error, {"error_code": error_code})


class DatabaseLogHandler(logging.Handler):
    def emit(self, record):
        from .models import StatusLog

        kwargs = {}

        msg = record.getMessage()

        if not all(record.exc_info):
            kwargs = {
                'logger_name': "DB_LOGGER",
                'level': record.levelno,
                'msg': msg,
                'trace': msg,
                'error_code': record.args["error_code"]
            }

        elif record.exc_info:
            trace = db_default_formatter.formatException(record.exc_info)
            trace_details = trace.split("\n")[1].split(", ")

            if trace_details:
                kwargs = {
                    'logger_name': trace_details[0],
                    'level': record.levelno,
                    'msg': msg,
                    'trace': trace,
                    'error_code': record.args["error_code"],
                    'method_name': trace_details[2].split(" ")[1]
                }
            else:
                kwargs = {
                    'logger_name': "DB_LOGGER",
                    'level': record.levelno,
                    'msg': msg,
                    'trace': trace,
                    'error_code': record.args["error_code"]
                }

        StatusLog.objects.create(**kwargs)

    def format(self, record):
        if self.formatter:
            fmt = self.formatter
        else:
            fmt = db_default_formatter

        if type(fmt) == logging.Formatter:
            record.message = record.getMessage()

            if fmt.usesTime():
                record.asctime = fmt.formatTime(record, fmt.datefmt)

            # ignore exception traceback and stack info

            return fmt.formatMessage(record)
        else:
            return fmt.format(record)
