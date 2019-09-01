import os
import logging
import seaborn as sns
from modules.misc import get_logger
from matplotlib import pyplot as plt
LOGGER = get_logger(__name__)
LOGGER.setLevel(logging.INFO)


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
    sns.set(style="whitegrid")
    plt.figure(figsize=(n_max, n_max / 2))
    ax = sns.barplot(
        list(y)[:n_max],
        list(x)[:n_max],
        palette="Blues_d")
    ax.set_title(title)
    plt.xticks(fontsize=16)
    plt.xticks(fontsize=16)
    plt.xlabel(labels[1], fontsize=18)
    plt.ylabel(labels[0], fontsize=18, labelpad=60, rotation=90)
    plt.savefig(path)


def plot_pos(data, out_dir_name, n_max_words, type_pos):
    """
    Save a bar plot of the adverb count
    :param data: list
    :param out_dir_name: str
    :param n_max_words: int
    :param type_pos: str
    :return: None
    """
    LOGGER.info("Making plot for {}".format(type_pos))
    if n_max_words < len(data):
        plot_title = (
                "Top {} ".format(n_max_words) + type_pos +
                " out of {} different ones".format(len(data))
        )
    else:
        plot_title = (
            "The {} different ".format(len(data)) +
            type_pos + " found"
        )
    plot_labels = [type_pos, "% of occurrence"]
    plot_fp = os.path.join(out_dir_name, type_pos + ".png")
    save_barplot(
        data,
        plot_labels,
        n_max_words,
        plot_fp,
        title=plot_title
    )


def plot_kwords(kwords_data, out_dir_name, n_max_words):
    """
    Save a bar plot of the keywords count
    :param kwords_data: list
    :param out_dir_name: str
    :param n_max_words: int
    :return: None
    """
    LOGGER.info(
        "Making plot for the top {} keywords".format(n_max_words)
    )
    kwords_labels = ["Keyword", "Counts"]
    kwords_plot_fp = os.path.join(out_dir_name, "kwords_count.png")
    save_barplot(
        kwords_data,
        kwords_labels,
        n_max_words,
        kwords_plot_fp,
        title="Top {} Keywords".format(n_max_words)
    )

