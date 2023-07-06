import logging
import os


def setup_logger(logger_name, level=logging.INFO, handler='stream', log_file=''):
    """
    :param logger_name:
    :param log_file:
    :param level:
    :param handler: file or stream or all
    :return:
    """
    logger_custom = logging.getLogger(logger_name)
    logger_custom.setLevel(level)
    formatter = logging.Formatter(
        '[%(asctime)s %(filename)s:%(funcName)s:%(lineno)d %(levelname)-8s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    if handler in ['file', 'all']:
        if not os.path.exists(log_file):
            os.makedirs(os.path.dirname(log_file))
        fileHandler = logging.FileHandler(log_file, mode='a')
        fileHandler.setFormatter(formatter)
        logger_custom.addHandler(fileHandler)
    if handler in ['stream', 'all']:
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        logger_custom.addHandler(streamHandler)
    return logger_custom


logger = setup_logger('notion-entertainment-tracker-logger', handler='stream')
