import os
import errno
import logging
from wordcloud import WordCloud
from classes.Pdf import PdfHandler
ENTITY_ABBRV_MAP = {
  "PERSON": "People, including fictional",
  "NORP": "Nationalities or religious or political groups",
  "FAC": "Buildings, airports, highways, bridges, etc",
  "ORG": "Companies, agencies, institutions, etc",
  "GPE": "Countries, cities, states",
  "LOC": "Non-GPE locations, mountain ranges, bodies of water",
  "PRODUCT": "Objects, vehicles, foods, etc. (Not services.",
  "EVENT": "Named hurricanes, battles, wars, sports events, etc",
  "WORK_OF_ART": "Titles of books, songs, etc",
  "LAW": "Named documents made into laws",
  "LANGUAGE": "Any named language",
  "DATE": "Absolute or relative dates or periods",
  "TIME": "Times smaller than a day",
  "PERCENT": "Percentage, including ”%“",
  "MONEY": "Monetary values, including unit",
  "QUANTITY": "Measurements, as of weight or distance",
  "ORDINAL": "'first', 'second', etc",
  "CARDINAL": "Numerals that do not fall under another type"
}


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
        "Please run the script providing the PDF file path and "
        "maximum number of elements to plot\n"
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


def save_wordcloud(corpus, out_dir_name):
    """
    Save wordcloud basic image
    :param corpus: str: the string of the
        document content
    :param out_dir_name: str: output directory
    :return: None
    """
    LOGGER.info("Making Word Cloud image")
    wc = WordCloud(
        width=800,
        height=600,
        background_color="black",
        contour_width=3,
        contour_color="steelblue"
    )
    wc.generate(corpus)
    output_fp = os.path.join(out_dir_name, "wordcloud.png")
    wc.to_file(output_fp)