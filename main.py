"""
This script takes a searchable PDF file as input
and produces a plot of the word frequency
"""
import argparse
import logging
from io import BytesIO

import spacy

from classes.Text import TextPreprocessor
from modules.data import get_data, kwords_count, normalize_data
from modules.misc import (
    create_nonexistent_dir, extract_text, get_logger,
    get_project_name, save_wordcloud, usage
)
from modules.plot import plot_kwords, plot_pos


def main(args, logger):
    try:
        n_max_words = args.nmaxwords
        file_path = args.filepath
        with open(file_path, 'rb') as file_in:
            pdf_byte_content = BytesIO(file_in.read())
    except OSError:
        message = "Please check the provided input parameters."
        status = {
            "status": "OK",
            "message": message
        }
        return status
    logger.info("Reading File from path {}".format(file_path))
    logger.info("N max for plots {}".format(n_max_words))
    out_dir_name = get_project_name(file_path)
    create_nonexistent_dir(out_dir_name)
    corpus = extract_text(pdf_byte_content)
    logger.info("Loading spaCy English model. This may take up to 1 minute")
    nlp = spacy.load("en_core_web_md")
    logger.info("Model loaded")
    doc = nlp(corpus)
    doc_data = get_data(nlp, doc)
    norm_data = normalize_data(doc_data)
    if len(norm_data["adverbs"]) != 0:
        plot_pos(norm_data["adverbs"], out_dir_name, n_max_words, type_pos="Adverbs")
    else:
        logger.warning("No adverbs found in the provided PDF")
    if len(norm_data["verbs"]) != 0:
        plot_pos(norm_data["verbs"], out_dir_name, n_max_words, type_pos="Verbs")
    else:
        logger.warning("No verbs found in the provided PDF")
    if len(norm_data["nouns"]) != 0:
        plot_pos(norm_data["nouns"], out_dir_name, n_max_words, type_pos="Nouns")
    else:
        logger.warning("No nouns found in the provided PDF")
    if len(norm_data["adjectives"]) != 0:
        plot_pos(norm_data["adjectives"], out_dir_name, n_max_words, type_pos="Adjectives")
    else:
        logger.warning("No adjectives found in the provided PDF")
    if len(norm_data["entities"]) != 0:
        plot_pos(norm_data["entities"], out_dir_name, n_max_words, type_pos="Entities")
        plot_pos(norm_data["entity_types"], out_dir_name, n_max_words, type_pos="Entity Types")
    else:
        logger.warning("No entities found in the provided PDF")
    save_wordcloud(corpus, out_dir_name)
    tp = TextPreprocessor(corpus)
    cleaned_text = tp.preprocess()
    kwords_data = kwords_count(cleaned_text)
    if len(kwords_data) != 0:
        plot_kwords(kwords_data, out_dir_name, n_max_words)
    else:
        logger.warning("No keywords found in the provided PDF")
    status = {
        "status": "OK",
        "message": "Done with no errors."
    }
    return status


if __name__ == "__main__":
    PARSER_DESCRIPTION = (
        "Provide the PDF file name and the maximum"
        " number of words to plot"
    )
    parser = argparse.ArgumentParser(description=PARSER_DESCRIPTION)
    argparse.ArgumentParser()
    parser.add_argument(
        '-f', '--filepath',
        type=str,
        metavar='',
        required=True,
        help="Specify the file path of the PDF to analyze"
    )
    parser.add_argument(
        '-nmw', '--nmaxwords',
        type=int,
        metavar='',
        required=False,
        default=15,
        help=("Specify the max number of words to "
              "plot (15 max recommended), default 20")
    )
    ARGS = parser.parse_args()
    LOGGER = get_logger("main")
    LOGGER.setLevel(logging.INFO)
    results = main(ARGS, LOGGER)
    if results["status"] == "OK":
        LOGGER.info(results["message"])
    else:
        LOGGER.error(
            "Exited with errors: {}".format(results["message"])
        )
        usage()
