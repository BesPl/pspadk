import logging

def _setup_logger(self):
    logger = logging.getLogger(self.__class__.__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler("test.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger