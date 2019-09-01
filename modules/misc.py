import os
import errno
import logging
from classes.Pdf import PdfHandler


def get_logger(name):
    """
    Add a StreamHandler to a logger if still not added and
    return the logger

    :param name: str
    :return: logger
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.propagate = 1  # propagate to parent
        console = logging.StreamHandler()
        logger.addHandler(console)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s [%(levelname)s] %(message)s')
        console.setFormatter(formatter)
    return logger


LOGGER = get_logger(__name__)
LOGGER.setLevel(logging.INFO)


def usage():
    """
    Log the usage of the script in case of input errors
    :return: None
    """
    message = (
        "Es.: \n\t"
        "python run_anal.py --filename <path/to/file.pdf> --nwords <num>"
    )
    LOGGER.error(message)


def extract_text(stream_in):
    """
    Convert a PDF byte stream into str
    :param stream_in: bytes
    :return: str
    """
    converter = PdfHandler(stream_in)
    corpus = converter.get_corpus()
    return corpus


def get_project_name(file_path):
    """
    Given a file path return a string
    corresponding to the base name
    witthout the extension
    :param file_path: str
    :return: str
    """
    base_name = os.path.basename(file_path)
    try:
        proj_name = os.path.splitext(base_name)[0]
    except IndexError:
        proj_name = base_name
    return proj_name


def create_nonexistent_dir(path, exc_raise=False):
    """
    Create a directory from a given path if it does not exist.
    If exc_raise is False, no exception is raised

    """
    try:
        os.makedirs(path)
        LOGGER.info("Created directory with path: {}".format(path))
    except OSError as e:
        if e.errno != errno.EEXIST:
            LOGGER.exception(
                "Could not create directory with path: {}".format(path))
            if exc_raise:
                raise
