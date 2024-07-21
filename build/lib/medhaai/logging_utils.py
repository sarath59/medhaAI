import logging
from .config import MedhaConfig

def setup_logger(name: str, level: str = None):
    config = MedhaConfig()
    logger = logging.getLogger(name)
    logger.setLevel(level or config.log_level)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger