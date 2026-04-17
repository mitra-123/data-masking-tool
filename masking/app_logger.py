import logging
import sys

def get_logger(name: str = "data_masker") -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        console = logging.StreamHandler(sys.stdout)
        console.setLevel(logging.INFO)
        console.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))

        file_handler = logging.FileHandler("masking.log")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
        )

        logger.addHandler(console)
        logger.addHandler(file_handler)

    return logger