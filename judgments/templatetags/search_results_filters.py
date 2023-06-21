import re

from django import template

from judgments.utils import normalise_spaces, preprocess_query

register = template.Library()

not_alphanumeric = re.compile("[^a-zA-Z0-9]")


def replace_parens(string):
    return normalise_spaces(re.sub("\\(.+\\)", "", string))


def preprocess_title(string):
    return replace_parens(preprocess_query(string)).lower().strip()


def preprocess_ncn(string):
    return re.sub(not_alphanumeric, "", preprocess_query(string).lower()).strip()


@register.filter
def is_exact_match(result, query):
    return is_exact_title_match(result, query) or is_exact_ncn_match(result, query)


@register.filter
def is_exact_title_match(result, query):
    return preprocess_title(query) == preprocess_title(result.name)


@register.filter
def is_exact_ncn_match(result, query):
    return preprocess_ncn(query) == preprocess_ncn(result.neutral_citation)


@register.filter
def show_matches(result, query):
    return result.matches and not is_exact_match(result, query)
