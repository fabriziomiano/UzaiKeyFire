import os
import errno
import logging
from collections import Counter
from classes.Pdf import PdfHandler
from matplotlib import pyplot as plt
import seaborn as sns


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


def save_barplot(data, labels, n_max, path, title):
    """
    Save bar plot of given data in format list(tuples)

    :param data: list of tuples
    :param labels: list: x and y axis labels in this order
    :param n_max: int: max number of elements
    :param path: str: output file path
    :param title: str
    :return: None
    """
    x, y = zip(*data)
    plt.figure(figsize=(n_max, 10))
    ax = sns.barplot(
        list(x)[:n_max],
        list(y)[:n_max],
        palette="Blues_d")
    ax.set_title(title)
    plt.xticks(rotation=30)
    plt.xlabel(labels[0])
    plt.ylabel(labels[1], labelpad=60, rotation=90)
    plt.savefig(path)


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


def kwords_count(corpus):
    """
    Perfom word count on a given corpus
    Return a descedant sorted list of tuples(word, count)
    :param corpus: list
    :return: list
    """
    return Counter(corpus.split()).most_common()


def get_adverbs(doc):
    """
    Given a spacy-parsed document
    return a list with all the adverbs in it.
    :param doc: spacy.tokens.doc.Doc parsed document
    :return: list
    """
    return [
        token.lower_ for sent in doc.sents
        for token in sent if token.pos_ == "ADV"
    ]


def adv_stats(adverbs):
    """
    Return a dict with the % of occurrence of the adverbs
    in a given non-empty list of adverbs
    :param adverbs: list of adverbs
    :return:
    """
    adv_count = Counter(adverbs).most_common()
    adv_data = [
        (el[0], el[1] / len(adv_count))
        for el in adv_count
    ]
    return adv_data

