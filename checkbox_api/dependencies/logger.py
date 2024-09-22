import logging
import multiprocessing


class LoggerDependency:

    def __init__(
            self,
            *,
            name: str,
            formatter_string: str = '[%(levelname)s/%(processName)s] %(message)s',
            level: int = logging.INFO
    ) -> None:
        self._name = name
        self._handler = logging.StreamHandler()
        self._handler.setFormatter(
            logging.Formatter(formatter_string)
        )
        self._level = level

    def __call__(self) -> logging.Logger:
        logger = multiprocessing.get_logger()
        logger.name = self._name
        logger.addHandler(self._handler)
        logger.setLevel(self._level)
        return logger
