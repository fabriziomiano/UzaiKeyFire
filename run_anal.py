"""
This script takes a searchable PDF file as input
and produces a plot of the word frequency
"""
import os
import argparse
import logging
import spacy
from io import BytesIO
from classes.Text import TextPreprocessor
from utils.misc import (
    usage, get_logger, extract_text, kwords_count,
    get_project_name, save_barplot, create_nonexistent_dir,
    get_adverbs, adv_stats
)


def main(args, logger):
    try:
        n_max_words = args.nwords
        file_path = args.filename
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
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(corpus)
    adverbs = get_adverbs(doc)
    adverbs_data = adv_stats(adverbs)
    if len(adverbs_data) != 0:
        if n_max_words < len(adverbs_data):
            adv_plot_title = "Top {} Adverbs out of {} different ones".format(
                n_max_words, len(adverbs_data))
        else:
            adv_plot_title = "The {} different adverbs found".format(
                len(adverbs_data)
            )
        adverbs_labels = ["Adverb", "% of occurrence"]
        adverbs_plot_fp = os.path.join(out_dir_name, "adv_stats.png")
        save_barplot(
            adverbs_data,
            adverbs_labels,
            n_max_words,
            adverbs_plot_fp,
            title=adv_plot_title
        )
    else:
        logger.warning("No adverbs found in the provided PDF")
    tp = TextPreprocessor(corpus)
    cleaned_text = tp.preprocess()
    kwords_data = kwords_count(cleaned_text)
    if len(kwords_data) != 0:
        kwords_labels = ["Keyword", "Counts"]
        kwords_plot_fp = os.path.join(out_dir_name, "kwords_count.png")
        save_barplot(
            kwords_data,
            kwords_labels,
            n_max_words,
            kwords_plot_fp,
            title="Top {} Keywords".format(n_max_words)
        )
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
        '-f', '--filename',
        type=str,
        metavar='',
        required=True,
        help="Specify the file path of the PDF to analyze"
    )
    parser.add_argument(
        '-nw', '--nwords',
        type=int,
        metavar='',
        required=False,
        default=15,
        help=("Specify the max number of words to "
              "plot (20 max recommended), default 15")
    )
    ARGS = parser.parse_args()
    LOGGER = get_logger(__name__)
    LOGGER.setLevel(logging.INFO)
    results = main(ARGS, LOGGER)
    if results["status"] == "OK":
        LOGGER.info(results["message"])
    else:
        LOGGER.error(
            "Exited with errors: {}".format(results["message"])
        )
        usage()
