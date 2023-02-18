import logging
from collections import Counter

import pandas as pd

from modules.misc import get_logger

LOGGER = get_logger(__name__)
LOGGER.setLevel(logging.INFO)


def kwords_count(corpus):
    """
    Perfom word count on a given corpus
    Return a descedant sorted list of tuples(word, count)
    :param corpus: list
    :return: list
    """
    LOGGER.info("Running keywords count")
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


def get_data(nlp, doc):
    """
    Get doc main POS data and entities
    with their types from a given corpus
    :param nlp: spacy.lang.en.English
    :param doc: spacy.tokens.doc.Doc object
    :return: dict
    """
    LOGGER.info("Getting data from doc")
    nouns, adjectives = [], []
    adverbs, verbs = [], []
    entities, entity_types = [], []
    for sent in doc.sents:
        for token in sent:
            if not token.is_oov and len(token.text) > 1:
                if token.pos_ == "ADV":
                    adverbs.append(token.lower_)
                if token.pos_ == "VERB" and not token.is_stop:
                    verbs.append(token.lemma_)
                if token.pos_ == "ADJ":
                    adjectives.append(token.lower_)
                if token.pos_ == "NOUN":
                    nouns.append(token.lower_)
        subdoc = nlp(sent.text)
        for ent in subdoc.ents:
            if len(ent.text) > 2:
                entities.append(ent.text)
                entity_types.append(ent.label_)
    adverbs_data = Counter(adverbs).most_common()
    verbs_data = Counter(verbs).most_common()
    nouns_data = Counter(nouns).most_common()
    adjectives_data = Counter(adjectives).most_common()
    entities_data = Counter(entities).most_common()
    entity_types_data = Counter(entity_types).most_common()
    data = {
        "adverbs": adverbs_data,
        "verbs": verbs_data,
        "nouns": nouns_data,
        "adjectives": adjectives_data,
        "entities": entities_data,
        "entity_types": entity_types_data
    }
    return data


def normalize_data(data):
    """
    Normalize data to the sum of the element in the set
    :param data: dict
    :return: dict

    Ex.:
    data_in = {
        'verbs': [('work', 2)],
        'nouns': [('painter', 1)],
        'entities': [
            ('the Ministry of Justice', 1),
            ('Rome', 1),
            ('10/09/2012', 1)
        ]
    }

    data_out = {
        'verbs': [('work', 200.0)],
        'nouns': [('painter', 100.0)],
        'adjectives': [],
        'entities': [
            ('the Ministry of Justice', 25.0),
            ('Italy', 'GPE', 25.0),
            ('Rome', 'GPE', 25.0),
            ('10/09/2012', 25.0)
        ]
    }
    """
    normalized_data = {
        key: [(el[0], (el[1] / len(value)) * 100) for el in value]
        for key, value in data.items()
    }
    return normalized_data
