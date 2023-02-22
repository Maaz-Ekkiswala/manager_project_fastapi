import logging


from loguru import logger


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: 'CRITICAL',
        40: 'ERROR',
        30: 'WARNING',
        20: 'INFO',
        10: 'DEBUG',
        0: 'NOTSET',
    }

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        from core.main import request_id_contextvar
        message = f"Request ID:{request_id_contextvar.get()}, Message: {record.getMessage()}"
        logger.opt(depth=depth, exception=record.exc_info).log(level, message)


def setup_logging(log_level="DEBUG"):
    # intercept everything at the root logger

    logging.root.handlers = [InterceptHandler()]
    log_level = logging.getLevelName(log_level.upper())
    logging.root.setLevel(log_level)

    # remove every other logger's handlers
    # and propagate to root logger

    logging.getLogger("manager_project").handlers = []
    logging.getLogger("manager_project").propagate = True

    # configure loguru
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True